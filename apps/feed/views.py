from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.notifications.utilities import create_notification


from .models import Qwert


@login_required
def feed(request):
    userids = [request.user.id]
    #
    for qwerter in request.user.qwertyprofile.follows.all():
        userids.append(qwerter.user.id)
    #
    qwerts = Qwert.objects.filter(created_by_id__in=userids)
    #
    for qwert in qwerts:
        likes = qwert.likes.filter(created_by_id=request.user.id)
    #
        if likes.count() > 0:
            qwert.liked = True
        else:
            qwert.liked = False

    return render(request, 'feed/feed.html', {'qwerts': qwerts})


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        qwerters = User.objects.filter(username__icontains=query)
        qwerts = Qwert.objects.filter(body__icontains=query)
    else:
        qwerters = []
        qwerts = []

    context = {
        'query': query,
        'qwerters': qwerters,
        'qwerts': qwerts
    }

    return render(request, 'feed/search.html', context)