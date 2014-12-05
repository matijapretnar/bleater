from django.contrib import admin

from bleats.models import Bleat, Sheep


# S spodnjima dvema vrsticama v administrativnem vmesniku vklopimo urejanje
# modelov Bleat in Sheep. Da to lahko storimo, moramo prej z zgornjima dvema
# vrsticama uvoziti paket za administracijo in omenjena modela.
admin.site.register(Bleat)
admin.site.register(Sheep)
