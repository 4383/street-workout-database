from django.contrib import admin
from models import Category
from models import Equipment
from models import Exercise
from models import ImageExercise
from models import ImageEquipment
from models import ImageCategory
from models import ImageMuscle
from models import ImageMuscleGroup
from models import ImageStep
from models import MuscleGroup
from models import Muscle
from models import MuscleType
from models import Step
from models import VideoExercise


class ImageCategoryInLine(admin.StackedInline):
    model = ImageCategory
    extra = 2


class ImageExerciseInLine(admin.TabularInline):
    model = ImageExercise
    extra = 2


class ImageMuscleInLine(admin.StackedInline):
    model = ImageMuscle
    extra = 2


class ImageMuscleGroupInLine(admin.StackedInline):
    model = ImageMuscleGroup
    extra = 2


class ImageStepInline(admin.StackedInline):
    model = ImageStep
    extra = 1


class ImageEquipmentInline(admin.StackedInline):
    model = ImageEquipment
    extra = 1


class VideoExerciseInline(admin.StackedInline):
    model = VideoExercise
    extra = 1


class StepAdminInline(admin.TabularInline):
    model = Step
    extra = 3
    inlines = [ImageStepInline]


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageCategoryInLine]


class ExerciseAdmin(admin.ModelAdmin):
    inlines = [StepAdminInline, ImageExerciseInLine, VideoExerciseInline]
    list_display = ('name', 'level', 'category', 'have_related_exercises')
    fieldsets = (
        ('General', {'fields': ('name', 'description', 'link_title', 'level', 'active')}),
        ('Organisation', {'classes': ('collapse', ), 'fields': ('category', 'muscles', 'related_exercises')}),
        ('Extra', {'classes': ('collapse', ), 'fields': ('equipments', )})
    )
    list_filter = ['category', 'muscles', 'level', 'active']


class EquimentAdmin(admin.ModelAdmin):
    inlines = [ImageEquipmentInline]
    list_display = ('name', 'is_indoor', 'is_outdoor', 'is_public_facilities', 'is_free')


class MuscleAdmin(admin.ModelAdmin):
    inlines = [ImageMuscleInLine]


class MuscleGroupAdmin(admin.ModelAdmin):
    inlines = [ImageMuscleGroupInLine]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Equipment, EquimentAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(MuscleType)
