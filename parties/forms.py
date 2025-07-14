"""
Forms for parties application.
"""

from django import forms
from .models import Party


class PartyForm(forms.ModelForm):
    """Form for creating and editing parties."""
    
    class Meta:
        model = Party
        fields = [
            'name',
            'document',
            'category',
            'email',
            'phone',
            'process',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da parte'
            }),
            'document': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF ou CNPJ'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'process': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione o processo'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar processos por número para facilitar a seleção
        try:
            from processes.models import Process
            self.fields['process'].queryset = Process.objects.all().order_by('process_number')
            self.fields['process'].empty_label = "Selecione um processo"
        except ImportError:
            # Fallback caso haja problema de importação
            pass

    def clean_document(self):
        """Validate document format."""
        document = self.cleaned_data['document']
        if not document:
            raise forms.ValidationError("Documento é obrigatório.")
        
        # Remove formatting for validation
        clean_doc = document.replace('.', '').replace('-', '').replace('/', '')
        
        if not clean_doc.isdigit():
            raise forms.ValidationError("Documento deve conter apenas números.")
        
        if len(clean_doc) not in [11, 14]:
            raise forms.ValidationError("Documento deve ser CPF (11 dígitos) ou CNPJ (14 dígitos).")
        
        return document

    def clean_email(self):
        """Validate email format."""
        email = self.cleaned_data['email']
        if email and '@' not in email:
            raise forms.ValidationError("Por favor, insira um endereço de email válido.")
        return email 