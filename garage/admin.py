from django.contrib import admin

from .models import Garage, Vehicule, AFaire, Entretien


class EntretienAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'kms', 'date', 'montant')
    date_hierarchy = 'date'

    search_fields = ['vehicule__marque', 'vehicule__modele']


admin.site.register(Garage)
admin.site.register(Vehicule)
admin.site.register(AFaire)
admin.site.register(Entretien, EntretienAdmin)
