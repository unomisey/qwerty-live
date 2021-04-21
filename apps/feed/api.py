import json
import re

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.notifications.utilities import create_notification

from django.contrib.auth.models import User


from .models import Qwert, Like


@login_required
def api_add_qwert(request):
    data = json.loads(request.body)
    body = data['body']

    qwert = Qwert.objects.create(body=body, created_by=request.user)

    results = re.findall("(^|[^@\w])@(\w{1,20})", body)

    for result in results:
        result = result[1]

        print(result)

        if User.objects.filter(username=result).exists() and result != request.user.username:
            create_notification(request, User.objects.get(username=result), 'mention')



    return JsonResponse({'success': True})


@login_required
def api_add_like(request):
    data = json.loads(request.body)
    qwert_id = data['qwert_id']

    if not Like.objects.filter(qwert_id=qwert_id).filter(created_by=request.user).exists():
        like = Like.objects.create(qwert_id=qwert_id, created_by=request.user)
        qwert = Qwert.objects.get(pk=qwert_id)
        create_notification(request, qwert.created_by, 'like')

    return JsonResponse({'success': True})
