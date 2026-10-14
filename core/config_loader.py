import os

def load_production_config():
    config = {
        "owner": "Abdallah Ben Belgacem",
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "sender_email": os.getenv("SENDER_EMAIL", "your_email@gmail.com"),
        "sender_password": os.getenv("SENDER_PASSWORD", "your_app_password"),
        "target_iban": "FR76 1659 8000 0140 0014 2630 322"
    }
    return config

if __name__ == "__main__":
    cfg = load_production_config()
    print(f"[*] Production configuration loaded for {cfg['owner']}.")
