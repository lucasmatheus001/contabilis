"""
Models for legal processes application.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Process(models.Model):
    """
    Model to store legal process information.
    """
    PROCESS_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('archived', 'Archived'),
    ]

    PROCESS_TYPE_CHOICES = [
        ('digital', 'Digital'),
        ('physical', 'Physical'),
    ]

    # Basic process information
    process_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Process number (e.g., 1004030-81.2016.0.00.0008)"
    )
    status = models.CharField(
        max_length=20,
        choices=PROCESS_STATUS_CHOICES,
        default='active'
    )
    process_type = models.CharField(
        max_length=20,
        choices=PROCESS_TYPE_CHOICES,
        default='digital'
    )

    # Process details
    process_class = models.CharField(
        max_length=200,
        help_text="Process class (e.g., Execução de Título Extrajudicial)"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Process subject (e.g., Locação de Imóvel)"
    )
    judge = models.CharField(
        max_length=100,
        help_text="Judge name"
    )

    # Location information
    court = models.CharField(
        max_length=200,
        blank=True,
        help_text="Court name"
    )
    jurisdiction = models.CharField(
        max_length=200,
        blank=True,
        help_text="Jurisdiction information"
    )
    district = models.CharField(
        max_length=200,
        blank=True,
        help_text="District information"
    )

    # Financial information
    action_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text="Action value in currency"
    )

    # Dates
    distribution_date = models.DateField(
        null=True,
        blank=True,
        help_text="Process distribution date"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Process"
        verbose_name_plural = "Processes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.process_number} - {self.process_class}"

    @property
    def formatted_action_value(self):
        """Return formatted action value."""
        return f"R$ {self.action_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def is_active(self):
        """Check if process is active."""
        return self.status == 'active'
