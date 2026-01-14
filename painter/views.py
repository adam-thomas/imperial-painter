import base64
import importlib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView

from . import models
from .forms import SelectGeneratorForm

# settings.IP_IMPORTER needs to point to a management command.
# There are two default ones:
#  * painter.importers.import_cards
#  * painter.importers.import_laundry
ip_importer = importlib.import_module(settings.IP_IMPORTER)


class Home(FormView):
    template_name = "painter/home.html"
    form_class = SelectGeneratorForm

    def form_valid(self, form):
        generator_key = form.cleaned_data["generator"]
        file_path = form.cleaned_data["file_path"]
        b64_file_path = base64.b64encode(file_path.encode("utf-8")).decode("ascii")

        return HttpResponseRedirect(f"/{generator_key}/{b64_file_path}")


class CardDisplay(ListView):
    model = models.Card
    template_name = "painter/card_display.html"

    def load_importer(self, generator_key):
        module_path = settings.GENERATORS[generator_key].get("importer", settings.DEFAULT_IMPORTER)
        module = importlib.import_module(module_path)
        return module.CardImporter()
    
    def get(self, request, *args, **kwargs):
        generator_key = kwargs["generator"]
        b64_file_path = kwargs["b64_file_path"]

        file_path = base64.b64decode(b64_file_path.encode("ascii")).decode("utf-8")

        importer = self.load_importer(generator_key)
        importer.handle(filenames=[file_path])

        return super().get(request, *args, **kwargs)
