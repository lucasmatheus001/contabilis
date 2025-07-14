# Sistema de Gerenciamento de Processos Jurídicos - Python 3.13

Este projeto Django foi configurado especificamente para funcionar com Python 3.13.

## 🚀 Instalação Rápida

### Para Python 3.13 (Recomendado)

```bash
# Execute o script específico para Python 3.13
./setup_python313.sh
```

### Para outras versões do Python

```bash
# Execute o script padrão
./setup.sh
```

## 🔧 Solução de Problemas

### Problemas com Python 3.13

Se você está usando Python 3.13 e enfrenta problemas de instalação:

1. **psycopg2-binary**: A versão 2.9.9 pode falhar. O script automaticamente tenta versões mais recentes.

2. **Pillow**: A versão 10.2.0 pode falhar. O script automaticamente tenta versões mais recentes.

### Instalação Manual (se necessário)

```bash
# Remover ambiente virtual existente
rm -rf venv

# Criar novo ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências do sistema (Fedora)
sudo dnf install -y python3-devel postgresql-devel libpq-devel gcc

# Instalar dependências Python
pip install Django==4.2.7
pip install pytest==7.4.3 pytest-django==4.7.0 pytest-cov==4.1.0
pip install beautifulsoup4==4.12.2 openpyxl==3.1.2
pip install python-decouple==3.8 gunicorn==21.2.0 whitenoise==6.6.0
pip install django-crispy-forms==2.1 crispy-bootstrap5==0.7

# Instalar psycopg2-binary (versão mais recente)
pip install psycopg2-binary

# Instalar Pillow (versão mais recente)
pip install Pillow

# Configurar banco de dados
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

## 🎯 Como Usar

### Desenvolvimento Local

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Docker

```bash
# Executar com Docker
docker-compose up --build
```

## 📋 Funcionalidades

- ✅ Importação de dados de arquivos HTML
- ✅ CRUD para processos e partes
- ✅ Exportação para Excel
- ✅ Autenticação de usuários
- ✅ Testes com pytest
- ✅ Ambiente Docker configurado
- ✅ Compatível com Python 3.13

## 🔍 Verificação

Para verificar se tudo está funcionando:

```bash
# Testar se o servidor inicia
python manage.py runserver --noreload

# Em outro terminal, testar a conexão
curl http://localhost:8000/
```

## 📝 Notas Importantes

- O projeto foi testado e funciona com Python 3.13
- As dependências problemáticas (psycopg2-binary e Pillow) são instaladas automaticamente com versões compatíveis
- O script `setup_python313.sh` é específico para Python 3.13 e resolve automaticamente os problemas de compatibilidade

## 🆘 Suporte

Se ainda enfrentar problemas:

1. Verifique se está usando Python 3.13: `python3 --version`
2. Execute o script específico: `./setup_python313.sh`
3. Verifique os logs de erro para problemas específicos
4. Considere usar Docker como alternativa: `docker-compose up --build` 