__author__ = 'herve.beraud'
from django.conf.urls import url, patterns

from . import views

urlpatterns = [
    url(r'^categories/$', views.categories, name='exercises_categories'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/$', views.category, name='exercises_category'),
    url(r'^exercise/(?P<slug>[a-z\-0-9]+)/$', views.exercise, name='exercise'),
]