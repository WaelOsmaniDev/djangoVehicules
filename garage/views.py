from django.shortcuts import render
from django.views.generic import ListView
from .models import Garage


def home(request):
    """Page Accueil"""
    return render(request, 'garage/home_v3.html', {})


class GaragesListView(ListView):
    model = Garage
    context_object_name = 'garages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_garages'] = 'active'
        return context


