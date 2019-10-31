from django.db import models

class Tech_Type(models.Model):

    name = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name = ("tech_type")
        verbose_name_plural = ("tech_types")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("tech_type_detail", kwargs={"pk": self.pk})
    