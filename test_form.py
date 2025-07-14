#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seuprojeto.settings')
django.setup()

from processes.models import SeuModel
from faker import Faker

fake = Faker('pt_BR')
for _ in range(60):
    SeuModel.objects.create(
        campo1=fake.name(),
        campo2=fake.date(),
        # outros campos...
    ) 