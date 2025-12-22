# Safe UserBot - Makefile
# For Linux/Mac systems

.PHONY: all install setup test clean backup update deploy help

# Variables
PYTHON = python3
PIP = pip3
BOT_NAME = safe-userbot
VERSION = 1.0.0

# Default target
all: help

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

# Setup bot
setup:
	@echo "🔧 Setting up bot..."
	$(PYTHON) setup.py
	@echo "✅ Setup completed"

# Quick setup
quick-setup:
	@echo "⚡ Quick setup..."
	$(PYTHON) quick_setup.py
	@echo "✅ Quick setup completed"

# Run bot
run:
	@echo "🚀 Starting bot..."
	$(PYTHON) main.py

# Run with auto-restart
run-daemon:
	@echo "🔄 Starting bot with auto-restart..."
	@while true; do \
		$(PYTHON) main.py; \
		echo "Bot stopped. Restarting in 5 seconds..."; \
		sleep 5; \
	done

# Test bot
test:
	@echo "🧪 Running tests..."
	$(PYTHON) test_bot.py

# Check system
check:
	@echo "🔍 Checking system..."
	$(PYTHON) check_system.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -mtime +7 -delete
	rm -f sessions/*.session.bak
	@echo "✅ Cleanup completed"

# Backup bot
backup:
	@echo "💾 Creating backup..."
	$(PYTHON) backup.py
	@echo "✅ Backup created"

# Update bot
update:
	@echo "🔄 Updating bot..."
	$(PYTHON) update.py
	@echo "✅ Update completed"

# Deploy to server
deploy:
	@echo "🌐 Deploying to server..."
	$(PYTHON) deploy_server.py

# Create distribution package
dist:
	@echo "📦 Creating distribution package..."
	mkdir -p dist
	tar -czf dist/$(BOT_NAME)-$(VERSION).tar.gz \
		--exclude="__pycache__" \
		--exclude="*.pyc" \
		--exclude=".git" \
		--exclude="logs/*" \
		--exclude="sessions/*" \
		--exclude="backups/*" \
		--exclude="dist" \
		.
	@echo "✅ Distribution package created: dist/$(BOT_NAME)-$(VERSION).tar.gz"

# Install as system service (Linux)
install-service:
	@echo "🔧 Installing as system service..."
	sudo cp systemd/safe-userbot.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable safe-userbot
	@echo "✅ Service installed. Start with: sudo systemctl start safe-userbot"

# Help
help:
	@echo "🤖 Safe UserBot - Make Commands"
	@echo "================================"
	@echo "install      - Install dependencies"
	@echo "setup        - Run setup wizard"
	@echo "quick-setup  - Quick setup"
	@echo "run          - Run bot"
	@echo "run-daemon   - Run with auto-restart"
	@echo "test         - Run tests"
	@echo "check        - Check system"
	@echo "clean        - Clean temporary files"
	@echo "backup       - Create backup"
	@echo "update       - Update bot"
	@echo "deploy       - Deploy to server"
	@echo "dist         - Create distribution package"
	@echo "install-service - Install as system service"
	@echo "help         - Show this help"