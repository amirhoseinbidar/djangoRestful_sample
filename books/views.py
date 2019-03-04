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
from rest_framework.exceptions import ParseError

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

class BookSearch(generics.GenericAPIView , generics.mixins.ListModelMixin):
    serializer_class = BookSerializer
    def get_queryset(self):
        try:
            publisher ,authors , data = self.get_data()
        except ValueError and TypeError :
            raise ParseError('uncorrect argument')
        
        books = Book.objects.filter(**data)
        if authors:
            books = books.filter(authors__pk__in = authors)
        if publisher != -1:
            books = books.filter(publisher__pk = publisher )
        return books

    def get_data(self):
        data  = {}
        data['title'] = self.request.POST.get('title' , None)
        authors = self.request.POST.get('authors' , None)
        publisher = int( self.request.POST.get('publisher' , -1) )
        data['publication_date'] = self.request.POST.get('publication_data' , None)
        data['num_pages'] = int( self.request.POST.get('num_pages' , -1) )
        data['cost'] = int(self.request.POST.get('cost' , -1))
        buf = data.copy()
        
        for key in buf :
            if not data[key] or data[key] == -1:
                del data[key]

        if authors :
            authors = [ int(ele) for ele in authors.split(',')]
        return (publisher , authors , data)                                                                 

    def post(self,*args,**kwargs):
        return self.list(*args,**kwargs)


class CreateVote(APIView):
    def post(self, request , pk):
        voted_by = request.user

        data = {'book':pk , 'voted_by':voted_by.pk}
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