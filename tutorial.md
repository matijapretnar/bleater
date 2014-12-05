Django za začetnike
===================

Že z malo znanja HTML-ja, PHP-ja in podatkovnih baz lahko precej hitro
vzpostavimo osnovno spletno storitev, kot na primer spletna trgovina ali
učilnica. Težave nastanejo, ko naša storitev postane priljubljena med
uporabniki. Takrat nove razširitve vse težje dodajamo, ker postaja koda
nepregledna. Skrbi nas tudi, da ne bi kdo pred nami odkril kakšne varnostne
luknje in se okoristil s podatki uporabnikov. Poleg tega pa z večjim številom
uporabnikov vse skupaj postaja vedno počasnejše, mi pa ne vemo, kako bi storitev
prilagodili, da bi delovala na več kot enem strežniku hkrati.

Vsem tem težavam se lahko izognemo, če uporabimo ustrezno programsko ogrodje, ki
nam omogoča tako hitro postavitev osnovne storitve kot tudi dobro osnovo za
bodoče razširitve. Primer takega ogrodja je Django, ki ga bomo spoznali na
delavnici.

S pomočjo Djanga bomo razvili enostavno družabno omrežje _Bleater_, na katerem
na katerem bodo ovce blejale in sledile drugim ovcam. Omrežje bo nudila dve
strani:

1. Začetno stran, na kateri bo:
  * časovnica vseh blejanj,
  * seznam vseh ovc s povezavami na njihove strani.
2. Stran posamezne ovce, na kateri bo:
  * časovnica vseh njenih blejanj,
  * obrazec za objavo novega blejanja,
  * enostavna statistika o številu objav in sledenih ovc,
  * seznam sledenih ovc z gumbi za prenehanje sledenja,
  * seznam še nesledenih ovc z gumbi za začetek sledenja.


Postavitev projekta
-------------------

Predpostavimo, da je Django že nameščen. Sicer si pogledamo navodila na
https://www.djangoproject.com. Nato v primerni mapi ustvarimo projekt z ukazom

    django-admin startproject bleater

Poglejmo, kaj smo dobili:

* `manage.py` - skripta, s katero bomo nadzorovali projekt
* `bleater/` - mapa, v kateri so podatki o projektu
  * `__init__.py` - datoteka, ki Pythonu omogoča, da mapo vidi kot modul
  * `settings.py` - nastavitve projekta (zaenkrat jih ni treba spreminjati)
  * `urls.py` - povezava med URL naslovi ter kodo, ki jo pišemo
  * `wsgi.py` - program za zagon storitve na pravem strežniku (ne bomo rabili)

Nato z ukazom

    ./manage.py migrate

vzpostavimo bazo, z ukazom 

    ./manage.py runserver

pa zaženemo strežnik ter v brskalniku obiščemo stran http://127.0.0.1:8000/.
Kot vidimo iz pozdravnega sporočila, nas pravo delo šele čaka.


Postavitev aplikacije
---------------------

Vsak Django projekt je razdeljen na aplikacije, od katerih vsaka ponuja neko
osnovno funkcionalnost. Na dolgi rok bi bilo naš projekt dobro razdeliti na dve
aplikaciji: eno za ovce, drugo pa za njihova blejanja, vendar bomo zaradi
enostavnosti naredili le eno aplikacijo.

Zelo pogosto vključimo tudi zunanje aplikacije, ki skrbijo za lažjo
administracijo, samodejna opozorila na sprejem piškotkov in vse relevantne
zakone, prijavo prek zunanjih ponudnikov avtentikacije (Google, Facebook, …),
značke in podobno.

Z ukazom

    ./manage.py startapp bleats

ustvarimo aplikacijo `bleats` (interne aplikacije se splača poimenovati po
njihovem glavnem modelu (glej spodaj)). Nato v ustvarjeni mapi `bleats` naredimo
še prazno mapo z imenom `templates`. Poglejmo, kaj dobimo:

* `bleats/`
  * `migrations/`
  * `templates/`
  * `__init__.py`
  * `admin.py`
  * `models.py`
  * `tests.py`
  * `views.py`

Django je zasnovan na strogi ločitvi podatkov od njihovega prikaza uporabniku:
* Podatke predstavimo z modeli, opisanimi v datoteki `models.py`.
* Podatke prikažemo s spletnimi stranmi, ustvarjenimi iz predlog v mapi
  `templates/`.
* Modele in predloge med seboj povežemo s pogledi, opisanimi v datoteki
  `views.py`.

Poleg tega aplikacija vsebuje še nekaj pomožnih stvari:
* Datoteka `__init__.py` Pythonu omogoča, da mapo `bleats` vidi kot modul.
* V datoteki `admin.py` vklopimo enostaven administrativni vmesnik, ki je že
  vključen v Django.
* V datoteki `tests.py` lahko napišemo teste, ki preverjajo pravilnost delovanja
  naše aplikacije. Testov tokrat ne bomo pisali.
* Mapa `migrations/` vsebuje migracije, ki iz modelov ustvarijo tabele v
  podatkovni bazi. Vsakič, ko spremenimo predstavitev podatkov v modelu, moramo
  ustrezno spremeniti tudi bazo.

Aplikacijo registriramo tako, da v `bleater/settings.py` med `INSTALLED_APPS`
dodamo `bleats`.


Modeli
------

Najprej vedno definiramo modele. V datoteko `models.py` dodamo dva modela:
* `Sheep`, ki vsebuje podatke o kratkem in polnem imenu ovce ter ovcam, ki jim
  sledi,
* `Bleat`, ki vsebuje podatke o avtorju, sporočilu in času blejanja.

Nato ustvarimo in zaženemo migracije, ki pripravijo bazo:

    ./manage.py makemigrations
    ./manage.py migrate

Sedaj bi lahko s pomočjo ukazne vrstice, ki jo dobimo z `./manage.py shell`, že
začeli delati z bazo. Lažje pa je, če za to uporabimo administracijski vmesnik.

Zato v datoteki `admin.py` registriramo modela `Sheep` in `Bleat`, nato pa z
ukazom

    ./manage.py createsuperuser

ustvarimo prvega uporabnika. Potem gremo na naslov http://127.0.0.1:8000/admin,
se tam prijavimo in začnemo vpisovati testne podatke.


Predloge
--------

Na začetni strani bo glavni del zasedala časovnica vseh blejanj, na strani pa bo
seznam vseh ovc. Na strani posamezne ovce bo na sredini zopet časovnica vseh
blejanj, na strani pa podatki o statistiki in sledenih ovcah. Ker imata obe
strani podobno strukturo, bomo v mapi `templates/` najprej naredili predlogo
`base.html`, ki vsebuje osnovni HTML ter označeni mesti, v kateri bomo kasneje
postavili glavno in stransko vsebino.

Začetno stran opišemo s predlogo `homepage.html`, stran ovce pa s predlogo
`timeline.html`. Ker se na obeh straneh blejanja in naštete ovce prikazujejo na
enak način, bomo naredili še pomožni predlogi `bleat.html` in `sheep.html`, ki
ju bomo vključili v predlogi strani.


Pogledi
-------

Modele in predloge povežemo prek pogledov, opisanih v datoteki `views.py`. Vsak
pogled je funkcija, ki sprejme HTTP zahtevo in vrne odziv. Vsak pogled moramo
povezati tudi z naslovom, prek katerega bo dostopen. Naslove vpišemo v datoteko
`urls.py`.
