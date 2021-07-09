# Generated by Django 3.2.4 on 2021-07-08 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FolderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_identifier', models.IntegerField()),
                ('folder_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='WellModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('well_identifier', models.IntegerField()),
                ('well_name', models.CharField(max_length=200)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WellProject.foldermodel')),
            ],
        ),
        migrations.CreateModel(
            name='CoordinateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_number', models.IntegerField()),
                ('X', models.FloatField()),
                ('Y', models.FloatField()),
                ('Z', models.FloatField()),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WellProject.wellmodel')),
            ],
        ),
    ]
