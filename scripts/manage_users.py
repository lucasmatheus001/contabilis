#!/usr/bin/env python
"""
Script para gerenciar usuários do sistema de processos jurídicos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_processes.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

def create_users():
    """Criar usuários padrão do sistema"""
    
    # Criar grupo de administradores
    admin_group, created = Group.objects.get_or_create(name='Administradores')
    if created:
        print("✅ Grupo 'Administradores' criado")
    
    # Criar grupo de usuários normais
    user_group, created = Group.objects.get_or_create(name='Usuários')
    if created:
        print("✅ Grupo 'Usuários' criado")
    
    # Criar usuário admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('admin123')
        }
    )
    
    if created:
        admin_user.groups.add(admin_group)
        print("✅ Usuário admin criado")
    else:
        # Atualizar senha se o usuário já existe
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.groups.add(admin_group)
        print("✅ Usuário admin atualizado")
    
    # Criar usuário normal
    normal_user, created = User.objects.get_or_create(
        username='usuario',
        defaults={
            'email': 'usuario@example.com',
            'first_name': 'Usuário',
            'last_name': 'Normal',
            'is_staff': False,
            'is_superuser': False,
            'password': make_password('usuario123')
        }
    )
    
    if created:
        normal_user.groups.add(user_group)
        print("✅ Usuário normal criado")
    else:
        # Atualizar senha se o usuário já existe
        normal_user.set_password('usuario123')
        normal_user.save()
        normal_user.groups.add(user_group)
        print("✅ Usuário normal atualizado")
    
    print("\n🎉 Usuários configurados com sucesso!")
    print("📋 Credenciais de acesso:")
    print("   👤 Admin - Usuário: admin, Senha: admin123")
    print("   👤 Normal - Usuário: usuario, Senha: usuario123")
    print("\n⚠️  IMPORTANTE: Altere essas senhas em produção!")

def list_users():
    """Listar todos os usuários do sistema"""
    print("\n📋 Usuários cadastrados:")
    print("-" * 50)
    
    for user in User.objects.all():
        groups = ", ".join([group.name for group in user.groups.all()])
        status = "Admin" if user.is_superuser else "Normal"
        print(f"👤 {user.username} ({user.get_full_name()}) - {status}")
        if groups:
            print(f"   Grupos: {groups}")
        print()

def delete_user(username):
    """Deletar um usuário específico"""
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"✅ Usuário '{username}' deletado com sucesso!")
    except User.DoesNotExist:
        print(f"❌ Usuário '{username}' não encontrado!")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create':
            create_users()
        elif command == 'list':
            list_users()
        elif command == 'delete' and len(sys.argv) > 2:
            delete_user(sys.argv[2])
        else:
            print("❌ Comando inválido!")
            print("Uso:")
            print("  python manage_users.py create  - Criar usuários padrão")
            print("  python manage_users.py list    - Listar usuários")
            print("  python manage_users.py delete <username> - Deletar usuário")
    else:
        print("🔧 Gerenciador de Usuários - Sistema de Processos Jurídicos")
        print("=" * 60)
        print("Comandos disponíveis:")
        print("  create  - Criar usuários padrão (admin/usuario)")
        print("  list    - Listar todos os usuários")
        print("  delete <username> - Deletar usuário específico")
        print("\nExemplo: python manage_users.py create") 