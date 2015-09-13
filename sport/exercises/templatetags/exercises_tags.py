__author__ = 'herve'
from django import template
from exercises.models import Exercise
from exercises.models import ImageCategory
from exercises.models import VideoCategory

register = template.Library()


@register.inclusion_tag('tags/show_exercises_category_menu.html')
def show_exercises_category_menu(category, active="exercises"):
    total_exercises = Exercise.objects.filter(active=True, category=category).count()
    total_images = ImageCategory.objects.filter(active=True, binding=category).count()
    total_videos = VideoCategory.objects.filter(active=True, binding=category).count()
    return {'total_exercises': total_exercises,
            'total_images': total_images,
            'total_videos': total_videos,
            'active': active,
            'category': category,
    }