from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
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
