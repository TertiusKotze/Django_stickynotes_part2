"""Unit tests covering the use cases of the Sticky Notes application.

Use cases covered:
    UC1 - View all notes
    UC2 - View a single note
    UC3 - Create a note
    UC4 - Update a note
    UC5 - Delete a note
"""
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import NoteForm
from .models import Note


class NoteModelTests(TestCase):
    """Tests for the Note model."""

    def test_string_representation_returns_title(self):
        note = Note.objects.create(title="Sprint goals", content="Plan release")
        self.assertEqual(str(note), "Sprint goals")

    def test_created_at_is_set_automatically(self):
        note = Note.objects.create(title="Timestamp", content="Check")
        self.assertIsNotNone(note.created_at)

    def test_notes_ordered_newest_first(self):
        older = Note.objects.create(title="Older", content="a")
        newer = Note.objects.create(title="Newer", content="b")
        Note.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        self.assertEqual(list(Note.objects.all()), [newer, older])

    def test_title_max_length(self):
        self.assertEqual(Note._meta.get_field("title").max_length, 255)


class NoteFormTests(TestCase):
    """Tests for NoteForm validation."""

    def test_valid_form(self):
        form = NoteForm(data={"title": "Title", "content": "Body"})
        self.assertTrue(form.is_valid())

    def test_title_required(self):
        form = NoteForm(data={"title": "", "content": "Body"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_content_required(self):
        form = NoteForm(data={"title": "Title", "content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_title_too_long_is_invalid(self):
        form = NoteForm(data={"title": "x" * 256, "content": "Body"})
        self.assertFalse(form.is_valid())


class NoteListViewTests(TestCase):
    """UC1 - View all notes."""

    def test_empty_list(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertEqual(len(response.context["notes"]), 0)

    def test_list_displays_all_notes(self):
        Note.objects.create(title="First", content="1")
        Note.objects.create(title="Second", content="2")
        response = self.client.get(reverse("note_list"))
        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertEqual(len(response.context["notes"]), 2)

    def test_list_shows_trash_button_for_each_note(self):
        note = Note.objects.create(title="Bin me", content="x")
        response = self.client.get(reverse("note_list"))
        delete_url = reverse("note_delete", kwargs={"pk": note.pk})
        self.assertContains(response, 'class="trash-button"')
        self.assertContains(response, f'data-delete-url="{delete_url}"')

    def test_list_contains_delete_confirmation_popup(self):
        Note.objects.create(title="Popup", content="x")
        response = self.client.get(reverse("note_list"))
        self.assertContains(response, '<dialog id="delete-dialog"')
        self.assertContains(response, "csrfmiddlewaretoken")


class NoteDetailViewTests(TestCase):
    """UC2 - View a single note."""

    def setUp(self):
        self.note = Note.objects.create(title="Detail", content="Detail body")

    def test_detail_displays_note(self):
        response = self.client.get(
            reverse("note_detail", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_detail.html")
        self.assertContains(response, "Detail body")

    def test_detail_missing_note_returns_404(self):
        response = self.client.get(reverse("note_detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


class NoteCreateViewTests(TestCase):
    """UC3 - Create a note."""

    def test_get_shows_empty_form(self):
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_form.html")
        self.assertIsInstance(response.context["form"], NoteForm)

    def test_valid_post_creates_note_and_redirects(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "Created note", "content": "Created content"},
        )
        self.assertRedirects(response, reverse("note_list"))
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().title, "Created note")

    def test_invalid_post_does_not_create_note(self):
        response = self.client.post(
            reverse("note_create"), {"title": "", "content": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)


class NoteUpdateViewTests(TestCase):
    """UC4 - Update a note."""

    def setUp(self):
        self.note = Note.objects.create(title="Original", content="Original body")
        self.url = reverse("note_update", kwargs={"pk": self.note.pk})

    def test_get_shows_prefilled_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].instance, self.note)
        self.assertContains(response, "Original")

    def test_valid_post_updates_note(self):
        response = self.client.post(
            self.url, {"title": "Updated", "content": "Updated body"}
        )
        self.assertRedirects(response, reverse("note_list"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated")
        self.assertEqual(self.note.content, "Updated body")

    def test_invalid_post_does_not_update(self):
        response = self.client.post(self.url, {"title": "", "content": "x"})
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Original")

    def test_update_missing_note_returns_404(self):
        response = self.client.get(reverse("note_update", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


class NoteDeleteViewTests(TestCase):
    """UC5 - Delete a note."""

    def setUp(self):
        self.note = Note.objects.create(title="To delete", content="Bye")
        self.url = reverse("note_delete", kwargs={"pk": self.note.pk})

    def test_get_shows_confirmation_without_deleting(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_confirm_delete.html")
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_post_deletes_note_and_redirects(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("note_list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_delete_missing_note_returns_404(self):
        response = self.client.post(reverse("note_delete", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

