from django.db import models


# Create your models here.
class WellModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CoordinateModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    well = models.ForeignKey(WellModel, on_delete=models.CASCADE)
    sequence_number = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
