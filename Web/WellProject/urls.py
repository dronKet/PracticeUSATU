from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wells/<int:id>', views.show, name='show'),
]
