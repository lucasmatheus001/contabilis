from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from processes.models import Process
from parties.models import Party


class Command(BaseCommand):
    help = 'Setup users with different permission levels'

    def handle(self, *args, **options):
        # Criar grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        user_group, created = Group.objects.get_or_create(name='Usuários')

        # Criar usuário admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        # Criar usuário normal
        normal_user, created = User.objects.get_or_create(
            username='usuario',
            defaults={
                'email': 'usuario@example.com',
                'first_name': 'Usuário',
                'last_name': 'Normal'
            }
        )
        normal_user.set_password('usuario123')
        normal_user.save()

        # Adicionar usuários aos grupos
        admin_user.groups.add(admin_group)
        normal_user.groups.add(user_group)

        # Definir permissões para usuários normais (só visualização)
        process_ct = ContentType.objects.get_for_model(Process)
        party_ct = ContentType.objects.get_for_model(Party)

        # Permissões de visualização para usuários normais
        view_process = Permission.objects.get(content_type=process_ct, codename='view_process')
        view_party = Permission.objects.get(content_type=party_ct, codename='view_party')

        user_group.permissions.add(view_process, view_party)

        # Permissões completas para administradores
        admin_permissions = Permission.objects.filter(content_type__in=[process_ct, party_ct])
        admin_group.permissions.set(admin_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                '✅ Usuários criados com sucesso!\n'
                '🔑 Credenciais:\n'
                '   Admin - Usuário: admin, Senha: admin123\n'
                '   Normal - Usuário: usuario, Senha: usuario123\n'
                '📋 Grupos criados:\n'
                '   - Administradores (acesso total)\n'
                '   - Usuários (só visualização)'
            )
        ) 