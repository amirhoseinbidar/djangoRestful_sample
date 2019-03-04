from django.conf.urls import url , include
from django.contrib import admin
from .views import (BookDetail , BookList , PublisherList 
    , AuthorList ,CreateVote , UserCreate , LoginView , BookSearch)
from rest_framework.authtoken import views

app_name = 'api'
urlpatterns = [
    url(r'^books/search/$' , BookSearch.as_view(),name='books_search'),
    url(r'^books/(?P<pk>\d{1,10})/vote/$' , CreateVote.as_view(),name='books_vote'),
    url(r'^books/(?P<pk>\d{1,10})/$', BookDetail.as_view() , name='books_detail' ),
    url(r'^books/$', BookList.as_view() , name='books_list'),
    url(r'^publishers/$',PublisherList.as_view() , name = 'publishers_view'),
    url(r'^authors/$',AuthorList.as_view(), name = 'authors_view'),
    url(r'^users/$',UserCreate.as_view(),name='create_user'),
    #url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^login/$", views.obtain_auth_token, name="login"),
]