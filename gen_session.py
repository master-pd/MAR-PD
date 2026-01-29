from pyrogram import Client

API_ID = 28356317  # নতুন account এর জন্য API_ID
API_HASH = "60d7f5663898a5d855ac4aceab4315e6"  # নতুন account এর জন্য API_HASH

with Client(
    "session",
    api_id=API_ID,
    api_hash=API_HASH
) as app:
    print("\n✅ SESSION STRING:\n")
    print(app.export_session_string())
