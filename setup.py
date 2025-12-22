#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
সেটআপ স্ক্রিপ্ট - Safe UserBot
"""

import os
import sys
import json
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SetupWizard:
    def __init__(self):
        self.project_name = "Safe UserBot"
        self.developer = "RANA"
        self.version = "1.0.0"
        
    def clear_screen(self):
        """স্ক্রিন ক্লিয়ার"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """হেডার প্রিন্ট"""
        self.clear_screen()
        print(Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + f"🚀 {self.project_name} - Setup Wizard")
        print(Fore.CYAN + "=" * 60)
        print(Fore.GREEN + f"👨‍💻 Developer: {self.developer}")
        print(Fore.GREEN + f"📦 Version: {self.version}")
        print(Fore.CYAN + "=" * 60)
        print()
    
    def check_python_version(self):
        """পাইথন ভার্সন চেক"""
        print(Fore.BLUE + "🔍 Checking Python version...")
        
        if sys.version_info < (3, 7):
            print(Fore.RED + f"❌ Python 3.7+ required. You have {sys.version}")
            print(Fore.YELLOW + "💡 Please install Python 3.7 or higher")
            return False
        
        print(Fore.GREEN + f"✅ Python {sys.version} detected")
        return True
    
    def check_requirements(self):
        """রিকোয়ারমেন্টস চেক"""
        print(Fore.BLUE + "\n🔍 Checking requirements.txt...")
        
        if not os.path.exists("requirements.txt"):
            print(Fore.RED + "❌ requirements.txt not found")
            return False
        
        print(Fore.GREEN + "✅ requirements.txt found")
        return True
    
    def install_dependencies(self):
        """ডিপেন্ডেন্সি ইন্সটল"""
        print(Fore.BLUE + "\n📦 Installing dependencies...")
        
        try:
            import subprocess
            
            # Install requirements
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(Fore.GREEN + "✅ Dependencies installed successfully")
                return True
            else:
                print(Fore.RED + f"❌ Failed to install dependencies:\n{result.stderr}")
                return False
                
        except Exception as e:
            print(Fore.RED + f"❌ Error installing dependencies: {e}")
            return False
    
    def get_api_credentials(self):
        """API ক্রিডেনশিয়াল নিন"""
        print(Fore.BLUE + "\n🔑 Telegram API Configuration")
        print(Fore.YELLOW + "💡 Get API ID and Hash from: https://my.telegram.org")
        print()
        
        api_id = input(Fore.CYAN + "Enter API ID: " + Style.RESET_ALL)
        api_hash = input(Fore.CYAN + "Enter API Hash: " + Style.RESET_ALL)
        
        if not api_id or not api_hash:
            print(Fore.RED + "❌ API credentials cannot be empty")
            return None, None
        
        return api_id, api_hash
    
    def get_bot_info(self):
        """বট ইনফো নিন"""
        print(Fore.BLUE + "\n🤖 Bot Information")
        
        bot_name = input(Fore.CYAN + "Bot Name (default: Safe UserBot): " + Style.RESET_ALL)
        if not bot_name:
            bot_name = "Safe UserBot"
        
        developer = input(Fore.CYAN + "Developer Name (default: RANA): " + Style.RESET_ALL)
        if not developer:
            developer = "RANA"
        
        timezone = input(Fore.CYAN + "Timezone (default: Asia/Dhaka): " + Style.RESET_ALL)
        if not timezone:
            timezone = "Asia/Dhaka"
        
        language = input(Fore.CYAN + "Language (default: bn): " + Style.RESET_ALL)
        if not language:
            language = "bn"
        
        return {
            'name': bot_name,
            'developer': developer,
            'timezone': timezone,
            'language': language
        }
    
    def configure_settings(self):
        """সেটিংস কনফিগার"""
        print(Fore.BLUE + "\n⚙️ Bot Settings Configuration")
        
        settings = {
            'human_delay': 1.5,
            'max_retries': 3,
            'log_level': 'INFO'
        }
        
        print(Fore.YELLOW + "Default settings:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
        
        change = input(Fore.CYAN + "\nChange default settings? (yes/no): " + Style.RESET_ALL)
        
        if change.lower() == 'yes':
            try:
                delay = input(Fore.CYAN + f"Human delay (default: {settings['human_delay']}): " + Style.RESET_ALL)
                if delay:
                    settings['human_delay'] = float(delay)
                
                retries = input(Fore.CYAN + f"Max retries (default: {settings['max_retries']}): " + Style.RESET_ALL)
                if retries:
                    settings['max_retries'] = int(retries)
                
                log_level = input(Fore.CYAN + f"Log level (default: {settings['log_level']}): " + Style.RESET_ALL)
                if log_level:
                    settings['log_level'] = log_level
                    
            except ValueError:
                print(Fore.RED + "❌ Invalid input, using defaults")
        
        return settings
    
    def enable_features(self):
        """ফিচারস এনাবল"""
        print(Fore.BLUE + "\n✨ Features Configuration")
        
        features = {
            'auto_reply': True,
            'namaz_alert': True,
            'slot_reminders': True,
            'quotes_enabled': True,
            'duas_enabled': True,
            'developer_info': True
        }
        
        print(Fore.YELLOW + "Available features:")
        for feature, enabled in features.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            print(f"  {feature}: {status}")
        
        change = input(Fore.CYAN + "\nConfigure features? (yes/no): " + Style.RESET_ALL)
        
        if change.lower() == 'yes':
            for feature in features:
                current = "Y" if features[feature] else "N"
                response = input(Fore.CYAN + f"Enable {feature}? (current: {current}) (y/n): " + Style.RESET_ALL)
                if response.lower() == 'y':
                    features[feature] = True
                elif response.lower() == 'n':
                    features[feature] = False
        
        return features
    
    def create_directories(self):
        """ডিরেক্টরি তৈরি"""
        print(Fore.BLUE + "\n📁 Creating directories...")
        
        directories = [
            'data',
            'sessions',
            'logs',
            'backups',
            'media/photos',
            'media/stickers',
            'media/audio',
            'core',
            'utils',
            'admin',
            'notifications',
            'analytics',
            'plugins',
            'docs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(Fore.GREEN + f"✅ Created: {directory}")
        
        return True
    
    def create_config_file(self, api_id, api_hash, bot_info, settings, features):
        """কনফিগ ফাইল তৈরি"""
        print(Fore.BLUE + "\n💾 Creating configuration file...")
        
        config = {
            "bot_info": {
                "name": bot_info['name'],
                "developer": bot_info['developer'],
                "version": self.version
            },
            "settings": {
                "timezone": bot_info['timezone'],
                "language": bot_info['language'],
                "human_delay": settings['human_delay'],
                "max_retries": settings['max_retries'],
                "log_level": settings['log_level']
            },
            "features": features,
            "telegram": {
                "api_id": int(api_id),
                "api_hash": api_hash
            }
        }
        
        try:
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write('import json\n')
                f.write('import os\n')
                f.write('from datetime import datetime\n\n')
                f.write('class ConfigManager:\n')
                f.write('    def __init__(self):\n')
                f.write('        self.base_dir = os.path.dirname(os.path.abspath(__file__))\n')
                f.write('        self.data_dir = os.path.join(self.base_dir, \'data\')\n')
                f.write('        self.config_file = os.path.join(self.data_dir, \'config.json\')\n')
                f.write('        \n')
                f.write('        # Create directories if not exist\n')
                f.write('        os.makedirs(self.data_dir, exist_ok=True)\n')
                f.write('        \n')
                f.write('        # লোড কনফিগারেশন\n')
                f.write('        self.config = self._load_config()\n')
                f.write('    \n')
                f.write('    def _load_config(self):\n')
                f.write('        """JSON থেকে কনফিগারেশন লোড"""\n')
                f.write('        default_config = ')
                f.write(json.dumps(config, indent=8, ensure_ascii=False))
                f.write('\n        \n')
                f.write('        if os.path.exists(self.config_file):\n')
                f.write('            try:\n')
                f.write('                with open(self.config_file, \'r\', encoding=\'utf-8\') as f:\n')
                f.write('                    return json.load(f)\n')
                f.write('            except:\n')
                f.write('                print("Config file corrupted, creating new one")\n')
                f.write('                return self._create_default_config(default_config)\n')
                f.write('        else:\n')
                f.write('            return self._create_default_config(default_config)\n')
                f.write('    \n')
                f.write('    def _create_default_config(self, default_config):\n')
                f.write('        """ডিফল্ট কনফিগারেশন তৈরি"""\n')
                f.write('        self._save_config(default_config)\n')
                f.write('        return default_config\n')
                f.write('    \n')
                f.write('    def _save_config(self, config):\n')
                f.write('        """কনফিগারেশন সেভ"""\n')
                f.write('        with open(self.config_file, \'w\', encoding=\'utf-8\') as f:\n')
                f.write('            json.dump(config, f, indent=4, ensure_ascii=False)\n')
                f.write('    \n')
                f.write('    def get_response_file(self, file_type):\n')
                f.write('        """রেসপন্স ফাইল পাথ রিটার্ন"""\n')
                f.write('        files = {\n')
                f.write('            "default": "default.json",\n')
                f.write('            "extra": "extra_responses.json",\n')
                f.write('            "namaz": "namaz.json",\n')
                f.write('            "slot": "slot.json",\n')
                f.write('            "users": "users.json",\n')
                f.write('            "quotes": "quotes.json",\n')
                f.write('            "duas": "duas.json",\n')
                f.write('            "media": "media.json",\n')
                f.write('            "events": "events.json",\n')
                f.write('            "announcements": "announcements.json"\n')
                f.write('        }\n')
                f.write('        \n')
                f.write('        if file_type in files:\n')
                f.write('            file_path = os.path.join(self.data_dir, files[file_type])\n')
                f.write('            # ফাইল না থাকলে তৈরি করবে\n')
                f.write('            if not os.path.exists(file_path):\n')
                f.write('                self.create_default_json(file_type)\n')
                f.write('            return file_path\n')
                f.write('        return None\n')
                f.write('    \n')
                f.write('    def create_default_json(self, file_type):\n')
                f.write('        """ডিফল্ট JSON ফাইল তৈরি"""\n')
                f.write('        default_data = {\n')
                f.write('            "default": {\n')
                f.write('                "hello": ["Hi! 👋", "Hello! 😃", "Assalamu Alaikum! 🤲"],\n')
                f.write('                "how are you": ["I\'m fine, alhamdulillah!", "All good by Allah\'s grace!"]\n')
                f.write('            },\n')
                f.write('            "extra": {\n')
                f.write('                "good morning": ["Good morning 🌞", "Morning! Hope you slept well 😴"],\n')
                f.write('                "good night": ["Good night 🌙", "Sleep tight! 🌟"]\n')
                f.write('            },\n')
                f.write('            "namaz": {\n')
                f.write('                "Fajr": "05:00",\n')
                f.write('                "Dhuhr": "12:30",\n')
                f.write('                "Asr": "15:45",\n')
                f.write('                "Maghrib": "18:20",\n')
                f.write('                "Isha": "19:40"\n')
                f.write('            },\n')
                f.write('            "slot": {\n')
                f.write('                "slots": [\n')
                f.write('                    {\n')
                f.write('                        "name": "morning",\n')
                f.write('                        "start": "06:00",\n')
                f.write('                        "end": "09:00",\n')
                f.write('                        "level1": "Good morning! 🌞",\n')
                f.write('                        "level2": "Time to start your work ⏰",\n')
                f.write('                        "level3": "Don\'t forget your morning routine!"\n')
                f.write('                    }\n')
                f.write('                ]\n')
                f.write('            },\n')
                f.write('            "users": {},\n')
                f.write('            "quotes": {\n')
                f.write('                "quotes": [\n')
                f.write('                    "The best among you are those who have the best manners.",\n')
                f.write('                    "Patience is the key to success."\n')
                f.write('                ]\n')
                f.write('            },\n')
                f.write('            "duas": {\n')
                f.write('                "duas": [\n')
                f.write('                    "O Allah, guide me to the straight path.",\n')
                f.write('                    "Grant me patience and strength."\n')
                f.write('                ]\n')
                f.write('            },\n')
                f.write('            "media": {\n')
                f.write('                "emojis": ["😊", "👍", "❤️", "🤲", "🌙", "☀️"],\n')
                f.write('                "stickers": []\n')
                f.write('            },\n')
                f.write('            "events": {},\n')
                f.write('            "announcements": {}\n')
                f.write('        }\n')
                f.write('        \n')
                f.write('        if file_type in default_data:\n')
                f.write('            file_path = os.path.join(self.data_dir, f"{file_type}.json")\n')
                f.write('            with open(file_path, \'w\', encoding=\'utf-8\') as f:\n')
                f.write('                json.dump(default_data[file_type], f, indent=4, ensure_ascii=False)\n')
                f.write('    \n')
                f.write('    def get_telegram_creds(self):\n')
                f.write('        """টেলিগ্রাম ক্রিডেনশিয়াল"""\n')
                f.write('        return (\n')
                f.write('            self.config[\'telegram\'][\'api_id\'],\n')
                f.write('            self.config[\'telegram\'][\'api_hash\']\n')
                f.write('        )\n')
            
            print(Fore.GREEN + "✅ config.py created successfully")
            return True
            
        except Exception as e:
            print(Fore.RED + f"❌ Error creating config.py: {e}")
            return False
    
    def create_requirements_file(self):
        """রিকোয়ারমেন্টস ফাইল তৈরি"""
        print(Fore.BLUE + "\n📦 Creating requirements.txt...")
        
        requirements = """telethon==1.28.1
apscheduler==3.10.1
pytz==2022.7
python-dotenv==1.0.0
colorlog==6.7.0
colorama==0.4.6
requests==2.31.0"""
        
        try:
            with open('requirements.txt', 'w', encoding='utf-8') as f:
                f.write(requirements)
            
            print(Fore.GREEN + "✅ requirements.txt created successfully")
            return True
            
        except Exception as e:
            print(Fore.RED + f"❌ Error creating requirements.txt: {e}")
            return False
    
    def create_main_file(self):
        """মেইন ফাইল তৈরি"""
        print(Fore.BLUE + "\n🤖 Creating main bot file...")
        
        # We'll create a simplified version for setup
        # Full main.py will be created by the main script
        
        main_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SAFE USERBOT - Setup Complete
Run setup.py first to configure the bot
"""

print("🚀 Safe UserBot Setup Complete!")
print("📁 Please run the main bot script:")
print("python main.py")
print()
print("📞 For support:")
print("Email: ranaeditz333@gmail.com")
print("Telegram: @rana_editz_00")
'''
        
        try:
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write(main_content)
            
            print(Fore.GREEN + "✅ main.py created successfully")
            return True
            
        except Exception as e:
            print(Fore.RED + f"❌ Error creating main.py: {e}")
            return False
    
    def run_wizard(self):
        """সেটআপ উইজার্ড রান"""
        self.print_header()
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Check/create requirements
        if not self.check_requirements():
            if not self.create_requirements_file():
                return False
        
        # Step 3: Install dependencies
        if not self.install_dependencies():
            retry = input(Fore.YELLOW + "Retry installation? (yes/no): " + Style.RESET_ALL)
            if retry.lower() != 'yes':
                return False
            self.install_dependencies()
        
        # Step 4: Get API credentials
        api_id, api_hash = self.get_api_credentials()
        if not api_id or not api_hash:
            return False
        
        # Step 5: Get bot info
        bot_info = self.get_bot_info()
        
        # Step 6: Configure settings
        settings = self.configure_settings()
        
        # Step 7: Enable features
        features = self.enable_features()
        
        # Step 8: Create directories
        if not self.create_directories():
            return False
        
        # Step 9: Create config file
        if not self.create_config_file(api_id, api_hash, bot_info, settings, features):
            return False
        
        # Step 10: Create main file
        if not self.create_main_file():
            return False
        
        # Success message
        self.print_header()
        print(Fore.GREEN + "🎉 Setup Completed Successfully!")
        print()
        print(Fore.YELLOW + "📋 Next Steps:")
        print(Fore.CYAN + "1. Run the bot:" + Fore.WHITE + " python main.py")
        print(Fore.CYAN + "2. Enter your phone number when prompted")
        print(Fore.CYAN + "3. Enter the verification code")
        print(Fore.CYAN + "4. The bot will start automatically")
        print()
        print(Fore.YELLOW + "🔧 Configuration Files:")
        print(Fore.WHITE + "• config.py - Main configuration")
        print(Fore.WHITE + "• data/ - All JSON response files")
        print(Fore.WHITE + "• sessions/ - Telegram session files")
        print()
        print(Fore.YELLOW + "📞 Support:")
        print(Fore.WHITE + "• Email: ranaeditz333@gmail.com")
        print(Fore.WHITE + "• Telegram: @rana_editz_00")
        print(Fore.WHITE + "• Phone: 01847634486")
        print()
        print(Fore.CYAN + "=" * 60)
        print(Fore.GREEN + "🚀 Your Safe UserBot is ready to go!")
        print(Fore.CYAN + "=" * 60)
        
        return True

if __name__ == "__main__":
    wizard = SetupWizard()
    
    try:
        success = wizard.run_wizard()
        if not success:
            print(Fore.RED + "\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {e}")
        sys.exit(1)