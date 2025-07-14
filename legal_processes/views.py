"""
Views for legal processes project.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from processes.models import Process
from parties.models import Party


def home(request):
    """Home page view."""
    context = {}
    
    if request.user.is_authenticated:
        # Add statistics for authenticated users
        context['processes_count'] = Process.objects.count()
        context['parties_count'] = Party.objects.count()
        context['active_processes_count'] = Process.objects.filter(status='active').count()
    
    return render(request, 'home.html', context) 