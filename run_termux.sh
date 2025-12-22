#!/data/data/com.termux/files/usr/bin/bash

# Safe UserBot - Termux Run Script
# For Android Termux

clear

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
echo "========================================="
echo "🚀 Safe UserBot - Termux Edition"
echo "📱 Optimized for Android"
echo "👨‍💻 Developer: RANA"
echo "========================================="
echo -e "${NC}"

# Check if running in Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    echo -e "${RED}✗ This script is for Termux only${NC}"
    exit 1
fi

# Update packages
echo -e "${YELLOW}[*] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install dependencies
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
pkg install -y python git wget curl proot

# Check Python
echo -e "${YELLOW}[*] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    pkg install -y python
fi

python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $python_version${NC}"

# Check git
if ! command -v git &> /dev/null; then
    pkg install -y git
fi

# Clone or update repository
if [ -d "SAFE_USERBOT" ]; then
    echo -e "${YELLOW}[*] Updating existing bot...${NC}"
    cd SAFE_USERBOT
    git pull
else
    echo -e "${YELLOW}[*] Cloning repository...${NC}"
    git clone <repository_url> SAFE_USERBOT
    cd SAFE_USERBOT
fi

# Install Python dependencies
echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo -e "${YELLOW}[*] Creating directories...${NC}"
mkdir -p data sessions logs backups

# Set permissions
echo -e "${YELLOW}[*] Setting permissions...${NC}"
chmod 700 sessions
chmod 600 sessions/* 2>/dev/null || true

# Check storage permission
echo -e "${YELLOW}[*] Checking storage permission...${NC}"
if [ ! -d ~/storage ]; then
    echo -e "${BLUE}[!] Granting storage permission...${NC}"
    termux-setup-storage
    sleep 2
fi

# Create backup on external storage
echo -e "${YELLOW}[*] Creating external backup...${NC}"
if [ -d ~/storage/shared/SafeUserBot ]; then
    cp -r data ~/storage/shared/SafeUserBot/backup_$(date +%Y%m%d)
    echo -e "${GREEN}✓ Backup created on external storage${NC}"
fi

# Check battery optimization
echo -e "${YELLOW}[*] Battery optimization tips:${NC}"
echo "1. Go to Settings > Battery > Battery optimization"
echo "2. Find Termux and set to 'Don't optimize'"
echo "3. This prevents Termux from being killed in background"
echo ""

# Check for existing session
if [ -f "sessions/main_account.session" ]; then
    echo -e "${GREEN}✓ Existing session found${NC}"
else
    echo -e "${YELLOW}[!] No session found. First time setup required.${NC}"
fi

# Run bot
echo -e "${BLUE}"
echo "========================================="
echo "🤖 Starting Safe UserBot..."
echo "💡 Keep Termux running in background"
echo "🔋 Disable battery optimization for Termux"
echo "📞 Support: ranaeditz333@gmail.com"
echo "========================================="
echo -e "${NC}"

# Auto-restart loop
while true; do
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] Starting bot...${NC}"
    
    # Run with nohup for background execution
    python main.py
    
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ Bot stopped normally${NC}"
        break
    elif [ $exit_code -eq 2 ]; then
        echo -e "${RED}✗ Session error. Removing session file...${NC}"
        rm -f sessions/main_account.session
    else
        echo -e "${RED}✗ Bot crashed with code $exit_code${NC}"
    fi
    
    echo -e "${YELLOW}[*] Restarting in 15 seconds...${NC}"
    echo "Press Ctrl+C to stop"
    
    # Countdown
    for i in {15..1}; do
        echo -ne "Restarting in $i seconds...\r"
        sleep 1
    done
    echo -ne "                            \r"
done

echo -e "${GREEN}✓ Bot stopped. Goodbye!${NC}"