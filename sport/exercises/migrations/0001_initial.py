# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=-1, blank=True)),
                ('indoor', models.BooleanField(default=False)),
                ('outdoor', models.BooleanField(default=False)),
                ('public_facilities', models.BooleanField(default=False)),
                ('gym_suit', models.BooleanField(default=False)),
                ('comfort', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
                ('link_title', models.CharField(default='See This Exercise', max_length=80, blank=True)),
                ('level', models.CharField(max_length=15, choices=[(b'easy', 'Easy'), (b'medium', 'Medium'), (b'hard', 'Hard')])),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='exercises.Category')),
                ('equipments', models.ManyToManyField(default=None, to='exercises.Equipment', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to=b'')),
                ('alt', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('main', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MuscleGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MuscleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150, choices=[(b'skeleton', 'Skeletal Striated Muscle'), (b'smooth', 'Smooth Muscle'), (b'cardiac', 'Cardiac Muscle')])),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=300)),
                ('description', models.TextField()),
                ('exercise', models.ForeignKey(to='exercises.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('url', models.URLField()),
                ('alt', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('main', models.BooleanField(default=False)),
                ('player_height', models.IntegerField()),
                ('player_width', models.IntegerField()),
                ('youtube_id', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageEquipment',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
                ('binding', models.ForeignKey(to='exercises.Equipment')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageExercise',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageMuscle',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageMuscleGroup',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
                ('binding', models.ForeignKey(to='exercises.MuscleGroup')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageMuscleType',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
                ('binding', models.ForeignKey(to='exercises.MuscleType')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='ImageStep',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Image')),
                ('binding', models.ForeignKey(to='exercises.Step')),
            ],
            bases=('exercises.image',),
        ),
        migrations.CreateModel(
            name='VideoExercise',
            fields=[
                ('video_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exercises.Video')),
            ],
            bases=('exercises.video',),
        ),
        migrations.AddField(
            model_name='muscle',
            name='group',
            field=models.ForeignKey(to='exercises.MuscleGroup', blank=True),
        ),
        migrations.AddField(
            model_name='muscle',
            name='type_of_muscle',
            field=models.ForeignKey(to='exercises.MuscleType'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscles',
            field=models.ManyToManyField(to='exercises.Muscle'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='related_exercises',
            field=models.ManyToManyField(default=None, related_name='related_exercises_rel_+', null=True, to='exercises.Exercise', blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='muscles',
            field=models.ManyToManyField(to='exercises.Muscle'),
        ),
        migrations.AddField(
            model_name='videoexercise',
            name='binding',
            field=models.ForeignKey(to='exercises.Exercise'),
        ),
        migrations.AddField(
            model_name='imagemuscle',
            name='binding',
            field=models.ForeignKey(to='exercises.Muscle'),
        ),
        migrations.AddField(
            model_name='imageexercise',
            name='binding',
            field=models.ForeignKey(to='exercises.Exercise'),
        ),
        migrations.AddField(
            model_name='imagecategory',
            name='binding',
            field=models.ForeignKey(to='exercises.Category'),
        ),
    ]
