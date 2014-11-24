# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bleat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=140)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sheep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('shortname', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=250)),
                ('following', models.ManyToManyField(to='bleats.Sheep', blank=True, related_name='followers')),
            ],
            options={
                'verbose_name_plural': 'sheep',
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bleat',
            name='author',
            field=models.ForeignKey(related_name='bleats', to='bleats.Sheep'),
            preserve_default=True,
        ),
    ]
