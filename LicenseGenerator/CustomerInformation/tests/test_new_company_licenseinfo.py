from django.test import TestCase
from django.urls import reverse
from ..models import Company

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='smith', email='smith@mail.com', password='123')
        Company.objects.create(name='Ducati', description='This is a two-wheeler automobile company.',created_by=user,updated_by=user)
        self.url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))