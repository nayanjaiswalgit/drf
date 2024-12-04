from django.db import models

class Transaction(models.Model):
    email = models.ForeignKey('Email', on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey('File', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
