from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .company import Company
from .tech_type import Tech_Type

class Resource(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    link_to_resource = models.URLField(max_length=250, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    tech_type = models.ForeignKey(Tech_Type, on_delete=models.CASCADE, null=True)
    date_due = models.DateField(auto_now_add=True, blank=True)
    is_complete = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = ("resource")
        verbose_name_plural = ("resources")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("resource_details", kwargs={"pk": self.pk})
    
