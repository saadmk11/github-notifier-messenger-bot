import hashlib
import hmac
import json

import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


@login_required
def list_user_repositories(request):
    url = 'https://api.github.com/users/{}/repos'.format(request.user.username)
    response = requests.get(url)

    if response.status_code == 200:
        context = {
            'repos': response.json()
        }
    else:
        context = {
            'repos': None
        }

    return render(request, 'github_bot/index.html', context)
