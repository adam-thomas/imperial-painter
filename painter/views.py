import base64
import importlib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView

from . import models
from .forms import SelectGeneratorForm, EMPTY_OLD_PATH_VALUE


class Home(FormView):
    template_name = "painter/_core/home.html"
    form_class = SelectGeneratorForm

    def form_valid(self, form):
        generator_key = form.cleaned_data["generator"]
        file_path = form.cleaned_data["old_file_path"]
        if file_path == EMPTY_OLD_PATH_VALUE:
            file_path = form.cleaned_data["new_file_path"]

        # Encode the file path into base64 so it can be safely passed in the URL
        # (without having to deal with multiple layers of URL encoding).
        b64_file_path = base64.b64encode(file_path.encode("utf-8")).decode("ascii")
        return HttpResponseRedirect(f"/{generator_key}/{b64_file_path}")


class CardDisplay(ListView):
    model = models.Card
    template_name = "painter/_core/card_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["generator"] = self.generator_key
        return context

    def load_importer_class(self):
        """
        Load an importer from a module specified in the generator's settings, or the
        default one if not.
        """
        module_path = settings.GENERATORS[self.generator_key].get("importer", settings.DEFAULT_IMPORTER)
        module = importlib.import_module(module_path)
        return module.CardImporter
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve a generator key and a base64-encoded file path from the URL, look up
        a card importer for the given generator, and run it on those files.
        This fills the database with Card objects drawn from the file, and we then
        display them to the user using the normal ListView functionality.
        """
        self.generator_key = kwargs["generator"]
        b64_file_path = kwargs["b64_file_path"]

        file_path = base64.b64decode(b64_file_path.encode("ascii")).decode("utf-8")

        importer_class = self.load_importer_class()
        importer = importer_class(self.generator_key, filenames=[file_path])
        importer.run_import()

        return super().get(request, *args, **kwargs)
