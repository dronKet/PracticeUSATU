from django.shortcuts import render

from .mocks import Well


# Create your views here.
def index(request):
    wells = Well.all()
    return render(request, 'WellProject/index.html', {'wells': wells})


def show(request, id):
    well = Well.find(id)
    return render(request, 'WellProject/show.html', {'well': well})
