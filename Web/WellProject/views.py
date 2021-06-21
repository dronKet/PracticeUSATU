from django.shortcuts import render

from .mocks import Well


# Create your views here.
def index(request):
    wells = Well.all()
    return render(request, 'WellProject/index.html', {'wells': wells})


def show(request, id):
    well = Well.find(id)
    mylist = zip(well['Coordinate']['x'], well['Coordinate']['y'], well['Coordinate']['z'])
    return render(request, 'WellProject/show.html', {'well': well, 'coords': mylist})
