from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .company import Company


class Social_Connection(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title_of_position = models.CharField(max_length=100)
    date_of_last_encounter = models.DateField(auto_now_add=True, blank=True)
    linked_in_profile = models.URLField(max_length=250)

    class Meta:
        verbose_name = ("social_connection")
        verbose_name_plural = ("social_connections")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("social_connection_detail", kwargs={"pk": self.pk})
    