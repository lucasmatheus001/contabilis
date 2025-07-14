"""
Tests for legal processes application.
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Process


class ProcessModelTest(TestCase):
    """Test cases for Process model."""

    def setUp(self):
        """Set up test data."""
        self.process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            status='active',
            process_type='digital',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            court='Foro Regional VIII - Tatuapé',
            jurisdiction='4ª Vara Cível',
            action_value=Decimal('5911.72'),
        )

    def test_process_creation(self):
        """Test process creation."""
        self.assertEqual(self.process.process_number, '1004030-81.2016.0.00.0008')
        self.assertEqual(self.process.status, 'active')
        self.assertEqual(self.process.process_class, 'Execução de Título Extrajudicial')
        self.assertEqual(self.process.subject, 'Locação de Imóvel')
        self.assertEqual(self.process.judge, 'Mariana')

    def test_process_str_representation(self):
        """Test string representation of process."""
        expected = '1004030-81.2016.0.00.0008 - Execução de Título Extrajudicial'
        self.assertEqual(str(self.process), expected)

    def test_formatted_action_value(self):
        """Test formatted action value property."""
        self.assertEqual(self.process.formatted_action_value, 'R$ 5.911,72')

    def test_is_active_property(self):
        """Test is_active property."""
        self.assertTrue(self.process.is_active)
        
        self.process.status = 'suspended'
        self.assertFalse(self.process.is_active)

    def test_process_ordering(self):
        """Test process ordering by created_at."""
        process2 = Process.objects.create(
            process_number='1007944-79.2020.0.00.0361',
            process_class='Busca e Apreensão',
            subject='Alienação Fiduciária',
            judge='Domingos Parra Neto',
            action_value=Decimal('51336.07'),
        )
        
        processes = list(Process.objects.all())
        self.assertEqual(processes[0], process2)  # Newer process first


class ProcessViewsTest(TestCase):
    """Test cases for process views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.process = Process.objects.create(
            process_number='1004030-81.2016.0.00.0008',
            status='active',
            process_class='Execução de Título Extrajudicial',
            subject='Locação de Imóvel',
            judge='Mariana',
            action_value=Decimal('5911.72'),
        )

    def test_process_list_view_requires_login(self):
        """Test that process list requires login."""
        response = self.client.get(reverse('processes:process_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_process_list_view_with_login(self):
        """Test process list view with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1004030-81.2016.0.00.0008')

    def test_process_detail_view(self):
        """Test process detail view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_detail', args=[self.process.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1004030-81.2016.0.00.0008')

    def test_process_create_view(self):
        """Test process create view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_create'))
        self.assertEqual(response.status_code, 200)

    def test_process_create_post(self):
        """Test process creation via POST."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'process_number': '1007944-79.2020.0.00.0361',
            'status': 'active',
            'process_type': 'digital',
            'process_class': 'Busca e Apreensão',
            'subject': 'Alienação Fiduciária',
            'judge': 'Domingos Parra Neto',
            'action_value': '51336.07',
        }
        response = self.client.post(reverse('processes:process_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Process.objects.filter(process_number='1007944-79.2020.0.00.0361').exists())

    def test_process_update_view(self):
        """Test process update view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_update', args=[self.process.pk]))
        self.assertEqual(response.status_code, 200)

    def test_process_update_post(self):
        """Test process update via POST."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'process_number': '1004030-81.2016.0.00.0008',
            'status': 'suspended',
            'process_type': 'digital',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Locação de Imóvel Atualizada',
            'judge': 'Mariana Silva',
            'action_value': '6000.00',
        }
        response = self.client.post(reverse('processes:process_update', args=[self.process.pk]), data)
        self.assertEqual(response.status_code, 302)
        
        self.process.refresh_from_db()
        self.assertEqual(self.process.subject, 'Locação de Imóvel Atualizada')
        self.assertEqual(self.process.status, 'suspended')

    def test_process_delete_view(self):
        """Test process delete view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_delete', args=[self.process.pk]))
        self.assertEqual(response.status_code, 200)

    def test_process_delete_post(self):
        """Test process deletion via POST."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('processes:process_delete', args=[self.process.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Process.objects.filter(pk=self.process.pk).exists())

    def test_export_processes_view(self):
        """Test export processes view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:export_processes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_search_functionality(self):
        """Test search functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_list'), {'search': 'Mariana'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1004030-81.2016.0.00.0008')

    def test_status_filter(self):
        """Test status filter functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('processes:process_list'), {'status': 'active'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1004030-81.2016.0.00.0008')


class ProcessFormsTest(TestCase):
    """Test cases for process forms."""

    def test_process_form_valid(self):
        """Test valid process form."""
        from .forms import ProcessForm
        data = {
            'process_number': '1004030-81.2016.0.00.0008',
            'status': 'active',
            'process_type': 'digital',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Locação de Imóvel',
            'judge': 'Mariana',
            'action_value': '5911.72',
        }
        form = ProcessForm(data)
        self.assertTrue(form.is_valid())

    def test_process_form_invalid_process_number(self):
        """Test invalid process number."""
        from .forms import ProcessForm
        data = {
            'process_number': '123',  # Too short
            'status': 'active',
            'process_type': 'digital',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Locação de Imóvel',
            'judge': 'Mariana',
            'action_value': '5911.72',
        }
        form = ProcessForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Process number seems too short', str(form.errors))

    def test_process_form_negative_action_value(self):
        """Test negative action value."""
        from .forms import ProcessForm
        data = {
            'process_number': '1004030-81.2016.0.00.0008',
            'status': 'active',
            'process_type': 'digital',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Locação de Imóvel',
            'judge': 'Mariana',
            'action_value': '-100',
        }
        form = ProcessForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Action value cannot be negative', str(form.errors))
