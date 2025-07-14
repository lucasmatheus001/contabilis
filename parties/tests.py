"""
Tests for parties application.
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from processes.models import Process
from .models import Party


class PartyModelTest(TestCase):
    """Test cases for Party model."""

    def setUp(self):
        """Set up test data."""
        self.process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )
        
        self.party = Party.objects.create(
            name='Eduardo Amoroso',
            document='564.406.360-73',
            category='EXEQUENTE',
            email='eduardo@example.com',
            phone='(11) 99999-9999',
            process=self.process,
        )

    def test_party_creation(self):
        """Test party creation."""
        self.assertEqual(self.party.name, 'Eduardo Amoroso')
        self.assertEqual(self.party.document, '564.406.360-73')
        self.assertEqual(self.party.category, 'EXEQUENTE')
        self.assertEqual(self.party.email, 'eduardo@example.com')
        self.assertEqual(self.party.phone, '(11) 99999-9999')

    def test_party_str_representation(self):
        """Test string representation of party."""
        expected = 'Eduardo Amoroso (Exequente) - 1004030-81.2016.0.00.0008'
        self.assertEqual(str(self.party), expected)

    def test_is_individual_property(self):
        """Test is_individual property."""
        # CPF (11 digits) - individual
        self.assertTrue(self.party.is_individual)
        
        # CNPJ (14 digits) - company
        company_party = Party.objects.create(
            name='Banco Bandeira',
            document='10.261.482/0001-97',
            category='REQUERENTE',
            process=self.process,
        )
        self.assertFalse(company_party.is_individual)

    def test_formatted_document(self):
        """Test formatted document property."""
        # CPF formatting
        self.assertEqual(self.party.formatted_document, '564.406.360-73')
        
        # CNPJ formatting
        company_party = Party.objects.create(
            name='Banco Bandeira',
            document='10.261.482/0001-97',
            category='REQUERENTE',
            process=self.process,
        )
        self.assertEqual(company_party.formatted_document, '10.261.482/0001-97')

    def test_party_ordering(self):
        """Test party ordering by name."""
        party2 = Party.objects.create(
            name='Ana Silva',
            document='123.456.789-00',
            category='EXECUTADA',
            process=self.process,
        )
        
        parties = list(Party.objects.all())
        self.assertEqual(parties[0], party2)  # Ana comes before Eduardo


class PartyViewsTest(TestCase):
    """Test cases for party views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )
        self.party = Party.objects.create(
            name='Eduardo Amoroso',
            document='564.406.360-73',
            category='EXEQUENTE',
            email='eduardo@example.com',
            phone='(11) 99999-9999',
            process=self.process,
        )

    def test_party_list_view_requires_login(self):
        """Test that party list requires login."""
        response = self.client.get(reverse('parties:party_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_party_list_view_with_login(self):
        """Test party list view with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eduardo Amoroso')

    def test_party_detail_view(self):
        """Test party detail view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_detail', args=[self.party.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eduardo Amoroso')

    def test_party_create_view(self):
        """Test party create view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_create'))
        self.assertEqual(response.status_code, 200)

    def test_party_create_post(self):
        """Test party creation via POST."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Daniele Caldas',
            'document': '093.911.450-00',
            'category': 'EXECUTADA',
            'email': 'daniele@example.com',
            'phone': '(11) 88888-8888',
            'process': self.process.pk,
        }
        response = self.client.post(reverse('parties:party_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Party.objects.filter(name='Daniele Caldas').exists())

    def test_party_update_view(self):
        """Test party update view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_update', args=[self.party.pk]))
        self.assertEqual(response.status_code, 200)

    def test_party_update_post(self):
        """Test party update via POST."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Eduardo Amoroso Silva',
            'document': '564.406.360-73',
            'category': 'EXEQUENTE',
            'email': 'eduardo.silva@example.com',
            'phone': '(11) 77777-7777',
            'process': self.process.pk,
        }
        response = self.client.post(reverse('parties:party_update', args=[self.party.pk]), data)
        self.assertEqual(response.status_code, 302)
        
        self.party.refresh_from_db()
        self.assertEqual(self.party.name, 'Eduardo Amoroso Silva')
        self.assertEqual(self.party.email, 'eduardo.silva@example.com')

    def test_party_delete_view(self):
        """Test party delete view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_delete', args=[self.party.pk]))
        self.assertEqual(response.status_code, 200)

    def test_party_delete_post(self):
        """Test party deletion via POST."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('parties:party_delete', args=[self.party.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Party.objects.filter(pk=self.party.pk).exists())

    def test_search_functionality(self):
        """Test search functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_list'), {'search': 'Eduardo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eduardo Amoroso')

    def test_category_filter(self):
        """Test category filter functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parties:party_list'), {'category': 'EXEQUENTE'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eduardo Amoroso')


class PartyFormsTest(TestCase):
    """Test cases for party forms."""

    def test_party_form_valid(self):
        """Test valid party form."""
        from .forms import PartyForm
        from processes.models import Process
        
        process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )
        
        data = {
            'name': 'Eduardo Amoroso',
            'document': '564.406.360-73',
            'category': 'EXEQUENTE',
            'email': 'eduardo@example.com',
            'phone': '(11) 99999-9999',
            'process': process.pk,
        }
        form = PartyForm(data)
        self.assertTrue(form.is_valid())

    def test_party_form_invalid_document(self):
        """Test invalid document format."""
        from .forms import PartyForm
        from processes.models import Process
        
        process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )
        
        data = {
            'name': 'Eduardo Amoroso',
            'document': '123',  # Invalid format
            'category': 'EXEQUENTE',
            'email': 'eduardo@example.com',
            'phone': '(11) 99999-9999',
            'process': process.pk,
        }
        form = PartyForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Document must be CPF (11 digits) or CNPJ (14 digits)', str(form.errors))

    def test_party_form_invalid_email(self):
        """Test invalid email format."""
        from .forms import PartyForm
        from processes.models import Process
        
        process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )
        
        data = {
            'name': 'Eduardo Amoroso',
            'document': '564.406.360-73',
            'category': 'EXEQUENTE',
            'email': 'invalid-email',  # Invalid email
            'phone': '(11) 99999-9999',
            'process': process.pk,
        }
        form = PartyForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please enter a valid email address', str(form.errors))
