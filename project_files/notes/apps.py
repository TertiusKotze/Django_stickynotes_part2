"""Application configuration for the ``notes`` app.

Django loads this configuration because the app is listed in
``INSTALLED_APPS`` in ``sticky_notes/settings.py``. It tells Django the
app's import name and which primary key type to use for its models.
"""
from django.apps import AppConfig


class NotesConfig(AppConfig):
    """Configuration class for the Sticky Notes ``notes`` app.

    Attributes:
        default_auto_field (str): The field type Django uses for the
            automatic primary key of models that don't define one.
            ``AutoField`` is an auto-incrementing integer.
        name (str): The Python import path of the app (``notes``).
    """

    default_auto_field = 'django.db.models.AutoField'
    name = 'notes'
