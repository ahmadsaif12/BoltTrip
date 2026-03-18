from django.db import models
from apps.misc.models import BaseModel


class TourType(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
