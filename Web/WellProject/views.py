import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pathlib import Path
import uuid
from ProjectModel.main import read_file
from os import remove, listdir
import json

from .models import WellModel, CoordinateModel, FolderModel, UploadFileModel


# Create your views here.
@login_required(login_url='login')
def index(request):
    # processing uploaded data
    directory = Path(__file__).resolve().parent.parent / 'media'
    print(directory)
    if request.method == 'POST':
        files = request.FILES.getlist('uploadfiles')
        filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        folder = FolderModel.objects.create(folder_name=filename, folder_identifier=str(uuid.uuid4()))
        for ff in files:
            UploadFileModel.objects.create(file=ff).save()
            # Read all files content for getting well_name and coords X, Y, Z
            name, coords = read_file(directory / str(ff.name))
            # Create well objects in database
            well = WellModel.objects.create(folder_id=folder.id, well_identifier=str(uuid.uuid4()), well_name=name)
            # Create coorinate objects in database
            for i, coord in enumerate(coords):
                x, y, z = coord
                CoordinateModel.objects.create(well_id=well.id, sequence_number=i, X=x, Y=y, Z=z)

    # After files read (deleting them)
    UploadFileModel.objects.all().delete()
    for filename in listdir(directory):
        remove(directory / filename)

    # Getting all data
    datas = []
    folders = FolderModel.objects.all()
    wells = WellModel.objects.all()
    coordinates = CoordinateModel.objects.all()
    data = []
    for folder in folders:
        dataset = []
        for well in wells:
            if well.folder_id == folder.id:
                coordinat = []
                for coord in coordinates:
                    if coord.well_id == well.id:
                        coordinat.append({'x': coord.X, 'y': coord.Y, 'z': coord.Z})
                element = {'id': well.id, 'name': well.well_name, 'coordinates': coordinat}
                dataset.append(element)
        row = {'id': folder.id, 'name': folder.folder_name, 'files': dataset}

        data.append(row)
        datas = json.dumps(data)

    context = {'folders': folders, 'wells': wells, 'coordinates': coordinates, 'data': datas}
    return render(request, 'WellProject/index.html', context)
