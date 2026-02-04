import json
import os
import asyncio
from datetime import datetime
from aiogram import Bot

LOG_FILE = "user_activity_logs.json"

class ActivityLogger:
    def __init__(self):
        self.logs = self._load_logs()
        
    def _load_logs(self):
        if not os.path.exists(LOG_FILE):
            return {}
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save_logs(self):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=4, ensure_ascii=False)

    async def log_action(self, bot: Bot, user, action: str):
        # Reload logs
        self.logs = self._load_logs()

        channel_id = os.getenv("LOG_CHANNEL_ID")
        print(f"DEBUG: Attempting to log. Channel ID: {channel_id}") 
        
        if not channel_id or "xxxx" in channel_id:
            print("DEBUG: Channel ID invalid or not set.")
            return

        user_id = str(user.id)

        user_id = str(user.id)
        username = f"@{user.username}" if user.username else f"ID: {user_id}"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # New action entry
        new_entry = f"🕒 {timestamp} — {action}"

        user_data = self.logs.get(user_id, {
            "username": username,
            "msg_id": None,
            "actions": []
        })
        
        # Update username if changed
        user_data["username"] = username
        
        # Append action
        user_data["actions"].append(new_entry)
        
        # Keep only last 15 actions to avoid hitting message length limits
        if len(user_data["actions"]) > 15:
            user_data["actions"] = user_data["actions"][-15:]
            
        self.logs[user_id] = user_data
        self._save_logs()

        # Build message text
        log_text = (
            f"👤 <b>User Tracking:</b> {username}\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            + "\n".join(user_data["actions"])
        )

        try:
            if user_data["msg_id"]:
                # Try to edit existing message
                try:
                    await bot.edit_message_text(
                        text=log_text,
                        chat_id=channel_id,
                        message_id=user_data["msg_id"],
                        parse_mode="HTML"
                    )
                except Exception as e:
                    # If edit fails (deleted, or too old, or content same), send new
                    if "message is not modified" in str(e).lower():
                        return # Nothing to do
                    
                    # Assume message lost/can't edit, send new
                    msg = await bot.send_message(
                        chat_id=channel_id,
                        text=log_text,
                        parse_mode="HTML"
                    )
                    user_data["msg_id"] = msg.message_id
            else:
                # Send new message
                msg = await bot.send_message(
                    chat_id=channel_id,
                    text=log_text,
                    parse_mode="HTML"
                )
                user_data["msg_id"] = msg.message_id
                
            self.logs[user_id] = user_data
            self._save_logs()
            
        except Exception as e:
            print(f"⚠️ Logger Error: {e}")

# Global instance
logger = ActivityLogger()
