from datetime import datetime

from django.db import models
from django.utils.timezone import utc


class Sheep(models.Model):
    shortname = models.SlugField(unique=True)
    name = models.CharField(max_length=250)
    following = models.ManyToManyField('bleats.Sheep', blank=True,
                                       related_name='followers')

    # V posebnem podrazredu Meta opišemo dodatne lastnosti modela. Vse možnosti
    # so opisane na https://docs.djangoproject.com/en/1.7/ref/models/options/.
    class Meta:
        # Naravna ureditev blejanj je padajoče po času.
        ordering = ['name']
        # Množina od sheep je sheep (uporablja se v administrativnem vmesniku).
        verbose_name_plural = 'sheep'

    # Z metodo __str__ podamo prijaznejšo predstavitev objektov razreda Sheep,
    # sicer bi se vsi prikazovali kot <Sheep: Sheep object>.
    def __str__(self):
        return '{} (@{})'.format(self.name, self.shortname)

    # Z metodo get_absolute_url podamo osnovno stran, ki jo uporabimo za prikaz
    # modela. V našem primeru bo to časovnica ovce.
    def get_absolute_url(self):
        return ('timeline', [self.shortname])

    # Novo blejanje sicer res ustvarimo v dveh vrsticah, vendar vseeno raje
    # napišemo metodo, ki jo kasneje lahko tudi razširjamo. Objekt naredimo
    # tako, kot bi ga običajno v Pythonu, z metodo save pa ga zapišemo v bazo.
    def bleat(self, message):
        '''Ustvari novo blejanje dane ovce.'''
        bleat = Bleat(author=self, message=message)
        bleat.save()

    def timeline_bleats(self):
        '''Vrne vsa blejanja dane ovce in vseh tistih ovc, ki jim sledi.'''
        my_bleats = self.bleats.all()
        following_bleats = Bleat.objects.filter(author__followers=self)
        return my_bleats | following_bleats

    def toggle_following(self, sheep):
        '''Spremeni sledenje dane ovce drugi ovci.'''
        if self.following.filter(pk=sheep.pk).exists():
            self.following.remove(sheep)
        else:
            self.following.add(sheep)
        self.save()

    def recommendations(self):
        '''Vrne seznam ovc, ki bi jim dana ovca lahko sledila.

        Najprej predlagamo vse tiste ovce, ki jim sledijo sledene ovce dane
        ovce. Če teh ni, predlagamo vse ovce, ki jim dana ovca še ne sledi.
        '''
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


class Bleat(models.Model):
    author = models.ForeignKey('bleats.Sheep', related_name='bleats')
    message = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return '@{}: {}'.format(self.author.shortname, self.message)

    def pretty_time(self):
        '''Prikaže čas blejanja v enostavni obliki.'''
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
