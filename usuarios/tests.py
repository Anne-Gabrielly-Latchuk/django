import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_redirects_to_login(self):
        response = self.client.get('/')

        self.assertRedirects(response, '/usuarios/login/')


class PainelTemaTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tema-teste',
            password='senha-de-teste',
        )
        self.client.force_login(self.user)

    def test_painel_aplica_tema_escuro_salvo(self):
        self.client.post(
            reverse('alternar_tema'),
            data=json.dumps({'modo_escuro': True}),
            content_type='application/json',
        )

        response = self.client.get(reverse('painel_teste'))

        self.assertContains(response, 'class="painel-page tema-escuro"')
        self.assertContains(response, 'background-color: #171923 !important;')

    def test_painel_renderiza_tema_claro_por_padrao(self):
        response = self.client.get(reverse('painel_teste'))

        self.assertContains(response, 'class="painel-page"')
