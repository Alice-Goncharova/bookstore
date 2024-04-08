"""
WSGI config for booking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking.settings')

application = get_wsgi_application()

path = '/home/Alice1995/warehouse/bookstore.pythonanywhere.com'
if path not in sys.path:
    sys.path.append(path)