from django.db import models
from simple_history.models import HistoricalRecords


class Pattern(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    duration = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    enabled = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
