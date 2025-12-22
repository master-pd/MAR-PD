#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
লগ ক্লিনআপ স্ক্রিপ্ট - Safe UserBot
"""

import os
import sys
import glob
from datetime import datetime, timedelta
import argparse

def cleanup_logs(days_to_keep=7, log_type=None, dry_run=False):
    """পুরোনো লগ ফাইল ক্লিনআপ"""
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        print(f"❌ Log directory '{log_dir}' not found")
        return
    
    # কতদিনের পুরোনো ফাইল কিপ করবে
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    # লগ ফাইল প্যাটার্ন
    patterns = []
    if log_type:
        if log_type == 'all':
            patterns = ['*.log']
        elif log_type == 'bot':
            patterns = ['bot_*.log']
        elif log_type == 'errors':
            patterns = ['errors_*.log']
        elif log_type == 'admin':
            patterns = ['admin_*.log']
        elif log_type == 'users':
            patterns = ['users_*.log']
    else:
        patterns = ['*.log']
    
    deleted_count = 0
    kept_count = 0
    total_size = 0
    
    print(f"🔧 Cleaning up logs older than {days_to_keep} days")
    print(f"📁 Log directory: {log_dir}")
    print(f"📊 Log type: {log_type or 'all'}")
    print(f"🔍 Dry run: {'Yes' if dry_run else 'No'}")
    print("=" * 50)
    
    for pattern in patterns:
        log_files = glob.glob(os.path.join(log_dir, pattern))
        
        for log_file in log_files:
            try:
                # ফাইল স্ট্যাটস
                stat = os.stat(log_file)
                file_date = datetime.fromtimestamp(stat.st_mtime)
                file_size = stat.st_size
                
                # ফাইলনেম থেকে ডেট পার্স করার চেষ্টা
                filename = os.path.basename(log_file)
                date_str = None
                
                # প্যাটার্ন ম্যাচিং: bot_20241222.log
                import re
                date_match = re.search(r'(\d{8})\.log$', filename)
                if date_match:
                    date_str = date_match.group(1)
                    try:
                        file_date = datetime.strptime(date_str, '%Y%m%d')
                    except:
                        pass  # ফাইল মডিফিকেশন ডেট ব্যবহার
                
                # পুরোনো ফাইল চেক
                if file_date < cutoff_date:
                    total_size += file_size
                    
                    if dry_run:
                        print(f"🗑️  [DRY RUN] Would delete: {filename}")
                        print(f"   Date: {file_date.strftime('%Y-%m-%d')}, Size: {file_size:,} bytes")
                        deleted_count += 1
                    else:
                        try:
                            os.remove(log_file)
                            print(f"✅ Deleted: {filename}")
                            print(f"   Date: {file_date.strftime('%Y-%m-%d')}, Size: {file_size:,} bytes")
                            deleted_count += 1
                        except Exception as e:
                            print(f"❌ Failed to delete {filename}: {e}")
                else:
                    kept_count += 1
                    
            except Exception as e:
                print(f"❌ Error processing {log_file}: {e}")
    
    # রিপোর্ট
    print("=" * 50)
    print(f"📊 Cleanup Report:")
    print(f"✅ Kept files: {kept_count}")
    print(f"🗑️  Deleted files: {deleted_count}")
    
    if deleted_count > 0:
        size_mb = total_size / (1024 * 1024)
        print(f"💾 Space freed: {size_mb:.2f} MB")
    
    if dry_run:
        print(f"💡 Note: This was a dry run. No files were actually deleted.")
    
    # বর্তমান লগ স্ট্যাটস
    print("\n📁 Current log files:")
    current_logs = glob.glob(os.path.join(log_dir, '*.log'))
    if current_logs:
        for log_file in sorted(current_logs):
            stat = os.stat(log_file)
            size_kb = stat.st_size / 1024
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            age_days = (datetime.now() - mod_time).days
            
            age_str = f"{age_days} day{'s' if age_days != 1 else ''} old"
            print(f"  {os.path.basename(log_file)} - {size_kb:.1f} KB - {age_str}")
    else:
        print("  No log files found")
    
    return deleted_count, total_size

def compress_logs(days_to_compress=30):
    """লগ ফাইলস কম্প্রেস"""
    print(f"🗜️  Compressing logs older than {days_to_compress} days...")
    
    # কম্প্রেশন লজিক এখানে যোগ করতে পারেন
    # যেমন: tar.gz এ আর্কাইভ করা
    
    print("💡 Log compression feature coming soon!")
    return 0

def main():
    """মেইন ফাংশন"""
    parser = argparse.ArgumentParser(description='Clean up old log files')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days to keep logs (default: 7)')
    parser.add_argument('--type', choices=['all', 'bot', 'errors', 'admin', 'users'],
                       default='all', help='Type of logs to clean up')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--compress', action='store_true',
                       help='Compress old logs instead of deleting')
    parser.add_argument('--compress-days', type=int, default=30,
                       help='Days after which to compress logs')
    
    args = parser.parse_args()
    
    print("🧹 Log Cleanup Tool - Safe UserBot")
    print("=" * 50)
    
    if args.compress:
        compress_logs(args.compress_days)
    else:
        cleanup_logs(args.days, args.type, args.dry_run)
    
    print("\n✅ Cleanup completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)