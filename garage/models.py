from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.user.id}/{filename}"


class Garage(models.Model):
    nom = models.CharField(max_length=32)
    adresse = models.CharField(max_length=128, null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=12, null=True, blank=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(object):
        ordering = ("nom", "adresse")

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('garage:garage-list')


class Vehicule(models.Model):
    marque = models.CharField(max_length=32)
    modele = models.CharField(max_length=32)
    immatriculation = models.CharField(max_length=32, null=True, blank=True)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
    mise_en_circulation = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)

    class Meta(object):
        ordering = ("marque", "modele")

    def __str__(self):
        msg = f"{self.marque} {self.modele}"
        if self.immatriculation:
            return f"{msg} ({self.immatriculation})"
        return msg

    def get_absolute_url(self):
        return reverse('garage:vehicule-list')


class AFaire(models.Model):
    description = models.CharField(max_length=64)
    date = models.DateField(null=True, blank=True)
    kms = models.IntegerField(null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)


class Entretien(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    kms = models.IntegerField()
    date = models.DateField()
    montant = models.DecimalField(decimal_places=2, max_digits=8)
    facture = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)



