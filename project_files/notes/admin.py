"""Django admin configuration for the Sticky Notes application.

Registering the ``Note`` model with the admin site makes notes available
at ``/admin/``. There, a superuser (created with
``python manage.py createsuperuser``) can list, add, edit and delete
notes through Django's built-in interface, which is useful for managing
data outside the main application pages.
"""
from django.contrib import admin
from .models import Note

admin.site.register(Note)
