from django.shortcuts import render
from models import Category


def categories(request):
    active_categories = Category.objects.filter(active=True)
    context = {'categories': active_categories}
    return render(request, "categories.html", context)


def category(request, name):
    return render(request, "category.html")


def exercise(request, name):
    return render(request, "exercise.html")
