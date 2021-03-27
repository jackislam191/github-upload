from django.db import models
from django.conf import settings

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length = 10)

    def __str__(self):
        return self.ticker

class Position(models.Model):
    stock_symbol = models.CharField(max_length = 10)
    stock_shares = models.IntegerField()
    stock_price = models.FloatField(default= 0.0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_user')
    def __str__(self):
        review = self.stock_symbol + str(self.created_by)
        return review
    