import datetime
from django.db import models


class Baby(models.Model):
    name = models.CharField(max_length=100)
    age = models.DateField(null=True)

    def __str__(self):
        return f'{self.name}, {datetime.date.today() - self.age} days'


class Food(models.Model):
    name = models.CharField(max_length=100)
    natural = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Feeding(models.Model):
    date = models.DateTimeField('feeding date')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.IntegerField()
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.food} on {self.date} at {self.time}'
