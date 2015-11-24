from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from home import views as home_view
from exercises import views as exercises_view

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^exercises/", include('exercises.urls')),
    url(r"^/$", home_view.index, name="index"),
    url(r"^$", home_view.index, name="index"),
    url(r"^about/$", home_view.about, name="about"),
    url(r"^about$", home_view.about, name="about"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
