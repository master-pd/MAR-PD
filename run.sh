#!/bin/bash

# Safe UserBot - Run Script
# For Linux and Mac systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_warning "Running as root is not recommended. Consider using a regular user."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 7 ]); then
    print_error "Python 3.7+ required. Found Python $python_version"
    exit 1
fi
print_success "Python $python_version detected"

# Check virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install/update dependencies
print_status "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed/updated"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Check for config.py
if [ ! -f "config.py" ]; then
    print_error "config.py not found. Please run setup.py first"
    exit 1
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p data sessions logs backups
print_success "Directories created"

# Set permissions
print_status "Setting permissions..."
chmod 755 .
chmod 644 *.py
chmod 600 sessions/* 2>/dev/null || true
chmod 644 data/*.json 2>/dev/null || true
chmod 755 logs/
print_success "Permissions set"

# Check disk space
print_status "Checking disk space..."
disk_space=$(df -h . | awk 'NR==2 {print $4}')
print_success "Available disk space: $disk_space"

# Check memory
print_status "Checking system resources..."
total_mem=$(free -h | awk 'NR==2 {print $2}')
available_mem=$(free -h | awk 'NR==2 {print $7}')
print_success "Memory: $available_mem available of $total_mem"

# Backup existing session if exists
if [ -f "sessions/main_account.session" ]; then
    print_status "Backing up existing session..."
    backup_dir="backups/sessions"
    mkdir -p "$backup_dir"
    cp "sessions/main_account.session" "$backup_dir/main_account_$(date +%Y%m%d_%H%M%S).session"
    print_success "Session backed up"
fi

# Run the bot
print_status "Starting Safe UserBot..."
echo "========================================="
echo "🚀 Safe UserBot - Professional & Safe"
echo "👨‍💻 Developer: RANA"
echo "📧 Contact: ranaeditz333@gmail.com"
echo "========================================="
echo ""

# Set Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Run with auto-restart
while true; do
    print_status "Launching bot..."
    if python3 main.py; then
        print_success "Bot stopped normally"
        break
    else
        exit_code=$?
        print_error "Bot crashed with exit code $exit_code"
        
        # Check if it's a session error
        if [ $exit_code -eq 2 ]; then
            print_warning "Session error detected. Trying to recover..."
            rm -f sessions/main_account.session 2>/dev/null
        fi
        
        # Ask if user wants to restart
        print_status "Bot crashed. Restarting in 5 seconds..."
        echo "Press Ctrl+C twice to stop"
        
        # Countdown
        for i in {5..1}; do
            echo -ne "Restarting in $i seconds...\r"
            sleep 1
        done
        echo -ne "Restarting now...                    \r"
        echo ""
    fi
done

print_success "Bot stopped"
deactivate