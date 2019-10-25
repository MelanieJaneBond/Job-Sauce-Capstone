from django.db import models

class Company(models.Model):

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="Co")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("company")
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})
    
