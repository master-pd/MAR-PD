#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Test Script - Safe UserBot
Test all bot features before production
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class BotTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def log_test(self, test_name, passed, message=""):
        """টেস্ট রেজাল্ট লগ"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message
        }
        self.results.append(result)
        
        if passed:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASS")
        else:
            self.tests_failed += 1
            print(f"❌ {test_name}: FAIL - {message}")
    
    async def test_config_loading(self):
        """কনফিগ লোডিং টেস্ট"""
        try:
            from config import ConfigManager
            config = ConfigManager()
            
            # Check required fields
            assert 'bot_info' in config.config
            assert 'telegram' in config.config
            assert 'api_id' in config.config['telegram']
            assert 'api_hash' in config.config['telegram']
            
            self.log_test("Config Loading", True)
            return True
        except Exception as e:
            self.log_test("Config Loading", False, str(e))
            return False
    
    async def test_response_handler(self):
        """রেসপন্স হ্যান্ডলার টেস্ট"""
        try:
            # Mock config
            mock_config = MagicMock()
            mock_config.get_response_file.return_value = 'data/default.json'
            
            from core.response_handler import ResponseHandler
            handler = ResponseHandler(mock_config)
            
            # Test loading
            assert 'default' in handler.responses
            
            self.log_test("Response Handler", True)
            return True
        except Exception as e:
            self.log_test("Response Handler", False, str(e))
            return False
    
    async def test_json_files(self):
        """JSON ফাইল টেস্ট"""
        json_files = [
            'data/default.json',
            'data/namaz.json',
            'data/slot.json',
            'data/quotes.json',
            'data/duas.json'
        ]
        
        all_valid = True
        for file in json_files:
            try:
                if os.path.exists(file):
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.log_test(f"JSON: {file}", True)
                else:
                    self.log_test(f"JSON: {file}", False, "File not found")
                    all_valid = False
            except Exception as e:
                self.log_test(f"JSON: {file}", False, str(e))
                all_valid = False
        
        return all_valid
    
    async def test_directory_structure(self):
        """ডিরেক্টরি স্ট্রাকচার টেস্ট"""
        required_dirs = [
            'data',
            'sessions',
            'logs',
            'core',
            'utils'
        ]
        
        all_exist = True
        for directory in required_dirs:
            if os.path.exists(directory):
                self.log_test(f"Directory: {directory}", True)
            else:
                self.log_test(f"Directory: {directory}", False, "Not found")
                all_exist = False
        
        return all_exist
    
    async def test_imports(self):
        """ইম্পোর্ট টেস্ট"""
        imports_to_test = [
            ('telethon', 'TelegramClient'),
            ('apscheduler', 'scheduler'),
            ('pytz', 'timezone'),
            ('colorlog', 'ColoredFormatter')
        ]
        
        all_imported = True
        for module, item in imports_to_test:
            try:
                __import__(module)
                self.log_test(f"Import: {module}", True)
            except ImportError as e:
                self.log_test(f"Import: {module}", False, str(e))
                all_imported = False
        
        return all_imported
    
    async def test_core_modules(self):
        """কোর মডিউল টেস্ট"""
        modules_to_test = [
            'core.response_handler',
            'core.slot_manager',
            'core.namaz_alert',
            'core.user_manager',
            'utils.helpers',
            'utils.logger'
        ]
        
        all_loaded = True
        for module in modules_to_test:
            try:
                __import__(module)
                self.log_test(f"Module: {module}", True)
            except Exception as e:
                self.log_test(f"Module: {module}", False, str(e))
                all_loaded = False
        
        return all_loaded
    
    async def run_all_tests(self):
        """সব টেস্ট রান"""
        print("🧪 Running Bot Tests...")
        print("="*60)
        
        tests = [
            self.test_config_loading,
            self.test_response_handler,
            self.test_json_files,
            self.test_directory_structure,
            self.test_imports,
            self.test_core_modules
        ]
        
        for test in tests:
            await test()
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        for result in self.results:
            print(f"{result['status']} {result['test']}")
        
        print("\n" + "="*60)
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {(self.tests_passed/(self.tests_passed+self.tests_failed))*100:.1f}%")
        
        if self.tests_failed == 0:
            print("\n🎉 All tests passed! Bot is ready.")
            return True
        else:
            print("\n⚠️  Some tests failed. Check above for details.")
            return False

async def main():
    """মেইন টেস্ট"""
    tester = BotTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🚀 Bot is ready for production!")
        print("\nNext steps:")
        print("1. python main.py (to start bot)")
        print("2. Send 'hello' to test")
        print("3. Check logs for any issues")
    else:
        print("\n🔧 Fix the failed tests before running the bot.")
    
    return success

if __name__ == "__main__":
    # Run tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        success = loop.run_until_complete(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted")
        sys.exit(1)
    finally:
        loop.close()