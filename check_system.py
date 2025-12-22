#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System Check Script - Safe UserBot
Check if system is ready for the bot
"""

import os
import sys
import platform
import shutil
from datetime import datetime

class SystemChecker:
    def __init__(self):
        self.results = {
            'python': {'status': '❌', 'message': ''},
            'files': {'status': '❌', 'message': ''},
            'dependencies': {'status': '❌', 'message': ''},
            'directories': {'status': '❌', 'message': ''},
            'permissions': {'status': '❌', 'message': ''},
            'resources': {'status': '❌', 'message': ''}
        }
    
    def check_python(self):
        """পাইথন চেক"""
        try:
            version = sys.version_info
            if version.major == 3 and version.minor >= 7:
                self.results['python']['status'] = '✅'
                self.results['python']['message'] = f'Python {version.major}.{version.minor}.{version.micro}'
            else:
                self.results['python']['status'] = '❌'
                self.results['python']['message'] = f'Python 3.7+ required, found {version.major}.{version.minor}'
        except:
            self.results['python']['status'] = '❌'
            self.results['python']['message'] = 'Python not found'
    
    def check_files(self):
        """ফাইলস চেক"""
        required_files = [
            'main.py',
            'config.py',
            'requirements.txt',
            'data/config.json'
        ]
        
        missing = []
        for file in required_files:
            if not os.path.exists(file):
                missing.append(file)
        
        if not missing:
            self.results['files']['status'] = '✅'
            self.results['files']['message'] = 'All required files found'
        else:
            self.results['files']['status'] = '❌'
            self.results['files']['message'] = f'Missing: {", ".join(missing)}'
    
    def check_dependencies(self):
        """ডিপেন্ডেন্সি চেক"""
        try:
            import telethon
            import apscheduler
            import pytz
            
            self.results['dependencies']['status'] = '✅'
            self.results['dependencies']['message'] = 'All dependencies found'
        except ImportError as e:
            self.results['dependencies']['status'] = '❌'
            self.results['dependencies']['message'] = f'Missing: {e.name}'
    
    def check_directories(self):
        """ডিরেক্টরি চেক"""
        required_dirs = ['data', 'sessions', 'logs', 'backups']
        missing = []
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                missing.append(directory)
        
        if not missing:
            self.results['directories']['status'] = '✅'
            self.results['directories']['message'] = 'All directories exist'
        else:
            self.results['directories']['status'] = '❌'
            self.results['directories']['message'] = f'Missing: {", ".join(missing)}'
    
    def check_permissions(self):
        """পারমিশন চেক"""
        try:
            # Check write permissions
            test_file = 'test_permission.tmp'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            self.results['permissions']['status'] = '✅'
            self.results['permissions']['message'] = 'Write permissions OK'
        except:
            self.results['permissions']['status'] = '❌'
            self.results['permissions']['message'] = 'No write permission'
    
    def check_resources(self):
        """রিসোর্সেস চেক"""
        try:
            import psutil
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk
            disk = psutil.disk_usage('.')
            disk_percent = disk.percent
            
            message = f'CPU: {cpu_percent}%, RAM: {memory_percent}%, Disk: {disk_percent}%'
            
            if cpu_percent < 90 and memory_percent < 90 and disk_percent < 90:
                self.results['resources']['status'] = '✅'
                self.results['resources']['message'] = message
            else:
                self.results['resources']['status'] = '⚠️'
                self.results['resources']['message'] = f'High usage: {message}'
                
        except ImportError:
            self.results['resources']['status'] = 'ℹ️'
            self.results['resources']['message'] = 'Install psutil for detailed info'
        except:
            self.results['resources']['status'] = '❌'
            self.results['resources']['message'] = 'Cannot check resources'
    
    def run_all_checks(self):
        """সব চেক রান"""
        print("🔍 Running system checks...\n")
        
        self.check_python()
        self.check_files()
        self.check_dependencies()
        self.check_directories()
        self.check_permissions()
        self.check_resources()
        
        # Print results
        for check, result in self.results.items():
            print(f"{result['status']} {check.upper():12} {result['message']}")
        
        # Summary
        print("\n" + "="*50)
        passed = sum(1 for r in self.results.values() if r['status'] == '✅')
        total = len(self.results)
        
        print(f"📊 Summary: {passed}/{total} checks passed")
        
        if passed == total:
            print("✅ System is ready for Safe UserBot!")
        else:
            print("❌ System needs configuration")
            print("\n💡 Recommendations:")
            
            if self.results['python']['status'] == '❌':
                print("  • Install Python 3.7 or higher")
            
            if self.results['files']['status'] == '❌':
                print("  • Run setup.py to create missing files")
            
            if self.results['dependencies']['status'] == '❌':
                print("  • Run: pip install -r requirements.txt")
            
            if self.results['directories']['status'] == '❌':
                print("  • Create missing directories manually")
            
            if self.results['permissions']['status'] == '❌':
                print("  • Run as administrator or fix permissions")
        
        return passed == total

def main():
    """মেইন ফাংশন"""
    print("="*50)
    print("SYSTEM CHECK - SAFE USERBOT")
    print("="*50)
    
    checker = SystemChecker()
    is_ready = checker.run_all_checks()
    
    print("\n" + "="*50)
    if is_ready:
        print("🚀 Ready to launch! Run: python main.py")
    else:
        print("🔧 Fix issues above, then run again")
    
    print("="*50)

if __name__ == "__main__":
    main()