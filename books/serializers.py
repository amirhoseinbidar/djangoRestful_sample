from rest_framework import serializers
from .models import Author, Book, Publisher , Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AuthorSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(many = False , required = False)
    authors = AuthorSerializer(many = True)
    class Meta:
        model = Book
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password' : {'write_only':True}}
    def create(self,validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
