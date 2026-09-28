"""Forms for the Sticky Notes application.

This module defines the HTML form used to create and edit notes. Because
``NoteForm`` is a ``ModelForm``, Django builds its fields and validation
rules directly from the ``Note`` model, so the form and the database
stay consistent (for example, the 255-character limit on ``title``).

The same form class is used by two views:
    * ``note_create`` - an empty form for a new note.
    * ``note_update`` - a form bound to an existing note via
      ``instance=note`` so its fields are pre-filled.
"""
from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """Form for entering or editing a note's title and content.

    Only ``title`` and ``content`` are shown to the user.
    ``created_at`` is deliberately left out because it is set
    automatically when a note is first saved.

    Validation (inherited from the model):
        * ``title`` is required and must be at most 255 characters.
        * ``content`` is required.

    If validation fails, ``form.errors`` holds the messages, which the
    ``note_form.html`` template displays to the user.
    """

    class Meta:
        """Configuration linking the form to the ``Note`` model.

        * ``model`` - the model the form creates or updates.
        * ``fields`` - the model fields shown on the form.
        * ``widgets`` - custom HTML inputs: a single-line text box with a
          placeholder and a browser-side ``maxlength`` for the title, and
          a six-row textarea with a placeholder for the content.
        """

        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter a short title",
                    "maxlength": "255",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Write your sticky note content",
                }
            ),
        }
