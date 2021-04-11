from django.db import models
from django.conf import settings
# Create your models here.

class Portfolio(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='portfolioEF/', blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_user_pf')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    