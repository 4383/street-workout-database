__author__ = 'herve.beraud'
from django import template
from exercises.models import Category
from exercises.models import MuscleGroup

register = template.Library()


@register.inclusion_tag('common_tags/show_exercises_menu.html')
def show_exercises_menu():
    categories = Category.objects.filter(active=True)
    muscles_group = MuscleGroup.objects.filter(active=True)
    return {'categories': categories, 'muscles_group': muscles_group}