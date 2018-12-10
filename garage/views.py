from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import edit, FormView

from garage.forms import ContactForm
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


def vehicule_visible(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.user == vehicule.proprietaire:
        vehicule.toggle_visible()
        messages.success(request, "Modification enregistrée")
    else:
        messages.error(request, "Accès non autorisé")
    return redirect('garage:vehicule-detail', pk)


class ContactView(FormView):
    template_name = 'garage/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('garage:home')

    def form_valid(self, form):
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        send_mail(sujet, message, self.request.user.email,
                  ['admin@example.com'])
        messages.success(self.request, "Mail envoyé !")
        return super().form_valid(form)
