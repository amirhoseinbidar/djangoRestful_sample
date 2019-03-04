# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from .models import Author, Book, Publisher, User, Vote
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
# Create your tests here.


class BaseAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = self.setup_test_user()
        self.view = None

    @staticmethod
    def setup_test_user():
        return BaseAPITest.setup_user(
            'test', 'test', 'test@test.com')

    @staticmethod
    def setup_user(username, password, email):
        return get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

    @staticmethod
    def write_info(expect_code, response):
        status_text = getattr(response, 'status_text', None)
        status_code = getattr(response, 'status_code', None)
        data = getattr(response, 'data', None) or getattr(
            response, 'content', None)
        return 'Expected Response Code {}, received {} instead. \n error message: {} \n error data:{}'.format(
            expect_code, status_code, status_text, data)


class BookAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.client.login(username='test', password='test')

        self.author1 = Author.objects.create(
            first_name='amir', last_name='testman', email='aaa@test.com')
        self.author2 = Author.objects.create(
            first_name='hamed', last_name='testman', email='hhh@test.com')  # این دوتا داداشن :D
        self.author3 = Author.objects.create(
            first_name='homa', last_name='testainy', email='hhh@test.com')
        self.publisher1 = Publisher.objects.create(
            name='elahiat-pu', address='abbas abad', city='varamin', state_province='tehran', country='iran', website='www.elahiat-pu.com')
        self.publisher2 = Publisher.objects.create(
            name='mathomi', address='vazir abad', city='tabriz', state_province='tabriz', country='iran', website='www.mathomi.com')
        self.book1 = Book.objects.create(
            title='a testman problems', cost='10500', publisher=self.publisher2, publication_date='2000-9-2')
        self.book1.authors.add(self.author2)
        self.book2 = Book.objects.create(
            title='testor the odyssey', cost='20000', publisher=self.publisher2, publication_date='2001-4-3')
        self.book2.authors.add(self.author1)
        
        self.book3 = Book.objects.create(
            title='hot test for every one', cost='20000', publisher=self.publisher1, publication_date='2001-4-3')
        self.book3.authors.add(self.author3)

class BookTest(BookAPITest):

    def test_view(self):
        url = reverse('api:books_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))

        result = json.loads(response.content)[0]['title']
        assert result == 'a testman problems'

    def test_detail(self):
        url = reverse('api:books_detail', kwargs={'pk': self.book2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))

        result = json.loads(response.content)['title']
        assert result == 'testor the odyssey'

    def test_vote(self):
        url = reverse('api:books_vote', kwargs={'pk': self.book2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code,201,self.write_info(201,response))

        # if vote doesn't exist will raise error
        print(Vote.objects.get(book=self.book2) )

    def test_search1(self):
        url = reverse('api:books_search' )
        response = self.client.post(url , {'title':'testor the odyssey'})
        self.assertEqual(response.status_code,200,self.write_info(200,response))

        result = json.loads(response.content)[0]['title']
        assert result == 'testor the odyssey'
    
    def test_search2(self):
        url = reverse('api:books_search' )
        response = self.client.post(url , {'authors':' {} , {} '.format(self.author1.pk ,self.author3.pk)})
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
        result = json.loads(response.content)[0]['title']
        assert result == 'testor the odyssey'
        result = json.loads(response.content)[1]['title']
        assert result == 'hot test for every one'
    
    def test_search3(self):
        url = reverse('api:books_search')
        response = self.client.post(url , {'cost':'20000' , 'publisher': '{}'.format(self.publisher1.pk) })
        self.assertEqual(response.status_code,200,self.write_info(200,response))
       
        result = json.loads(response.content)[0]['title']
        assert result == 'hot test for every one'
    
    def test_publishers(self):
        url = reverse('api:publishers_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
        
        result = json.loads(response.content)[0]['name']
        assert result == 'elahiat-pu'
        result = json.loads(response.content)[1]['name']
        assert result == 'mathomi'

    def test_author(self):
        url = reverse('api:authors_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200,self.write_info(200,response))
    
        result = json.loads(response.content)[0]['first_name']
        assert result == 'amir'
        result = json.loads(response.content)[1]['first_name']
        assert result == 'hamed'
        result = json.loads(response.content)[2]['first_name']
        assert result == 'homa'