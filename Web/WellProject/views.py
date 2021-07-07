import datetime

from django.contrib.auth.decorators import login_required
from .models import UploadFileModel
from django.shortcuts import render
import json

from .models import WellModel, CoordinateModel, FolderModel


# Create your views here.
@login_required(login_url='login')
def index(request):
    # wells = WellModel.objects.all()
    # coordinates = CoordinateModel.objects.all()
    # filess = UploadFileModel.objects.all()
    # dataset = []
    # for well in wells:
    #     coordinat = []
    #     for coord in coordinates:
    #         if coord.well_id == well.id:
    #             coordinat.append({'x': coord.X, 'y': coord.Y, 'z': coord.Z})
    #     element = {'id': well.id, 'name': well.name, 'coordinates': coordinat}
    #     dataset.append(element)
    # data = json.dumps(dataset)

    # processing uploaded data
    f = []
    if request.method == 'POST':
        files = request.FILES.getlist('uploadfiles')
        filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        folder = FolderModel.objects.create(folder_name=filename)
        for ff in files:
            with open(ff, 'r') as file:
                content = file.read()
            f.append(ff.name)
            # Read all files content for getting well_name and coords X, Y, Z

            # Create well objects in database
            well = WellModel.objects.create(folder_id=folder.id, well_name=ff.name)

            # Model using to read and save data to another database
            UploadFileModel.objects.create(file=ff).save()

    folders = FolderModel.objects.all()
    wells = WellModel.objects.all()
    coords = CoordinateModel.objects.all()

    context = {'files': f}
    return render(request, 'WellProject/index.html', context)
