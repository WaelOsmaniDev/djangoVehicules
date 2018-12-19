from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

from garage.models import Vehicule, Garage


class URLAnonymeTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        uri = reverse('garage:vehicule-list')
        response = self.client.get(uri)
        self.assertRedirects(response,
                             '/accounts/login/?next=/vehicules/')

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')

    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class URLUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        create_data(self)
        self.user1.set_password("pour_les_tests")
        self.user1.save()
        response = self.client.login(
            username=self.user1.username,
            password="pour_les_tests")
        self.assertEqual(response, True)

    def test_vehicule_detail(self):
        uri = reverse('garage:vehicule-detail',
                      kwargs={'pk': self.vehicule1.pk})
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['vehicule'],
                         self.vehicule1)

    def test_contact(self):
        response = self.client.get(reverse('garage:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)  # aucun msg dans la mailbox
        mon_sujet = "un sujet !"
        mon_message = "blablabla"
        uri = reverse('garage:contact')
        response = self.client.post(uri,
                                    {'sujet': mon_sujet,
                                     'message': mon_message})
        self.assertRedirects(response, '/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, mon_sujet)
        self.assertEqual(mail.outbox[0].body, mon_message)

    def test_vehicule_visible(self):
        self.assertEqual(self.vehicule1.visible, False)
        uri_visible = reverse('garage:vehicule-visible',
                              kwargs={'pk': self.vehicule1.pk})
        uri_detail = reverse('garage:vehicule-detail',
                             kwargs={'pk': self.vehicule1.pk})

        response = self.client.get(uri_visible)
        self.assertRedirects(response, uri_detail)

        self.assertEqual(self.vehicule1.visible, False)  # car pas de refresh depuis les données en base
        self.vehicule1 = Vehicule.objects.get(pk=self.vehicule1.pk)
        self.assertEqual(self.vehicule1.visible, True)

    def test_vehicule_update(self):
        uri_update = reverse('garage:vehicule-update',
                             kwargs={'pk': self.vehicule1.pk})
        uri_detail = reverse('garage:vehicule-detail',
                             kwargs={'pk': self.vehicule1.pk})

        response = self.client.get(uri_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.vehicule1.mise_en_circulation, 0)

        response = self.client.post(uri_update,
                                    {'mise_en_circulation': 2018,
                                     'marque': self.vehicule1.marque,
                                     'modele': self.vehicule1.modele,
                                     'proprietaire': self.vehicule1.proprietaire.pk,
                                     'visible': self.vehicule1.visible
                                     })
        print(Vehicule.objects.get(pk=self.vehicule1.pk).mise_en_circulation)
        self.assertRedirects(response, uri_detail)
        self.vehicule1 = Vehicule.objects.get(pk=self.vehicule1.pk)
        self.assertEqual(2018, self.vehicule1.mise_en_circulation)


    def test_garage_create(self):
        uri_create = reverse('garage:garage-create')

        response = self.client.post(uri_create,
                                    {
                                        'nom': "Speedy"
                                    })

        self.assertRedirects(response,
                             reverse('garage:garage-detail', kwargs={'pk': 1}))
        garage1 = Garage.objects.get(pk=1)
        self.assertEqual("Speedy", garage1.nom)


def create_data(self):
        self.user1 = User.objects.create(username="user1")
        self.user1.save()
        self.user2 = User.objects.create(username="user2")
        self.user2.save()

        self.admin = User.objects.create(username="admin",
                                         is_staff=True,
                                         is_superuser=True)
        self.admin.save()
        create = Vehicule.objects.create
        self.vehicule1 = create(marque="Toto", modele="TX",
                                proprietaire=self.user1)
