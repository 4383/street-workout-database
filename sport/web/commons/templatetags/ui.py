__author__ = 'herve'
from django import template

from exercises.models import ImageExercise

register = template.Library()


@register.inclusion_tag('ui/exercise-preview.html')
def exercise_preview(item):
    try:
        image = ImageExercise.objects.filter(active=True, binding=item)[0]
    except IndexError:
        image = None
    return {"item": item, "image": image}
