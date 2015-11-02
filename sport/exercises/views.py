from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import json
from django.conf import settings
from exercises.models import Category
from exercises.models import Exercise
from exercises.models import ExerciseSet
from exercises.models import ImageCategory
from exercises.models import ImageExercise
from exercises.models import ImageMuscle
from exercises.models import Mapping
from exercises.models import MappingAreaMuscles
from exercises.models import Muscle
from exercises.models import VideoCategory
from exercises.models import VideoExercise


def get_full_exercises_representation_for_a_category(current_category, limit=None):
    if limit:
        exercises = Exercise.objects.filter(active=True, category=current_category)[:limit]
    else:
        exercises = Exercise.objects.filter(active=True, category=current_category)
    exercises_list = []
    for active_exercise in exercises:
        try:
            exercises_data = {
                'information': active_exercise,
                'main_image': ImageExercise.objects.filter(active=True, main=True, binding=active_exercise)[0],
                }
        except IndexError:
            exercises_data = {
                'information': active_exercise,
                'main_image': None,
                }
        exercises_list.append(exercises_data)
    return exercises_list


def retrieve_all_muscles_information(specified_object, limit=None):
    if limit:
        actives_muscles = Muscle.objects.filter(id__in=specified_object.muscles.all, active=True)[:limit]
    else:
        actives_muscles = Muscle.objects.filter(id__in=specified_object.muscles.all, active=True)

    if actives_muscles:
        muscles_list = []
        for active_muscle in actives_muscles:
            try:
                muscles_data = {
                    'muscle': active_muscle,
                    'area': MappingAreaMuscles.objects.filter(binding=active_muscle),
                    'main_image': ImageMuscle.objects.filter(active=True, main=True, binding=active_muscle)[0],
                    }
            except IndexError:
                muscles_data = {
                    'muscle': active_muscle,
                    'area': MappingAreaMuscles.objects.filter(binding=active_muscle),
                    'main_image': None,
                    }
            muscles_list.append(muscles_data)
    return muscles_list


# Helper
def row_builder(items, maximum=3):
    row = []
    columns = []
    current_index = 0
    for item in items:
        if current_index == maximum:
            row.append(columns)
            columns = []
            current_index = 0
        columns.append(item)
        current_index += 1
    if columns:
        row.append(columns)
    return row


def exercise(request, slug):
    current_exercise = get_object_or_404(Exercise, active=True, slug=slug)
    try:
        main_image = ImageExercise.objects.filter(active=True, binding=current_exercise, main=True)[0]
    except IndexError:
        main_image = None
    try:
        main_exercise_set = ExerciseSet.objects.filter(how_to__active=True,
                                                       how_to__exercise=current_exercise, how_to__main=True)
    except IndexError:
        main_exercise_set = None

    if current_exercise.have_related_exercises():
        related_exercises_image = ImageExercise.objects.filter(active=True,
                                                               binding__in=current_exercise.related_exercises.all())

    context = {'exercise': current_exercise,
               'main_image': main_image,
               'main_exercise_set': main_exercise_set,
               'related_exercises_image': related_exercises_image}
    return render(request, "exercises/exercise.html", context)


def exercise_images(request, slug):
    current_exercise = get_object_or_404(Exercise, active=True, slug=slug)
    images = ImageExercise.objects.filter(active=True, binding=current_exercise)
    if len(images) < 1:
        return redirect('exercise', slug=slug)
    context = {'exercise': current_exercise, 'images': images}
    return render(request, "exercises/exercise_images.html", context)


def exercise_videos(request, slug):
    current_exercise = get_object_or_404(Exercise, active=True, slug=slug)
    videos = VideoExercise.objects.filter(active=True, binding=current_exercise)
    if len(videos) < 1:
        return redirect('exercise', slug=slug)
    context = {'exercise': current_exercise, 'videos': videos}
    return render(request, "exercises/exercise_videos.html", context)


def categories(request):
    actives_categories = Category.objects.filter(active=True)
    categories_list = []
    for active_category in actives_categories:
        try:
            category_data = {
                'information': active_category,
                'total_exercises': Exercise.objects.filter(category=active_category).count(),
                'random_selected_exercises': Exercise.objects.filter(category=active_category)[:3],
                'main_image': ImageCategory.objects.filter(active=True, main=True, binding=active_category)[0],
            }
        except IndexError:
            category_data = {
                'information': active_category,
                'total_exercises': Exercise.objects.filter(category=active_category).count(),
                'random_selected_exercises': Exercise.objects.filter(category=active_category)[:3],
                'main_image': None,
            }
        categories_list.append(category_data)

    context = {'categories': categories_list, }
    return render(request, "categories/categories.html", context)


def category(request, slug):
    current_category = get_object_or_404(Category, active=True, slug=slug)
    try:
        main_image = ImageCategory.objects.filter(active=True, binding=current_category, main=True)[0]
    except IndexError:
        main_image = None
    try:
        main_video = VideoCategory.objects.filter(active=True, binding=current_category, main=True)[0]
    except IndexError:
        main_video = None

    context = {'category': current_category,
               'main_image': main_image,
               'exercises_list': get_full_exercises_representation_for_a_category(current_category),
               'main_video': main_video,}
    return render(request, "categories/category.html", context)


def category_exercises(request, slug):
    current_category = get_object_or_404(Category, active=True, slug=slug)
    context = {'category': current_category,
               'exercises_list': get_full_exercises_representation_for_a_category(current_category)}
    return render(request, "categories/category_exercises.html", context)


def category_images(request, slug):
    current_category = get_object_or_404(Category, active=True, slug=slug)
    images = ImageCategory.objects.filter(active=True, binding=current_category)
    context = {'category': current_category,
               'images': images, }
    return render(request, "categories/category_images.html", context)


def category_videos(request, slug):
    current_category = get_object_or_404(Category, active=True, slug=slug)
    videos = VideoCategory.objects.filter(active=True, binding=current_category)
    context = {'category': current_category,
               'videos': videos, }
    return render(request, "categories/category_videos.html", context)


def muscles(request):
    actives_muscles = Muscle.objects.filter(active=True)
    if not actives_muscles:
        return

    try:
        mapping = Mapping.objects.get(name="main_muscle_mapping")
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

    context = {"muscles_list": muscles_list,
            "mapping": mapping,
            "json_data": json.dumps(json_data),
            "reverse_json_data": reverse_json_data}

    return render(request, "muscles/muscles.html", context)


def muscle(request, slug):
    return render(request, "muscle.html")


def muscles_groups(request):
    return render(request, "muscles_groups.html")


def muscle_group(request, slug):
    return render(request, "muscle_group.html")
