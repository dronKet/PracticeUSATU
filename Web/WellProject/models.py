from django.db import models


# Create your models here.
class FolderModel(models.Model):
    folder_name = models.CharField(max_length=200)


class WellModel(models.Model):
    folder = models.ForeignKey(FolderModel, on_delete=models.CASCADE)
    well_name = models.CharField(max_length=200)

    def __str__(self):
        return self.well_name


class CoordinateModel(models.Model):
    well = models.ForeignKey(WellModel, on_delete=models.CASCADE)
    sequence_number = models.IntegerField()
    X = models.FloatField()
    Y = models.FloatField()
    Z = models.FloatField()

    def __str__(self):
        return 'Well ID: ' + str(self.well.id) + ', name: ' + self.well.name + \
               ', sequence: ' + str(self.sequence_number)


class UploadFileModel(models.Model):
    file = models.FileField(upload_to='')

    def __str__(self):
        return self.file.name
