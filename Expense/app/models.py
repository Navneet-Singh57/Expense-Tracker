from django.db import models

# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=200)
    cost = models.IntegerField()
    category = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    