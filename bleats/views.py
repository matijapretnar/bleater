from django.shortcuts import get_object_or_404, redirect, render

from bleats.models import Bleat, Sheep


def homepage(request):
    '''Začetna stran, ki prikazuje seznam vseh ovc ter njihovih blejanj.'''
    # Za izris enostavnih strani uporabimo bližnjico render, ki sprejme HTTP
    # zahtevo, ime predloge ter kontekst, ki je slovar, v katerem podamo vse
    # spremenljivke, ki jih bomo uporabili pri izrisu predloge. V našem primeru
    # so to podatki o vseh ovcah in njihovih blejanjih.
    context = {
        'bleats': Bleat.objects.all(),
        'all_sheep': Sheep.objects.all()
    }
    return render(request, 'homepage.html', context)


def timeline(request, shortname):
    '''Časovnica dane ovce, na kateri vidimo njena blejanja ter statistiko.'''
    # Uporabimo bližnjico get_object_or_404, ki vrne iskano ovco v primeru, da
    # ta obstaja, sicer pa sproži HTTP napako 404, ki pomeni, da dana spletna
    # stran ne obstaja.
    context = {
        'current_sheep': get_object_or_404(Sheep, shortname=shortname)
    }
    return render(request, 'timeline.html', context)


def create_bleat(request):
    '''Naslov, na katerega pošljemo zahtevo za novo blejanje.'''
    # Blejanje dodamo le v primeru, da smo stran obiskali z metodo POST, torej
    # prek oddaje spletnega obrazca.
    if request.method == 'POST':
        author = get_object_or_404(Sheep, id=request.POST['author_id'])
        message = request.POST['message']
        author.bleat(message)
        # Po uspešni objavi brskalnik preusmerimo nazaj na časovnico avtorja
        # blejanja. To pomeni, da ob morebitni osvežitvi strani spročilo ne bi
        # bilo oddano dvakrat. Bližnjica redirect načeloma sprejme ime pogleda,
        # na katerega naj preusmeri brskalnik, lahko pa mu podamo tudi model. V
        # tem primeru se preusmeri na pogled, podan v metodi get_absolute_url.
        return redirect(author)


def toggle_following(request):
    '''Naslov, na katerega pošljemo zahtevo za spremembo sledenja.'''
    # Zgradba pogleda je podobna kot pri pogledu create_bleat.
    if request.method == 'POST':
        who = get_object_or_404(Sheep, id=request.POST['who_id'])
        whom = get_object_or_404(Sheep, id=request.POST['whom_id'])
        who.toggle_following(whom)
        return redirect(who)
