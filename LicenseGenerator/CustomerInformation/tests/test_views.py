from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from ..views import home, company_licenseinfo,new_company_licenseinfo
from ..models import Company,LicenseInformation
from django.contrib.auth.models import User
from ..forms import NewLicenseInformationForm


class HomeTests(TestCase):
    def setUp(self):
         user = User.objects.create_user(username='smith', email='smith@mail.com', password='123')
         self.company = Company.objects.create(name='Ducati', description='This is a two-wheeler automobile company.',created_by=user,updated_by=user)
         url = reverse('home')
         self.response = self.client.get(url)
    
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_home_view_contains_link_to_company_licenseinfo_page(self):
        company_licenseinfo_url = reverse('company_licenseinfo', kwargs={'pk': self.company.pk})
        self.assertContains(self.response, 'href="{0}"'.format(company_licenseinfo_url))
        
class CompanyLicenseInformationTests(TestCase):
    # create user and company data for testing
    def setUp(self):
        user = User.objects.create_user(username='jack', email='jack@mail.com', password='123')
        Company.objects.create(name='Mercedes', description='This is an automobile company.',created_by=user,updated_by=user)
     
    def test_company_licenseinfo_view_success_status_code(self):
        url = reverse('company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_company_licenseinfo_view_not_found_status_code(self):
        url = reverse('company_licenseinfo', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_company_licenseinfo_url_resolves_bcompany_licenseinfo_view(self):
        view = resolve('/CustomerInformation/1/')
        self.assertEquals(view.func, company_licenseinfo)
     
    # Test for navigation back to home page
    def test_company_licenseinfo_view_contains_link_back_to_homepage(self):
        company_licenseinfo_url = reverse('company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(company_licenseinfo_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
    
    # Test for navigation to add new license information page
    def test_company_licenseinfo_view_contains_navigation_links(self):
        company_licenseinfo_url = reverse('company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(company_licenseinfo_url)
        new_company_licenseinfo_url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(new_company_licenseinfo_url))
        
class NewCompanyLicenseInformationTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='Segio', email='sergio@mail.com', password='123')
        company = Company.objects.create(name='Alfa Romeo', description='This is an automobile company.',created_by=user,updated_by=user)
    
    def test_new_company_licenseinfo_view_success_status_code(self):
        url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_new_company_licenseinfo_view_not_found_status_code(self):
        url = reverse('new_company_licenseinfo', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    def test_new_company_licenseinfo_url_resolves_new_company_licenseinfo_view(self):
        view = resolve('/CustomerInformation/1/new/')
        self.assertEquals(view.func, new_company_licenseinfo)
        
    def test_new_company_licenseinfo_view_contains_link_back_to_company_licenseinfo_view(self):
        new_company_licenseinfo_url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        company_licenseinfo_url = reverse('company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(new_company_licenseinfo_url)
        self.assertContains(response, 'href="{0}"'.format(company_licenseinfo_url))
        
    # Test for CSRF token generation
    def test_csrf(self):
        url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    # To test data[Valid] posted
    def test_new_company_licenseinfo_valid_post_data(self):
        url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        data = {
            'product':'Test product',
            'company':'Test Company',
            'license':'1111-2222-1234',
            'noofusers':'10',
            'noofdaystrial':'30',
            'created_by':'1',
            'updated_by':'1'
        }
        response = self.client.post(url, data)
        self.assertTrue(LicenseInformation.objects.exists())
        
    def test_contains_form(self):  # <- new test
        url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewLicenseInformationForm)
        
    # To test data[Invalid]. Invalid post data should not redirect
    # The expected behavior is to show the form again with validation errors
    def test_new_company_licenseinfo_invalid_post_data(self):
        url = reverse('new_company_licenseinfo', kwargs={'pk': 1})
        data = {}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)