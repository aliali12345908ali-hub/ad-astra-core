import os
import requests

def send_telegram_alert(message, bot_token=None, chat_id=None):
    token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat:
        print(f"[*] [Simulated Notification]: {message}")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat, "text": message, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")
        return False

if __name__ == "__main__":
    send_telegram_alert("🚀 *Ad Astra System Alert*\nAll Autonomous Services are operating nominally for Abdallah Ben Belgacem.")
