__author__ = 'herve.beraud'
from django.conf.urls import url

from . import views

urlpatterns = [
    # Exercises
    url(r'^exercise/(?P<slug>[a-z\-0-9]+)/$', views.exercise, name='exercise'),
    url(r'^exercise/(?P<slug>[a-z\-0-9]+)/images/$', views.exercise_images, name='exercise_images'),
    url(r'^exercise/(?P<slug>[a-z\-0-9]+)/videos/$', views.exercise_videos, name='exercise_videos'),
    # Categories
    url(r'^categories/$', views.categories, name='exercises_categories'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/$', views.category, name='exercises_category'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/exercises/$', views.category_exercises, name='exercises_category_exercises'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/images/$', views.category_images, name='exercises_category_images'),
    url(r'^category/(?P<slug>[a-z\-0-9]+)/videos/$', views.category_videos, name='exercises_category_videos'),
    # Muscles
    url(r'^muscles/$', views.muscles, name='exercises_muscles'),
    url(r'^muscles/ajax-exercises-by-muscles/$', views.ajax_exercises_by_muscles, name='ajax_exercises_by_muscles'),
    url(r'^muscle/(?P<slug>[a-z\-0-9]+)/$', views.muscle, name='exercises_muscle'),
    # Muscles-Groups
    url(r'^muscles-groups/$', views.muscles_groups, name='exercises_muscles_groups'),
    url(r'^muscle-group/(?P<slug>[a-z\-0-9]+)/$', views.muscle_group, name='exercises_muscle_group'),
]

