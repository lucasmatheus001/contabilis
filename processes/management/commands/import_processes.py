"""
Management command to import legal processes from HTML files.
"""

import os
import re
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from bs4 import BeautifulSoup
from processes.models import Process
from parties.models import Party


class Command(BaseCommand):
    """Command to import legal processes from HTML files."""

    help = 'Import legal processes from HTML files'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            'html_files',
            nargs='+',
            type=str,
            help='HTML files to import'
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        html_files = options['html_files']
        
        for html_file in html_files:
            if not os.path.exists(html_file):
                self.stdout.write(
                    self.style.ERROR(f'File {html_file} does not exist')
                )
                continue
                
            self.stdout.write(f'Processing file: {html_file}')
            self.import_process_from_html(html_file)

    def import_process_from_html(self, html_file):
        """Import a single process from HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract process information
            process_data = self.extract_process_data(soup)
            parties_data = self.extract_parties_data(soup)
            
            # Create process and parties
            with transaction.atomic():
                process = self.create_process(process_data)
                self.create_parties(process, parties_data)
                
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported process {process.process_number}'
                )
            )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing {html_file}: {str(e)}')
            )

    def extract_process_data(self, soup):
        """Extract process data from HTML."""
        data = {}
        
        # Extract process number
        process_number_elem = soup.find('h4', class_='mr-auto')
        if process_number_elem:
            process_number = process_number_elem.get_text(strip=True)
            # Remove status badges from process number
            process_number = re.sub(r'\s+Ativo\s+.*$', '', process_number)
            data['process_number'] = process_number.strip()
        
        # Extract status and type
        status_badges = soup.find_all('span', class_='badge')
        for badge in status_badges:
            badge_text = badge.get_text(strip=True).lower()
            if badge_text in ['ativo', 'suspenso', 'arquivado']:
                if badge_text == 'ativo':
                    data['status'] = 'active'
                elif badge_text == 'suspenso':
                    data['status'] = 'suspended'
                elif badge_text == 'arquivado':
                    data['status'] = 'archived'
            elif badge_text == 'digital':
                data['process_type'] = 'digital'
            elif badge_text == 'físico':
                data['process_type'] = 'physical'
        
        # Extract other process details
        rows = soup.find_all('div', class_='row')
        for row in rows:
            cols = row.find_all('div', class_='col-2')
            for col in cols:
                label_elem = col.find('h6', class_='text-muted')
                if not label_elem:
                    continue
                    
                label = label_elem.get_text(strip=True).replace(':', '')
                value_elem = col.find('span') or col.find('div')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    
                    if label == 'Classe':
                        data['process_class'] = value
                    elif label == 'Assunto':
                        data['subject'] = value
                    elif label == 'Juiz':
                        data['judge'] = value
                    elif label == 'Foro':
                        data['court'] = value
                    elif label == 'Vara':
                        data['jurisdiction'] = value
                    elif label == 'Comarca':
                        data['district'] = value
                    elif label == 'Distribuição':
                        data['distribution_date'] = self.parse_date(value)
                    elif label == 'Valor da ação':
                        data['action_value'] = self.parse_currency(value)
        
        return data

    def extract_parties_data(self, soup):
        """Extract parties data from HTML."""
        parties = []
        
        # Find parties section
        parties_section = soup.find('h4', string=lambda text: text and 'Partes do processo' in text)
        if not parties_section:
            return parties
            
        parties_container = parties_section.find_next('ul', class_='list-group-party')
        if not parties_container:
            return parties
            
        party_items = parties_container.find_all('li', class_='list-group-item')
        
        for item in party_items:
            party_data = {}
            
            # Extract party name and document
            name_doc_elem = item.find('span', class_='mr-auto')
            if name_doc_elem:
                text = name_doc_elem.get_text(strip=True)
                # Extract name and document using regex
                match = re.match(r'(.+?)\s*\(Documento:\s*([^)]+)\)', text)
                if match:
                    party_data['name'] = match.group(1).strip()
                    party_data['document'] = match.group(2).strip()
            
            # Extract category
            category_badge = item.find('span', class_='badge')
            if category_badge:
                category = category_badge.get_text(strip=True)
                party_data['category'] = category
            
            if party_data:
                parties.append(party_data)
        
        return parties

    def parse_date(self, date_str):
        """Parse date string to datetime object."""
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        except (ValueError, TypeError):
            return None

    def parse_currency(self, currency_str):
        """Parse currency string to decimal."""
        try:
            # Remove R$ and spaces, replace comma with dot
            clean_value = currency_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            return Decimal(clean_value)
        except (ValueError, TypeError):
            return Decimal('0.00')

    def create_process(self, data):
        """Create a process from extracted data."""
        process, created = Process.objects.get_or_create(
            process_number=data['process_number'],
            defaults={
                'status': data.get('status', 'active'),
                'process_type': data.get('process_type', 'digital'),
                'process_class': data.get('process_class', ''),
                'subject': data.get('subject', ''),
                'judge': data.get('judge', ''),
                'court': data.get('court', ''),
                'jurisdiction': data.get('jurisdiction', ''),
                'district': data.get('district', ''),
                'action_value': data.get('action_value', Decimal('0.00')),
                'distribution_date': data.get('distribution_date'),
            }
        )
        
        if not created:
            # Update existing process
            for field, value in data.items():
                if hasattr(process, field) and value is not None:
                    setattr(process, field, value)
            process.save()
        
        return process

    def create_parties(self, process, parties_data):
        """Create parties for a process."""
        for party_data in parties_data:
            party, created = Party.objects.get_or_create(
                process=process,
                document=party_data['document'],
                defaults={
                    'name': party_data['name'],
                    'category': party_data['category'],
                }
            )
            
            if not created:
                # Update existing party
                party.name = party_data['name']
                party.category = party_data['category']
                party.save() 