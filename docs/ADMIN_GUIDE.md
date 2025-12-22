# 👨‍💼 এডমিন গাইড - Safe UserBot

## 🔐 এডমিন এক্সেস

### এডমিন যোগ করার উপায়:
1. `data/admins.json` ফাইল এডিট করুন
2. আপনার Telegram ID যোগ করুন:
```json
{
  "admins": [123456789, 987654321],
  "permissions": {
    "can_edit_responses": true,
    "can_edit_times": true
  }
}

# রেসপন্স ম্যানেজমেন্ট
```bash
/add_response hello "Hello there! 😊"
/edit_response thanks "You're welcome! 👍"
/delete_response goodbye
/list_responses

# 🕌 নামাজের সময়
```bash
/set_namaz Fajr 05:15
/set_namaz Dhuhr 12:45
/view_namaz_times

# ⏰ স্লট ম্যানেজমেন্ট
bash
/add_slot morning 06:00 09:00 "Good morning! 🌞"
/edit_slot morning message "Start your day with Fajr! 🤲"
/delete_slot afternoon

# 📊 ইউজার ম্যানেজমেন্ট
```bash
/user_stats 123456789
/user_history 123456789
/reset_stats 123456789
/block_user 987654321 "Spamming"
/unblock_user 987654321
# 📈 অ্যানালিটিক্স
```bash
/stats_today
/stats_week
/stats_month
/top_users
/activity_report