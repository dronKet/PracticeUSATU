from django.contrib import admin

# Register your models here.
from .models import WellModel, CoordinateModel

admin.site.register([WellModel, CoordinateModel])
