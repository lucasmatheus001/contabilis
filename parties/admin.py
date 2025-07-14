"""
Admin configuration for parties application.
"""

from django.contrib import admin
from .models import Party


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    """Admin configuration for Party model."""
    
    list_display = [
        'name',
        'document',
        'category',
        'process',
        'email',
        'phone',
        'created_at',
    ]
    
    list_filter = [
        'category',
        'process',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'document',
        'process__process_number',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'document',
                'category',
            )
        }),
        ('Contact Information', {
            'fields': (
                'email',
                'phone',
            )
        }),
        ('Process Relationship', {
            'fields': (
                'process',
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
    
    ordering = ['name']
    
    def get_queryset(self, request):
        """Optimize queryset with related process."""
        return super().get_queryset(request).select_related('process')
