# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField(blank=True)

    class Meta:
        db_table = "publisher"
    def __unicode__(self):
        return u'{0} , website:{1}'.format(self.name,self.website)

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True,verbose_name='e-mail')

    class Meta:
        db_table = "author"
    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name,self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher , on_delete=models.CASCADE )
    publication_date = models.DateField(null = True)
    num_pages = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField()

    class Meta:
        db_table = 'book'
    def __unicode__(self):
        return self.title

class Vote(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
