"""
Forms for legal processes application.
"""

from django import forms
from .models import Process


class ProcessForm(forms.ModelForm):
    """Form for creating and editing processes."""
    
    class Meta:
        model = Process
        fields = [
            'process_number',
            'status',
            'process_type',
            'process_class',
            'subject',
            'judge',
            'court',
            'jurisdiction',
            'district',
            'action_value',
            'distribution_date',
        ]
        widgets = {
            'process_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1004030-81.2016.0.00.0008'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'process_type': forms.Select(attrs={'class': 'form-select'}),
            'process_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Execução de Título Extrajudicial'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Locação de Imóvel'
            }),
            'judge': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judge name'
            }),
            'court': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Court name'
            }),
            'jurisdiction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jurisdiction information'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'District information'
            }),
            'action_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'distribution_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_process_number(self):
        """Validate process number format."""
        process_number = self.cleaned_data['process_number']
        if not process_number:
            raise forms.ValidationError("Process number is required.")
        
        # Basic validation for process number format
        if len(process_number) < 10:
            raise forms.ValidationError("Process number seems too short.")
        
        return process_number.strip()

    def clean_action_value(self):
        """Validate action value."""
        action_value = self.cleaned_data['action_value']
        if action_value and action_value < 0:
            raise forms.ValidationError("Action value cannot be negative.")
        return action_value 