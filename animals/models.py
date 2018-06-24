from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class Weight(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='weights')
    recorded_weight = models.FloatField()
    recorded_at = models.DateTimeField()
    estimated = models.BooleanField(default=False)