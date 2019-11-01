from django.db import models

class Company(models.Model):

    name = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = ("company")
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})
    
