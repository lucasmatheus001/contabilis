"""
Models for parties application.
"""

from django.db import models
from django.core.validators import RegexValidator


class Party(models.Model):
    """
    Model to store party information in legal processes.
    """
    PARTY_CATEGORY_CHOICES = [
        ('EXEQUENTE', 'Exequente'),
        ('EXECUTADA', 'Executada'),
        ('REQUERENTE', 'Requerente'),
        ('REQUERIDO', 'Requerido'),
        ('AUTOR', 'Autor'),
        ('RÉU', 'Réu'),
        ('TERCEIRO', 'Terceiro'),
    ]

    # Basic information
    name = models.CharField(
        max_length=200,
        help_text="Party name"
    )
    document = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[\d\.\-/]+$',
                message='Document must contain only numbers, dots, hyphens and slashes'
            )
        ],
        help_text="Document number (CPF, CNPJ, etc.)"
    )
    category = models.CharField(
        max_length=20,
        choices=PARTY_CATEGORY_CHOICES,
        help_text="Party category in the process"
    )

    # Contact information
    email = models.EmailField(
        blank=True,
        help_text="Party email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Party phone number"
    )

    # Relationship with process
    process = models.ForeignKey(
        'processes.Process',
        on_delete=models.CASCADE,
        related_name='parties',
        help_text="Related legal process"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"
        ordering = ['name']
        unique_together = ['process', 'document']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) - {self.process.process_number}"

    @property
    def is_individual(self):
        """Check if party is an individual (CPF) or company (CNPJ)."""
        return len(self.document.replace('.', '').replace('-', '').replace('/', '')) == 11

    @property
    def formatted_document(self):
        """Return formatted document number."""
        doc = self.document.replace('.', '').replace('-', '').replace('/', '')
        if len(doc) == 11:  # CPF
            return f"{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}"
        elif len(doc) == 14:  # CNPJ
            return f"{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}"
        return self.document
