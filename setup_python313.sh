#!/bin/bash

# Legal Processes Management System Setup Script for Python 3.13
# This script sets up the Django project with Python 3.13 compatible versions

echo "🚀 Setting up Legal Processes Management System for Python 3.13..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version detected: $PYTHON_VERSION"

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install system dependencies for psycopg2 and Pillow
echo "🔧 Installing system dependencies..."
if command -v dnf &> /dev/null; then
    # Fedora/RHEL/CentOS
    sudo dnf install -y python3-devel postgresql-devel libpq-devel gcc
elif command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y python3-dev libpq-dev postgresql-client build-essential
elif command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python-pip postgresql-libs gcc
fi

# Install dependencies one by one with Python 3.13 compatible versions
echo "📚 Installing Python dependencies..."

# Core Django
pip install Django==4.2.7

# Testing dependencies
pip install pytest==7.4.3
pip install pytest-django==4.7.0
pip install pytest-cov==4.1.0

# Data processing
pip install beautifulsoup4==4.12.2
pip install openpyxl==3.1.2

# Configuration
pip install python-decouple==3.8

# Web server
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0

# Forms
pip install django-crispy-forms==2.1
pip install crispy-bootstrap5==0.7

# Database - try multiple approaches
echo "📦 Installing database driver..."
if ! pip install psycopg2-binary==2.9.9; then
    echo "⚠️  psycopg2-binary failed, trying psycopg2..."
    if ! pip install psycopg2==2.9.9; then
        echo "⚠️  psycopg2 failed, trying psycopg2-binary with latest version..."
        pip install psycopg2-binary
    fi
fi

# Image processing - try multiple approaches
echo "📦 Installing Pillow..."
if ! pip install Pillow==10.2.0; then
    echo "⚠️  Pillow 10.2.0 failed, trying latest version..."
    if ! pip install Pillow; then
        echo "⚠️  Pillow failed, trying without version constraint..."
        pip install --no-deps Pillow
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=legal_processes
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
EOF
    echo "✅ .env file created"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superuser already exists or creation failed"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup completed successfully!"
echo ""
echo "🎉 You can now run the project:"
echo "   - Local development: python manage.py runserver"
echo "   - Docker: docker-compose up --build"
echo ""
echo "📖 For more information, see README.md" 