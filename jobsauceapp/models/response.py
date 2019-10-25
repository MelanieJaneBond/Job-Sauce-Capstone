from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .job import Job


class Reponse(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    is_rejected = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = ("response")
        verbose_name_plural = ("responses")

    def __str__(self):
        return self.date
    
    def get_absolute_url(self):
        return reverse("response_detail", kwargs={"pk": self.pk})
    
