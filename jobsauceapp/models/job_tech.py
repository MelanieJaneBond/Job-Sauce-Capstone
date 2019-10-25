from django.db import models
from .job import Job
from .tech_type import Tech_Type

class Job_Tech(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    tech_type = models.ForeignKey(Tech_Type, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("job_tech")
        verbose_name_plural = ("job_techs")

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("job_tech_detail", kwargs={"pk": self.pk})
    