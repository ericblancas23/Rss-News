from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feeds/', views.rest_feeds, name='rest-feeds'),
    re_path(r'^feeds/(?P<pk>[0-9]+)/$', views.rest_feeds_detail, name='rest_feeds_detail'),
    path('items/', views.rest_items, name='rest_items')
]