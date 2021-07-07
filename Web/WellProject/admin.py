from django.contrib import admin

# Register your models here.
from .models import WellModel, CoordinateModel, UploadFileModel, FolderModel

admin.site.register([WellModel, CoordinateModel, UploadFileModel, FolderModel])
