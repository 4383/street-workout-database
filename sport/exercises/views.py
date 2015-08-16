from django.shortcuts import render
from django.shortcuts import get_object_or_404
from exercises.models import Category
from exercises.models import Exercise
from exercises.models import ImageCategory
from exercises.models import ImageExercise
from exercises.models import ImageMuscle
from exercises.models import Muscle


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
    return render(request, "exercise.html")


def categories(request):
    actives_categories = Category.objects.filter(active=True)
    categories_list = []
    for active_category in actives_categories:
        category_data = {
            'category': active_category,
            'total_exercises': Exercise.objects.filter(category=active_category).count(),
            'random_selected_exercises': Exercise.objects.filter(category=active_category)[:10],
            'main_image': ImageCategory.objects.filter(active=True, main=True, binding=active_category)[0],
        }
        categories_list.append(category_data)

    context = {'categories': row_builder(categories_list),}
    return render(request, "categories.html", context)


def category(request, slug):
    current_category = get_object_or_404(Category, active=True, slug=slug)
    exercises = Exercise.objects.filter(active=True, category=current_category)
    images_category = ImageCategory.objects.filter(active=True, binding=current_category)
    actives_muscles = Muscle.objects.filter(id__in=current_category.muscles.all, active=True)
    exercises_list = []
    for active_exercise in exercises:
        try:
            exercises_data = {
                'exercise': active_exercise,
                'main_image': ImageExercise.objects.filter(active=True, main=True, binding=active_exercise)[0],
                }
        except IndexError:
            exercises_data = {
                'exercise': active_exercise,
                'main_image': None,
                }
        exercises_list.append(exercises_data)

    if actives_muscles:
        muscles_list = []
        for active_muscle in actives_muscles:
            try:
                muscles_data = {
                    'muscle': active_muscle,
                    'main_image': ImageMuscle.objects.filter(active=True, main=True, binding=active_muscle)[0],
                    }
            except IndexError:
                muscles_data = {
                    'muscle': active_muscle,
                    'main_image': None,
                    }
            muscles_list.append(muscles_data)

    context = {'category': current_category,
               'images_category': images_category,
               'exercises_list': exercises_list,
               'muscles_list': muscles_list, }
    return render(request, "category.html", context)


def muscles(request):
    return render(request, "muscles.html")


def muscle(request, slug):
    return render(request, "muscle.html")


def muscles_groups(request):
    return render(request, "muscles_groups.html")


def muscle_group(request, slug):
    return render(request, "muscle_group.html")
