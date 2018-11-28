from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit
from .models import Garage, Vehicule


def home(request):
    """Page Accueil"""
    return render(request, 'garage/home_v3.html', {})


class MenuGarage(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_garages'] = 'active'
        return context


class GaragesList(MenuGarage, generic.ListView):
    model = Garage
    context_object_name = 'object_list'


class GarageCreate(MenuGarage, edit.CreateView):
    model = Garage
    fields = ['nom', 'adresse', 'mail', 'telephone']
    template_name = "garage/object_create.html"

    def form_valid(self, form):
        form.instance.createur = self.request.user
        return super(GarageCreate, self).form_valid(form)


class GarageDetail(MenuGarage, generic.DetailView):
    model = Garage


class GarageUpdate(MenuGarage, edit.UpdateView):
    model = Garage
    fields = ['nom', 'adresse', 'mail', 'telephone']
    template_name = "garage/object_update.html"


class GarageDelete(MenuGarage, edit.DeleteView):
    model = Garage
    success_url = reverse_lazy('garage:garage-list')


class MenuVehicule(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_vehicule'] = 'active'
        return context


class VehiculesList(MenuVehicule, generic.ListView):
    model = Vehicule


class VehiculeCreate(MenuVehicule, edit.CreateView):
    model = Vehicule
    fields = ['marque', 'modele', 'immatriculation', 'proprietaire']
    template_name = "garage/object_create.html"

    def form_valid(self, form):
        form.instance.createur = self.request.user
        return super(VehiculeCreate, self).form_valid(form)


class VehiculeDetail(MenuVehicule, generic.DetailView):
    model = Vehicule


class VehiculeUpdate(MenuVehicule, edit.UpdateView):
    model = Vehicule
    fields = ['marque', 'modele', 'immatriculation', 'proprietaire']
    template_name = "garage/vehicule_update.html"


class VehiculeDelete(MenuVehicule, edit.DeleteView):
    model = Vehicule
    success_url = reverse_lazy('garage:vehicule-list')

