from django.urls import path

from . import views

app_name = "quotes"


urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('author/<int:id_>/', views.description_auth, name='description_auth'),
    path('tag_add/', views.tag_add, name='tag_add'),
    path('author_add/', views.author_add, name='author_add'),
    path('quote_add/', views.quote_add, name='quote_add')
]
