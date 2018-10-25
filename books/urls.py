from django.conf.urls import url , include
from django.contrib import admin
from views import (BookDetail , BookList , PublisherList 
    , AuthorList ,CreateVote , UserCreate , LoginView)
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^books/(?P<pk>\d{1,10})/vote/$' , CreateVote.as_view(),name='books_vote'),
    url(r'^books/(?P<pk>\d{1,10})/$', BookDetail.as_view() , name='books_detail' ),
    url(r'^books/$', BookList.as_view() , name='books_list'),
    url(r'^publishers/$',PublisherList.as_view()),
    url(r'^authors/$',AuthorList.as_view()),
    url(r'^users/$',UserCreate.as_view(),name='create_user'),
    #url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^login/$", views.obtain_auth_token, name="login"),
]