# from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QwerterProfileForm
from apps.notifications.utilities import create_notification

def qwerterprofile(request, username):
    user = get_object_or_404(User, username=username)
    qwerts = user.qwerts.all()

    for qwert in qwerts:
        likes = qwert.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            qwert.liked = True
        else:
            qwert.liked = False

    context = {
        'user': user,
        'qwerts': qwerts,
    }

    return render(request, 'qwertyprofile/qwerterprofile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = QwerterProfileForm(request.POST, request.FILES, instance=request.user.qwertyprofile)

        if form.is_valid():
            form.save()

            return redirect('qwerterprofile', username=request.user.username)
    else:
        form = QwerterProfileForm(instance=request.user.qwertyprofile)

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'qwertyprofile/edit_profile.html', context)



@login_required
def follow_qwerter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.qwertyprofile.follows.add(user.qwertyprofile)

    create_notification(request, user, 'follower')

    return redirect('qwerterprofile', username=username)

@login_required
def unfollow_qwerter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.qwertyprofile.follows.remove(user.qwertyprofile)

    return redirect('qwerterprofile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'qwertyprofile/followers.html', {'user': user})

def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'qwertyprofile/follows.html', {'user': user})
