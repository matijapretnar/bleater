from django.shortcuts import get_object_or_404, redirect, render

from bleats.models import Bleat, Sheep


def index(request):
    context = {
        'bleats': Bleat.objects.all(),
        'all_sheep': Sheep.objects.all()
    }
    return render(request, 'index.html', context)


def timeline(request, shortname):
    context = {
        'current_sheep': get_object_or_404(Sheep, shortname=shortname)
    }
    return render(request, 'timeline.html', context)


def create_bleat(request):
    if request.method == 'POST':
        author = get_object_or_404(Sheep, id=request.POST['author_id'])
        message = request.POST['message']
        author.bleat(message)
        return redirect(author)


def toggle_following(request):
    if request.method == 'POST':
        who = get_object_or_404(Sheep, id=request.POST['who_id'])
        whom = get_object_or_404(Sheep, id=request.POST['whom_id'])
        who.toggle_following(whom)
        return redirect(who)
