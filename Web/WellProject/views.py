from django.shortcuts import render

from .mocks import Well
from .models import WellModel, CoordinateModel


# Create your views here.
def index(request):
    # wells = Well.all()
    wells = WellModel.objects.all()
    coord = CoordinateModel.objects.all()
    return render(request, 'WellProject/index.html', {'wells': wells, 'coords': coord})


def show(request, id):
    # well = Well.find(id)
    # mylist = zip(well['Coordinate']['x'], well['Coordinate']['y'], well['Coordinate']['z'])
    well = WellModel.objects.get(id=id)
    coords = CoordinateModel.objects.filter(well_id=id)
    return render(request, 'WellProject/show.html', {'well': well, 'coords': coords})
