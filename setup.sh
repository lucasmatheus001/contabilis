#!/bin/bash

# Legal Processes Management System Setup Script
# This script sets up the Django project with all necessary configurations

echo "🚀 Setting up Legal Processes Management System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version detected: $PYTHON_VERSION"

# Check if Python version is compatible
if [[ $(echo "$PYTHON_VERSION >= 3.11" | bc -l) -eq 0 ]]; then
    echo "❌ Python version $PYTHON_VERSION is not supported. Please use Python 3.11+"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. You can still run the project locally."
fi

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

# Install dependencies with fallback options
echo "📚 Installing Python dependencies..."
pip install Django==4.2.7 pytest==7.4.3 pytest-django==4.7.0 pytest-cov==4.1.0 beautifulsoup4==4.12.2 openpyxl==3.1.2 python-decouple==3.8 gunicorn==21.2.0 whitenoise==6.6.0 django-crispy-forms==2.1 crispy-bootstrap5==0.7

# Try to install psycopg2-binary, fallback to psycopg2 if needed
echo "📦 Installing psycopg2..."
if ! pip install psycopg2-binary==2.9.9; then
    echo "⚠️  psycopg2-binary failed, trying psycopg2..."
    pip install psycopg2==2.9.9
fi

# Try to install Pillow with different versions if needed
echo "📦 Installing Pillow..."
if ! pip install Pillow==10.2.0; then
    echo "⚠️  Pillow 10.2.0 failed, trying latest version..."
    pip install Pillow
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