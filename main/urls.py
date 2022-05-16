'''
WSGI config for main(WoofyaAPIDashboard) project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
'''

import os

from django.contrib import admin
from django.core.wsgi import get_wsgi_application
from django.urls import path, include

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()

urlpatterns = [
    path('admin/', admin.site.urls),
]
