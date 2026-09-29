"""URL routes for the Sticky Notes application.

This module maps URL paths to the view functions in ``notes/views.py``.
The project URLconf (``sticky_notes/urls.py``) includes it at the site
root, so the paths below are relative to ``/``.

Each route has a ``name`` so templates and views can build links with
``{% url 'name' %}`` or ``reverse('name')`` instead of hard-coding
paths. The ``<int:pk>`` converter captures the note's primary key from
the URL as an integer and passes it to the view as ``pk``.

Routes:
    * ``/``                    -> ``note_list``   - list all notes
    * ``/note/<pk>/``          -> ``note_detail`` - view one note
    * ``/note/new/``           -> ``note_create`` - create a note
    * ``/note/<pk>/edit/``     -> ``note_update`` - edit a note (pencil)
    * ``/note/<pk>/delete/``   -> ``note_delete`` - delete a note (trash)
"""
from django.urls import path
from .views import note_list, note_detail, note_create, note_update, note_delete

urlpatterns = [
    path('', note_list, name='note_list'),
    path('note/<int:pk>/', note_detail, name='note_detail'),
    path('note/new/', note_create, name='note_create'),
    path('note/<int:pk>/edit/', note_update, name='note_update'),
    path('note/<int:pk>/delete/', note_delete, name='note_delete'),
]

