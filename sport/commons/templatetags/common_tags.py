__author__ = 'herve.beraud'
from datetime import datetime, timedelta
from django import template
from django.core.exceptions import ObjectDoesNotExist
from community.models import InformationMessage
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


@register.inclusion_tag('common_tags/grid-list-gallery.html')
def grid_list_gallery(items, display_level=True, display_menu=True, shortcut_menu=True, semantic_type="exercise"):
    return {"items": items,
            "display_level": display_level,
            "display_menu": display_menu,
            "shortcut_menu": shortcut_menu,
            "semantic_type": semantic_type
    }


@register.inclusion_tag('common_tags/video_gallery.html')
def videos_gallery(videos):
    return {"videos": videos}


@register.inclusion_tag('common_tags/grid-list-gallery-menu.html')
def grid_list_gallery_menu():
    return {}


@register.inclusion_tag('common_tags/display_information_message.html', takes_context=True)
def display_information_message(context):
    expiration_date = datetime.today() + timedelta(days=365)
    cookie_date_format = "%a, %d %b %Y %I:%M:%S GMT"
    try:
        information_message = InformationMessage.objects.filter(
            active=True,
            display_date__lte=datetime.now(), expiration_date__gt=datetime.now()).latest('publish_date')
        request = context['request']
        if information_message.display_once:
            try:
                already_read_information_message_id = int(request.COOKIES.get('information_message_id'))
                if already_read_information_message_id == information_message.id:
                    information_message = None
            # Cookie not found
            except TypeError:
                pass
    except ObjectDoesNotExist:
        information_message = None
    return {"information_message": information_message, "expiration_date": expiration_date.strftime(cookie_date_format)}
