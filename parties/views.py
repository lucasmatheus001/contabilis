"""
Views for parties application.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Party
from .forms import PartyForm


@login_required
def party_list(request):
    """Display list of parties with search and pagination."""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    parties = Party.objects.all()
    
    # Apply search filter
    if search_query:
        parties = parties.filter(
            Q(name__icontains=search_query) |
            Q(document__icontains=search_query) |
            Q(process__process_number__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        parties = parties.filter(category=category_filter)
    
    # Pagination
    paginator = Paginator(parties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'category_choices': Party.PARTY_CATEGORY_CHOICES,
    }
    
    return render(request, 'parties/party_list.html', context)


@login_required
def party_detail(request, pk):
    """Display party details."""
    party = get_object_or_404(Party, pk=pk)
    
    context = {
        'party': party,
    }
    
    return render(request, 'parties/party_detail.html', context)


@login_required
def party_create(request):
    """Create a new party."""
    if request.method == 'POST':
        form = PartyForm(request.POST)
        if form.is_valid():
            party = form.save()
            messages.success(request, f'Party {party.name} created successfully.')
            return redirect('parties:party_detail', pk=party.pk)
    else:
        form = PartyForm()
    
    context = {
        'form': form,
        'title': 'Create Party',
    }
    
    return render(request, 'parties/party_form.html', context)


@login_required
def party_update(request, pk):
    """Update an existing party."""
    party = get_object_or_404(Party, pk=pk)
    
    if request.method == 'POST':
        form = PartyForm(request.POST, instance=party)
        if form.is_valid():
            party = form.save()
            messages.success(request, f'Party {party.name} updated successfully.')
            return redirect('parties:party_detail', pk=party.pk)
    else:
        form = PartyForm(instance=party)
    
    context = {
        'form': form,
        'party': party,
        'title': 'Update Party',
    }
    
    return render(request, 'parties/party_form.html', context)


@login_required
def party_delete(request, pk):
    """Delete a party."""
    party = get_object_or_404(Party, pk=pk)
    
    if request.method == 'POST':
        party_name = party.name
        party.delete()
        messages.success(request, f'Party {party_name} deleted successfully.')
        return redirect('parties:party_list')
    
    context = {
        'party': party,
    }
    
    return render(request, 'parties/party_confirm_delete.html', context)
