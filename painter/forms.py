from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import CachedFilePath


# We need a rogue value for the custom path selection that's not actually None.
EMPTY_OLD_PATH_VALUE = "-"
EMPTY_OLD_PATH_CHOICE = (EMPTY_OLD_PATH_VALUE, "Enter a new path")



class SelectFileForm(forms.Form):
    def __init__(self, *args, generator_key, **kwargs):
        super().__init__(*args, **kwargs)

        self.generator_key = generator_key
        self.fields["old_file_path"].choices = self._get_cached_paths(generator_key)
        self.fields["new_file_path"].validators = [self._validate_xlsx_path]

    def _validate_xlsx_path(self, file_path):
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
        
        CachedFilePath.objects.update_or_create(path=file_path, defaults={"generator_key": self.generator_key})

    def _get_cached_paths(self, generator_key):
        paths = CachedFilePath.objects.filter(generator_key=generator_key)
        paths = [(path.path, str(path)) for path in paths]
        return [EMPTY_OLD_PATH_CHOICE, *paths]

    old_file_path = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[EMPTY_OLD_PATH_CHOICE],
        label="Choose a previous file...",
        label_suffix="",
    )

    new_file_path = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="...or enter a new file path (.xlsx)",
        label_suffix="",
    )
