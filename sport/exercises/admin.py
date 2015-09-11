from django.contrib import admin
from exercises.models import Category
from exercises.models import CommonsPagesAttributes
from exercises.models import Equipment
from exercises.models import Exercise
from exercises.models import ImageExercise
from exercises.models import ImageEquipment
from exercises.models import ImageCategory
from exercises.models import ImageMuscle
from exercises.models import ImageMuscleGroup
from exercises.models import ImageStep
from exercises.models import MappingAreaMuscles
from exercises.models import Mapping
from exercises.models import MuscleGroup
from exercises.models import Muscle
from exercises.models import MuscleType
from exercises.models import Step
from exercises.models import VideoExercise
from exercises.models import VideoCategory


class CommonsPagesAttributesAdmin(admin.ModelAdmin):
    list_display = ('keywords', 'description')


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


class MappingAreaMusclesInline(admin.StackedInline):
    model = MappingAreaMuscles
    extra = 2


class VideoExerciseInline(admin.StackedInline):
    model = VideoExercise
    extra = 1


class VideoCategoryInline(admin.StackedInline):
    model = VideoCategory
    extra = 1


class StepAdminInline(admin.TabularInline):
    model = Step
    extra = 3
    inlines = [ImageStepInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [ImageCategoryInLine, VideoCategoryInline]


class ExerciseAdmin(admin.ModelAdmin):
    inlines = [StepAdminInline, ImageExerciseInLine, VideoExerciseInline]
    list_display = ('name', 'level', 'category', 'have_related_exercises')
    fieldsets = (
        ('General', {'fields': ('name', 'description', 'link_title', 'level', 'active', 'slug')}),
        ('Organisation', {'classes': ('collapse', ), 'fields': ('category', 'muscles', 'related_exercises')}),
        ('Extra', {'classes': ('collapse', ), 'fields': ('equipments', )})
    )
    list_filter = ['category', 'muscles', 'level', 'active']


class EquimentAdmin(admin.ModelAdmin):
    inlines = [ImageEquipmentInline]
    list_display = ('name', 'is_indoor', 'is_outdoor', 'is_public_facilities', 'is_free')


class MuscleAdmin(admin.ModelAdmin):
    inlines = [ImageMuscleInLine, MappingAreaMusclesInline]


class MuscleGroupAdmin(admin.ModelAdmin):
    inlines = [ImageMuscleGroupInLine]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Equipment, EquimentAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(MuscleType)
admin.site.register(Mapping)
admin.site.register(CommonsPagesAttributes, CommonsPagesAttributesAdmin)
