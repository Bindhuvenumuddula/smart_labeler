from django import forms
from django.db import models

from authentication.models import CustomUser

# Create your models here.

MEDIA_CHOICES = (
    ('IMAGE', 'images'),
    ('VIDEO', 'videos')
)


class WebMedia(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=5, choices=MEDIA_CHOICES)
    media = models.BinaryField(max_length=1048576)
    labelling_data = models.JSONField(default=dict)
    filename = models.CharField(max_length=200, default="Default")

    class Meta:
        db_table = "web_media"
        verbose_name = "Web Media"
        verbose_name_plural = "Web Media"


class UploadForm(forms.Form):
    media_type = forms.ChoiceField(choices=MEDIA_CHOICES, required=True)
    media = forms.FileField()
