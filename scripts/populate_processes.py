import os
import django
from decimal import Decimal
from random import choice
from faker import Faker

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_processes.settings')
django.setup()

from processes.models import Process

fake = Faker('pt_BR')

PROCESS_STATUS_CHOICES = ['active', 'suspended', 'archived']
PROCESS_TYPE_CHOICES = ['digital', 'physical']

if Process.objects.exists():  # type: ignore
    print('Já existem processos cadastrados. Nada foi feito.')
    exit(0)

for _ in range(60):
    Process.objects.create(  # type: ignore
        process_number=fake.unique.bothify(text='########-##.####.#.##.####'),
        status=choice(PROCESS_STATUS_CHOICES),
        process_type=choice(PROCESS_TYPE_CHOICES),
        process_class=fake.job(),
        subject=fake.sentence(nb_words=3),
        judge=fake.name(),
        court=fake.company(),
        jurisdiction=fake.city(),
        district=fake.city_suffix(),
        action_value=Decimal(str(fake.pydecimal(left_digits=5, right_digits=2, positive=True))),
        distribution_date=fake.date_between(start_date='-5y', end_date='today'),
    )
print('60 processos criados com sucesso!') 