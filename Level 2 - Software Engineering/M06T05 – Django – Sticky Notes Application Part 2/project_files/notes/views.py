from django.shortcuts import render, get_object_or_404, redirect

from .models import Note
from .forms import NoteForm


def note_list(request):
    notes = Note.objects.all()
    context = {
        "notes": notes,
        "page_title": "Sticky Notes",
    }
    return render(request, "notes/note_list.html", context)


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form, "note": note})


def note_delete(request, pk):
    """Delete a sticky note after confirmation (UC5 - Delete a note).

    Reached from the trash can icon. A note is only deleted on POST, so
    simply visiting the URL (for example via a link or a web crawler)
    can never remove data.

    * **GET** - renders ``notes/note_confirm_delete.html`` asking the
      user to confirm. The detail page uses this, and so does the list
      page if the browser does not support the ``<dialog>`` pop-up.
    * **POST** - permanently deletes the note and redirects to the note
      list. The list page's pop-up sends this POST directly.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the note to delete, captured from the URL.

    Returns:
        HttpResponse: A redirect to ``note_list`` after deletion, or the
        rendered confirmation page with ``note`` in context.

    Raises:
        Http404: If no note with the given ``pk`` exists.
    """

    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})
