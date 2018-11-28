from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "garage"

urlpatterns = [
    path('', views.home, name='home'),
    path('garages/',
         login_required(views.GaragesList.as_view()),
         name='garage-list'),
    path('garages/add', login_required(views.GarageCreate.as_view()),
         name='garage-create'),
    path('garages/<int:pk>/', login_required(views.GarageDetail.as_view()),
         name='garage-detail'),
    path('garages/<int:pk>/update/',
         login_required(views.GarageUpdate.as_view()),
         name='garage-update'),
    path('garages/<int:pk>/delete',
         login_required(views.GarageDelete.as_view()),
         name='garage-delete'),
    path('vehicules/',
         login_required(views.VehiculesList.as_view()),
         name='vehicule-list'),
    path('vehicules/add',
         login_required(views.VehiculeCreate.as_view()),
         name='vehicule-create'),
    path('vehicules/<int:pk>/',
         login_required(views.VehiculeDetail.as_view()),
         name='vehicule-detail'),
    path('vehicules/<int:pk>/update',
         login_required(views.VehiculeUpdate.as_view()),
         name='vehicule-update'),
    path('vehicules/<int:pk>/delete',
         login_required(views.VehiculeDelete.as_view()),
         name='vehicule-delete'),
]
