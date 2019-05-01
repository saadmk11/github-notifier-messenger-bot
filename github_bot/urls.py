from django.conf.urls import url

from .views import WebhookView, list_user_repositories


urlpatterns = [
    url(r'^$', list_user_repositories, name='index'),
]
