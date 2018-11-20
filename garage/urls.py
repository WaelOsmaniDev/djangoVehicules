from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "garage"

urlpatterns = [
    path('', views.home, name='home'),
    path('garages/',
         login_required(views.GaragesListView.as_view()),
         name='garages'),

]
