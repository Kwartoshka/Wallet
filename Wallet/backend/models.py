from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[
        MinValueValidator(0.01),
        MaxValueValidator(10 ** 9)])

    def __str__(self):
        return f'{self.title} by {self.user} with balance:{self.balance}'

class Operation(models.Model):
    operation_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='operation_from')
    operation_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='operation_eto')
    sum = models.DecimalField(max_digits=12, decimal_places=2, validators=[
        MinValueValidator(0.01),
        MaxValueValidator(10 ** 9)])

    def __str__(self):
        return f'Operation from{self.operation_from} to {self.operation_to}. Sum:{self.sum}'

