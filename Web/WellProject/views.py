from django.shortcuts import render

from .models import WellModel, CoordinateModel


# Create your views here.
def index(request):
    wells = WellModel.objects.all()
    return render(request, 'WellProject/index.html', {'wells': wells})


def show(request, id):
    well = WellModel.objects.get(id=id)
    coords = CoordinateModel.objects.filter(well__id=id)
    return render(request, 'WellProject/show.html', {'well': well, 'coords': coords})
