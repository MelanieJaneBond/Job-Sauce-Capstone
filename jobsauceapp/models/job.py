from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .tech_type import Tech_Type
from .company import Company

class Job(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title_of_position = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Co", null=True)
    tech_list = models.ForeignKey(Tech_Type, on_delete=models.CASCADE, null=True)
    date_of_submission = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = ("job")
        verbose_name_plural = ("jobs")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})
    