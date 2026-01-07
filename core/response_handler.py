import json
import os
import random
import re
from utils.helpers import JSONHelper, TextHelper
from config import ConfigManager

class ResponseHandler:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.responses = {}
        self.load_responses_from_master()

    # Master JSON অনুযায়ী সব ফাইল load করা
    def load_responses_from_master(self):
        master_path = self.config.get_master_file()
        if not os.path.exists(master_path):
            print(f"[ERROR] Master file not found: {master_path}")
            return

        with open(master_path, "r", encoding="utf-8") as f:
            master_data = json.load(f)

        for filename in master_data.get("responses", []):
            file_path = os.path.join(self.config.data_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as rf:
                    self.responses[filename] = json.load(rf)
            else:
                print(f"[WARNING] Response file not found: {file_path}")

    # Auto reply
    def get_auto_reply(self, message_text: str):
        message_text = TextHelper.clean_text(message_text)
        for filename, data in self.responses.items():
            for key, responses in data.items():
                if re.search(rf'\b{re.escape(key)}\b', message_text):
                    return JSONHelper.get_random_response(responses)
        # No fallback
        return None

    # Generic methods for quotes, duas, media, events, announcements
    def get_quote(self):
        quotes = self.responses.get('quotes.json', {}).get('quotes', [])
        if quotes:
            return random.choice(quotes)
        return None

    def get_dua(self):
        duas = self.responses.get('duas.json', {}).get('duas', [])
        if duas:
            return random.choice(duas)
        return None

    def get_media(self, media_type: str):
        media = self.responses.get('media.json', {}).get(media_type, [])
        if media:
            return random.choice(media)
        return None

    def get_event_message(self, event_type: str):
        events = self.responses.get('events.json', {}).get(event_type, [])
        if events:
            return JSONHelper.get_random_response(events)
        return None

    def get_announcement(self, ann_type: str):
        announcements = self.responses.get('announcements.json', {}).get(ann_type, [])
        if announcements:
            return JSONHelper.get_random_response(announcements)
        return None
