from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1_000)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.owner.username}'s {self.name}"


class Measurement(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["hydroponic_system", "-when_measured"])
        ]
        ordering = ["-when_measured"]

    when_measured = models.DateTimeField(auto_now_add=True)
    water_ph = models.FloatField(null=True)
    water_tds = models.FloatField(null=True)
    water_temp = models.FloatField(null=True)
    hydroponic_system = models.ForeignKey(
        HydroponicSystem,
        related_name="measurements",
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self):
        return (
            f"Measurement {self.pk}: {self.when_measured},"
            "ph={self.water_ph}, tds={self.wated_tds},"
            "temperature={self.temperature}"
        )
