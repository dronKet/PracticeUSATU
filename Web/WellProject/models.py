from django.db import models


# Create your models here.
class Well(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Coordinate(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE)
    data = models.JSONField()


