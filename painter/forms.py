from django import forms
from django.conf import settings


GENERATOR_CHOICES = [(g["key"], g["name"]) for g in settings.GENERATORS.values()]


class BoundFilePathField(forms.BoundField):
    """
    Django doesn't provide a field that allows you to select a file path using
    a file selection dialog. We can fake it using a CharField with a FileInput
    widget, but we need to override the BoundField instance as well so that
    the incoming value is still treated as text, not a file.
    """
    @property
    def data(self):
        return self.form._widget_data_value(forms.TextInput(), self.html_name)


class SelectGeneratorForm(forms.Form):
    generator = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENERATOR_CHOICES,
    )

    file_path = forms.CharField(
        widget=forms.FileInput,
        bound_field_class=BoundFilePathField,
    )
