"""Database models for the Sticky Notes application.

This module defines the app's data layer. Django's ORM maps each model
class to a database table (here SQLite, stored in ``db.sqlite3``) and
each attribute to a column. After changing a model, run
``python manage.py makemigrations`` and ``python manage.py migrate`` to
keep the database schema in sync.

Models:
    * ``Note`` - a single sticky note with a title, body text and the
      time it was created.
"""
from django.db import models


class Note(models.Model):
    """A single sticky note created by the user.

    Each note is stored as one row in the ``notes_note`` table. Django
    automatically adds an integer primary key ``id`` (also available as
    ``pk``), which the URLs use to identify a note, e.g.
    ``/note/3/edit/``.

    Attributes:
        title (CharField): A short heading for the note. Required and
            limited to 255 characters.
        content (TextField): The main body of the note. Required, with
            no length limit.
        created_at (DateTimeField): The date and time the note was
            first saved. Set automatically on creation
            (``auto_now_add=True``) and not changed by later edits.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model-level options for ``Note``.

        * ``ordering`` - querysets return the newest notes first, so the
          most recent note always appears at the top of the list page.
        * ``verbose_name`` / ``verbose_name_plural`` - human-readable
          names shown in the Django admin site.
        """

        ordering = ["-created_at"]
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        """Return the note's title as its string representation.

        Used wherever a note is converted to text, such as the Django
        admin list and the interactive shell.

        Returns:
            str: The title of the note.
        """
        return self.title
