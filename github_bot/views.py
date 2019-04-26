import hashlib
import hmac
import json

import requests

from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


def send_message(fb_id, message):
    if message:
        api_url = '{}/me/messages?access_token={}'.format(
            settings.FB_API_ENDPOINT, settings.FB_PAGE_ACCESS_TOKEN)
        msg = json.dumps(
            {
                "recipient": {"id": fb_id},
                "message": {"text": message}
            }
        )
        headers = {
            'Content-Type': 'application/json',
        }
        requests.post(api_url, headers=headers, data=msg)


class WebhookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != settings.FB_VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status_code=403)
        return HttpResponse(hub_challenge)

    def post(self, request, *args, **kwargs):
        event = request.META.get('HTTP_X_GITHUB_EVENT')
        print(event)
        msg = None

        if event == 'push':
            payload = json.loads(request.body)
            committer = payload['head_commit']['author']['username']
            message = payload['head_commit']['message']
            url = payload['head_commit']['url']
            repo = payload['repository']['html_url']
            msg = f'Push event on {repo} by {committer} url: {url} message: {message}'
        print(msg)
        # print(payload)

        send_message('FB_ID', msg)
        return HttpResponse("Success", status=200)
