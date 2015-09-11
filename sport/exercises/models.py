from django.db import models
from django.utils.translation import gettext_lazy as _

MUSCLE_TYPE = (('skeleton', _('Skeletal Striated Muscle')),
               ('smooth', _('Smooth Muscle')),
               ('cardiac', _('Cardiac Muscle')),)

DIFFICULTY = (('easy', _('Easy')),
              ('medium', _('Medium')),
              ('hard', _('Hard')))


class CommonsPagesAttributes(models.Model):
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=150)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Mapping(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='upload/exercises/mapping')
    alt = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class MappingArea(models.Model):
    name = models.CharField(max_length=150)
    points = models.TextField()
    mapping = models.ForeignKey(Mapping)
    image_over = models.ImageField(upload_to='upload/exercises/mapping', blank=True)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def __str__(self):
        return self.name


class MuscleType(models.Model):
    name = models.CharField(max_length=150, choices=MUSCLE_TYPE, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    group = models.ForeignKey(MuscleGroup, blank=True)
    type_of_muscle = models.ForeignKey(MuscleType)
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    muscles = models.ManyToManyField(Muscle)
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)
    common_page_attribute = models.ForeignKey(CommonsPagesAttributes)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    price = models.IntegerField(default=-1, blank=True)
    indoor = models.BooleanField(default=False)
    outdoor = models.BooleanField(default=False)
    public_facilities = models.BooleanField(default=False)
    gym_suit = models.BooleanField(default=False)
    comfort = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def is_indoor(self):
        return self.indoor
    is_indoor.boolean = True

    def is_outdoor(self):
        return self.outdoor
    is_outdoor.boolean = True

    def is_public_facilities(self):
        return self.public_facilities
    is_public_facilities.boolean = True

    def is_gym_suit(self):
        return self.gym_suit
    is_gym_suit.boolean = True

    def is_free(self):
        return True if self.price == -1 else False
    is_free.boolean = True

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    link_title = models.CharField(max_length=80, blank=True, default=_("See This Exercise"))
    category = models.ForeignKey(Category)
    muscles = models.ManyToManyField(Muscle)
    related_exercises = models.ManyToManyField('self', blank=True, default=None, null=True)
    level = models.CharField(max_length=15, choices=DIFFICULTY)
    equipments = models.ManyToManyField(Equipment, blank=True, default=None, null=True)
    active = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def __str__(self):
        return self.name

    def have_related_exercises(self):
        return False if not self.related_exercises.all() else True
    have_related_exercises.boolean = True


class Step(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    exercise = models.ForeignKey(Exercise)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='upload/exercises')
    alt = models.CharField(max_length=300)
    description = models.TextField()
    active = models.BooleanField(default=False)
    main = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MappingAreaMuscles(MappingArea):
    binding = models.ForeignKey(Muscle)


class ImageExercise(Image):
    binding = models.ForeignKey(Exercise)


class ImageMuscleGroup(Image):
    binding = models.ForeignKey(MuscleGroup)


class ImageMuscle(Image):
    binding = models.ForeignKey(Muscle)


class ImageCategory(Image):
    binding = models.ForeignKey(Category)


class ImageMuscleType(Image):
    binding = models.ForeignKey(MuscleType)


class ImageStep(Image):
    binding = models.ForeignKey(Step)


class ImageEquipment(Image):
    binding = models.ForeignKey(Equipment)


class Video(models.Model):
    name = models.CharField(max_length=300)
    embedded_url = models.URLField()
    origin_url = models.URLField(default="")
    thumbnail_url = models.URLField(default="")
    alt = models.CharField(max_length=300)
    description = models.TextField()
    player_width = models.IntegerField(default=550)
    player_height = models.IntegerField(default=350)
    youtube_id = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    main = models.BooleanField(default=False)
    duration = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class VideoExercise(Video):
    binding = models.ForeignKey(Exercise)


class VideoCategory(Video):
    binding = models.ForeignKey(Category)
