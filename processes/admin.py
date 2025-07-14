"""
Admin configuration for legal processes application.
"""

from django.contrib import admin
from .models import Process


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    """Admin configuration for Process model."""
    
    list_display = [
        'process_number',
        'process_class',
        'subject',
        'judge',
        'status',
        'action_value',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'process_type',
        'distribution_date',
        'created_at',
    ]
    
    search_fields = [
        'process_number',
        'process_class',
        'subject',
        'judge',
        'court',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'process_number',
                'status',
                'process_type',
            )
        }),
        ('Process Details', {
            'fields': (
                'process_class',
                'subject',
                'judge',
            )
        }),
        ('Location Information', {
            'fields': (
                'court',
                'jurisdiction',
                'district',
            ),
            'classes': ('collapse',)
        }),
        ('Financial Information', {
            'fields': (
                'action_value',
                'distribution_date',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """Optimize queryset with related parties."""
        return super().get_queryset(request).prefetch_related('parties')
