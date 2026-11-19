from django.db import models


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True, default="Paragliding")  # noqa: DJ001
    badge = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    badge_type = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    url = models.CharField(max_length=200, blank=True, null=True)  # noqa: DJ001
    order = models.IntegerField(default=99)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.title}"
