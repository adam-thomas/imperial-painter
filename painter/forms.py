from django import forms
from django.conf import settings


GENERATOR_CHOICES = [(g["key"], g["name"]) for g in settings.GENERATORS.values()]

class SelectGeneratorForm(forms.Form):
    file_path = forms.FilePathField(path=settings.BASE_DIR)
    generator = forms.ChoiceField(choices=GENERATOR_CHOICES)
