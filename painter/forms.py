from pathlib import Path

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import CachedFilePath


GENERATOR_CHOICES = [(g["key"], g["name"]) for g in settings.GENERATORS.values()]
EMPTY_OLD_PATH_VALUE = "-"


def validate_xlsx_path(file_path):
    """
    For a nonempty path, check that it file path leads to a file that
    actually exists, and has the correct extension.
    
    If the path is considered valid, cache it in the database.
    """
    if file_path is None:
        return

    file_object = Path(file_path)
    if not file_object.is_file():
        raise ValidationError(f"Could not find a file at: {file_path}")
    if file_object.suffix != ".xlsx":
        raise ValidationError(f"Please supply a path to an .xlsx file.")
    
    CachedFilePath.objects.update_or_create(path=file_path)


def get_cached_paths():
    paths = CachedFilePath.objects.values_list("path", flat=True)
    paths = [(path, path) for path in paths]
    return [(EMPTY_OLD_PATH_VALUE, "Enter a new path"), *paths]


class SelectGeneratorForm(forms.Form):
    generator = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENERATOR_CHOICES,
        label="Select a generator",
        label_suffix="",
    )

    old_file_path = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=get_cached_paths,
        label="Choose a previous file...",
        label_suffix="",
    )

    new_file_path = forms.CharField(
        required=False,
        label="...or enter a new file path (.xlsx)",
        label_suffix="",
        validators=[validate_xlsx_path],
    )
