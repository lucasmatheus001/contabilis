import os
import django
from random import choice
from faker import Faker

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_processes.settings')
django.setup()

from parties.models import Party
from processes.models import Process

fake = Faker('pt_BR')

PARTY_CATEGORY_CHOICES = [
    'EXEQUENTE', 'EXECUTADA', 'REQUERENTE', 'REQUERIDO', 'AUTOR', 'RÉU', 'TERCEIRO'
]

def random_document():
    # Gera CPF ou CNPJ aleatório
    if fake.boolean():
        return fake.cpf()
    else:
        return fake.cnpj()

if Party.objects.exists():
    print('Já existem partes cadastradas. Nada foi feito.')
    exit(0)

processos = list(Process.objects.all())
if not processos:
    print('Nenhum processo encontrado. Execute o script de processos antes.')
    exit(1)

for _ in range(60):
    Party.objects.create(
        name=fake.name(),
        document=random_document(),
        category=choice(PARTY_CATEGORY_CHOICES),
        email=fake.email(),
        phone=fake.phone_number(),
        process=choice(processos),
    )
print('60 partes criadas com sucesso!') 