#!/usr/bin/env python
"""
Script para criar usuários com diferentes níveis de acesso
"""

import os
import sys
import django
sys.path.append('/app')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_processes.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from processes.models import Process
from parties.models import Party

def create_users():
    print("🚀 Criando usuários e grupos...")
    
    # Criar grupos
    admin_group, created = Group.objects.get_or_create(name='Administradores')
    user_group, created = Group.objects.get_or_create(name='Usuários')
    
    print(f"✅ Grupos criados: Administradores, Usuários")
    
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
    
    print(f"✅ Usuários criados: admin, usuario")
    
    # Adicionar usuários aos grupos
    admin_user.groups.add(admin_group)
    normal_user.groups.add(user_group)
    
    # Definir permissões para usuários normais (só visualização)
    try:
        process_ct = ContentType.objects.get_for_model(Process)
        party_ct = ContentType.objects.get_for_model(Party)
        
        # Permissões de visualização para usuários normais
        view_process = Permission.objects.get(content_type=process_ct, codename='view_process')
        view_party = Permission.objects.get(content_type=party_ct, codename='view_party')
        
        user_group.permissions.add(view_process, view_party)
        
        # Permissões completas para administradores
        admin_permissions = Permission.objects.filter(content_type__in=[process_ct, party_ct])
        admin_group.permissions.set(admin_permissions)
        
        print("✅ Permissões configuradas com sucesso!")
        
    except Exception as e:
        print(f"⚠️  Aviso: Erro ao configurar permissões: {e}")
        print("   As permissões podem ser configuradas manualmente no admin do Django")
    
    print("\n🎉 Usuários criados com sucesso!")
    print("🔑 Credenciais:")
    print("   Admin - Usuário: admin, Senha: admin123")
    print("   Normal - Usuário: usuario, Senha: usuario123")
    print("\n📋 Grupos criados:")
    print("   - Administradores (acesso total)")
    print("   - Usuários (só visualização)")

if __name__ == '__main__':
    create_users() 