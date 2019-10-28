from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .company import Company
from .tech_type import Tech_Type

class Study_Resource(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_to_resource = models.URLField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tech_type = models.ForeignKey(Tech_Type, on_delete=models.CASCADE)
    date_due = models.DateField(auto_now_add=True, blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("study_resource")
        verbose_name_plural = ("study_resources")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("study_resource_detail", kwargs={"pk": self.pk})
    
