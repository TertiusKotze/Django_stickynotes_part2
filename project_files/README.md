# Sticky Notes (Django Part 1)

A Django CRUD application for creating, viewing, editing, and deleting sticky notes.

## Project Structure

- `manage.py`
- `sticky_notes/` - project settings, root URLs, and WSGI/ASGI config.
- `notes/` - app containing model, form, views, URLs, templates, static files, and tests.
- `research_answers.md` - theory section responses.
- `sticky_notes_design_diagrams.md` - UML diagrams in PlantUML syntax.

## Requirements

- Python 3.12+ (or similar modern Python 3 version)
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Run Tests

```bash
python manage.py test
```

## Notes

- Static files are configured in `sticky_notes/settings.py`.
- The `venv/` and `.venv/` folders are not part of submission.

