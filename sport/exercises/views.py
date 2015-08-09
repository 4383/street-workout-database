from django.shortcuts import render
from exercises.models import Category
from exercises.models import ImageCategory
from exercises.models import Exercise


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


def categories(request):
    active_categories = Category.objects.filter(active=True)
    categories_list = []
    for active_category in active_categories:
        category_data = {
            'category': active_category,
            'total_exercises': Exercise.objects.filter(category=active_category).count(),
            'random_selected_exercises': Exercise.objects.filter(category=active_category)[:10],
            'main_image': ImageCategory.objects.filter(active=True, main=True, binding=active_category)[0],
        }
        print(category_data)
        categories_list.append(category_data)

    #images = ImageCategory.objects.filter(active=True, main=True)
    #exercises = Exercise.objects.filter(category__in=active_categories, active=True).order_by('-id', 'category')
    context = {'categories': active_categories,
               'categories_in_row': row_builder(categories_list),
               #'categories_in_row': row_builder(active_categories),
               #'images': images,
               #'exercises': exercises
               }
    return render(request, "categories.html", context)


def category(request, slug):
    return render(request, "category.html")


def exercise(request, slug):
    return render(request, "exercise.html")
