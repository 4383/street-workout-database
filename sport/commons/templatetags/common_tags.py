__author__ = 'herve.beraud'
from django import template
from exercises.models import Category
from exercises.models import MuscleGroup
from exercises.models import Muscle

register = template.Library()


@register.inclusion_tag('common_tags/show_exercises_menu.html')
def show_exercises_menu():
    categories = Category.objects.filter(active=True).count()
    muscles_groups = MuscleGroup.objects.filter(active=True).count()
    muscles = Muscle.objects.filter(active=True).count()
    return {'categories': categories, 'muscles_group': muscles_groups, 'muscles': muscles}


@register.inclusion_tag('common_tags/image_gallery.html')
def images_gallery(images):
    return {"images": images}