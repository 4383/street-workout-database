from django.shortcuts import render
from exercises.models import Exercise


# Create your views here.
def about(request):
    return render(request, "about.html")


def index(request):
    exercises_number = Exercise.objects.filter(active=True).count()
    context = {"exercises_number": exercises_number}
    return render(request, "index.html", context)


def page_not_found(request):
    return render(request, "page_not_found.html")


def server_error(request):
    return render(request, "server_error.html")
