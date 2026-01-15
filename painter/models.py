from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models


GENERATOR_CHOICES = [(g["key"], g["name"]) for g in settings.GENERATORS.values()]


class Card(models.Model):
    """A single card entry."""
    name = models.CharField(max_length=255)
    template_name = models.CharField(max_length=255)
    generator_key = models.CharField(choices=GENERATOR_CHOICES)
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    data = models.JSONField(default={})

    def __str__(self):
        return self.name

    def get_template(self):
        """
        Translate the stored template_name into a path to a template, which is expected
        to be in the custom/[generator] directory.
        """
        return f"painter/{self.generator_key}/{self.template_name}.html"

    class Meta:
        ordering = ["pk"]


class CachedFilePath(models.Model):
    path = models.FilePathField(unique=True)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.path
    
    class Meta:
        ordering = ["-last_used"]
