from django.db import models
from django.utils import timezone
from .job import Job

class Company(models.Model):

    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("company")
        verbose_name_plural = ("company")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})
    
