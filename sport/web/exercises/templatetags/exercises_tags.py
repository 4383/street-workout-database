__author__ = 'herve'
import json

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from exercises.models import Exercise
from exercises.models import ImageCategory
from exercises.models import ImageExercise
from exercises.models import MappingAreaMuscles
from exercises.models import Mapping
from exercises.models import Muscle
from exercises.models import VideoCategory
from exercises.models import VideoExercise

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


@register.inclusion_tag('tags/show_exercise_menu.html')
def show_exercise_menu(exercise, active="description"):
    total_images = ImageExercise.objects.filter(active=True, binding=exercise).count()
    total_videos = VideoExercise.objects.filter(active=True, binding=exercise).count()
    return {'total_images': total_images,
            'total_videos': total_videos,
            'active': active,
            'exercise': exercise, }


@register.inclusion_tag('tags/show_muscles_mapping.html')
def show_muscles_mapping(specified_object):
    if not hasattr(specified_object, 'muscles'):
        return

    actives_muscles = Muscle.objects.filter(id__in=specified_object.muscles.all, active=True)
    if not actives_muscles:
        return

    try:
        mapping = Mapping.objects.get(name="category_muscle_mapping")
    except ObjectDoesNotExist:
        mapping = None

    muscles_list = []
    json_data = {}
    reverse_json_data = {}
    for active_muscle in actives_muscles:
        areas = MappingAreaMuscles.objects.filter(binding=active_muscle)
        muscles_data = {
            'muscle': active_muscle,
            'area': areas,
        }

        for area in areas:
            if area.mapping == mapping:
                entry = {area.name: {
                    "image1": settings.MEDIA_URL + str(area.first_image_hover),
                    "image2": settings.MEDIA_URL + str(area.second_image_hover),
                    "muscle": active_muscle.name,
                }}
                reverse_entry = {active_muscle.name: {
                    "image1": settings.MEDIA_URL + str(area.first_image_hover),
                    "image2": settings.MEDIA_URL + str(area.second_image_hover),
                    "area": area.name,
                }}
                json_data.update(entry)
                reverse_json_data.update(reverse_entry)

        muscles_list.append(muscles_data)

    return {"muscles_list": muscles_list,
            "mapping": mapping,
            "json_data": json.dumps(json_data),
            "reverse_json_data": reverse_json_data}
