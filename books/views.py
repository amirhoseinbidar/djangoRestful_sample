# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book , Publisher , Author
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework.response import Response
from .serializers import (BookSerializer , AuthorSerializer 
    , PublisherSerializer , VoteSerializer , UserSerializer)

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class PublisherList(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class CreateVote(APIView):
    def post(self, request , pk):
        voted_by = request.user

        data = {'book':pk , 'voted_by':voted_by.pk}
        print data
        serializer = VoteSerializer(data= data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)    