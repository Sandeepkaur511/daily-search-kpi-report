import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "email_log.csv"


def log_email(
    sender_email,
    sender_name,
    recipient_email,
    recipient_name,
    subject
):
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header once
        if not file_exists:
            writer.writerow([
                "sender_email",
                "sender_name",
                "recipient_email",
                "recipient_name",
                "email_subject",
                "sent_timestamp"
            ])

        writer.writerow([
            sender_email,
            sender_name,
            recipient_email,
            recipient_name,
            subject,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
