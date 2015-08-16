__author__ = 'herve.beraud'
from django.conf.urls import url, patterns

from . import views

urlpatterns = [
    url(r'^exercise/(?P<slug>[a-z\-0-9]+)/$', views.exercise, name='exercise'),
    # Categories
    url(r'^categories/$', views.categories, name='exercises_categories'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/$', views.category, name='exercises_category'),
    # Muscles
    url(r'^muscles/$', views.muscles, name='exercises_muscles'),
    url(r'^muscle/(?P<slug>[a-z\-0-9]+)/$', views.muscle, name='exercises_muscle'),
    # Muscles-Groups
    url(r'^muscles-groups/$', views.muscles_groups, name='exercises_muscles_groups'),
    url(r'^muscle-group/(?P<slug>[a-z\-0-9]+)/$', views.muscle_group, name='exercises_muscle_group'),
]

