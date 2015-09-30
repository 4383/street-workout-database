__author__ = 'herve'
from django import template
from django.core.exceptions import ObjectDoesNotExist
from exercises.models import Exercise
from exercises.models import ImageCategory
from exercises.models import MappingAreaMuscles
from exercises.models import Mapping
from exercises.models import Muscle
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
            'category': category, }


@register.inclusion_tag('tags/show_muscles_mapping.html')
def show_muscles_mapping(specified_object):
    if not hasattr(specified_object, 'muscles'):
        return

    actives_muscles = Muscle.objects.filter(id__in=specified_object.muscles.all, active=True)
    if not actives_muscles:
        return

    muscles_list = []
    for active_muscle in actives_muscles:
        try:
            muscles_data = {
                'muscle': active_muscle,
                'area': MappingAreaMuscles.objects.filter(binding=active_muscle),
                }
        except IndexError:
            muscles_data = {
                'muscle': active_muscle,
                'area': MappingAreaMuscles.objects.filter(binding=active_muscle),
                }
        muscles_list.append(muscles_data)

    try:
        mapping = Mapping.objects.get(name="category_muscle_mapping")
    except ObjectDoesNotExist:
        mapping = None

    return {"muscles_list": muscles_list, "mapping": mapping}
