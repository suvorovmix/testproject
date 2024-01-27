# linktracker/models.py
from django.db import models
from urllib.parse import urlparse


# Create your models here.
class VisitedLink(models.Model):
    link = models.URLField()
    visited_at = models.DateTimeField(auto_now_add=True)

    def get_domain(self):
        return urlparse(self.link).hostname

    def __str__(self) :
        return f"{self.link[:30]}..."