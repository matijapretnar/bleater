from datetime import datetime

from django.db import models
from django.utils.timezone import utc


class Bleat(models.Model):
    author = models.ForeignKey('bleats.Sheep', related_name='bleats')
    message = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return '@{}: {}'.format(self.author.shortname, self.message)

    def pretty_time(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        diff = now - self.time
        if diff.seconds < 60:
            return '{}s'.format(diff.seconds)
        elif diff.seconds < 3600:
            return '{}m'.format(diff.seconds // 60)
        elif diff.seconds < 86400:
            return '{}h'.format(diff.seconds // 3600)
        else:
            return '{:%-d %b}'.format(self.time)


class Sheep(models.Model):
    shortname = models.SlugField(unique=True)
    name = models.CharField(max_length=250)
    following = models.ManyToManyField('bleats.Sheep', related_name='followers', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'sheep'

    def __str__(self):
        return '{} (@{})'.format(self.name, self.shortname)

    @models.permalink
    def get_absolute_url(self):
        return ('timeline', [self.shortname])

    def timeline_bleats(self):
        my_bleats = self.bleats.all()
        following_bleats = Bleat.objects.filter(author__in=self.following.all())
        # Could also be done as:
        # following_bleats = Bleat.objects.filter(author__followers=self)
        return my_bleats | following_bleats

    def bleat(self, message):
        bleat = Bleat(author=self, message=message)
        bleat.save()

    def toggle_following(self, sheep):
        if self.following.filter(pk=sheep.pk).exists():
            self.following.remove(sheep)
        else:
            self.following.add(sheep)
        self.save()

    def recommendations(self):
        already_following = self.following.all()
        not_yet_following = Sheep.objects.exclude(
            pk__in=already_following
        ).exclude(
            id=self.id
        )
        recommendations = not_yet_following.filter(
            following__in=already_following
        )
        if recommendations:
            return set(recommendations)
        else:
            return set(not_yet_following)

