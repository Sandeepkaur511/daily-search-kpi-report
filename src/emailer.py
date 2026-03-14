import json
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from email_logger import log_email

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SUCCESS EMAIL (KPI REPORT)
# ==================================================
def send_report_email(html_body, report_date):

    creds_path = BASE_DIR / "config" / "email_config.json"

    with open(creds_path) as f:
        creds = json.load(f)

    subject = f"Search Analytics KPI Report | {report_date}"

    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = creds["sender_email"]
    msg["To"] = ", ".join(creds["recipient_emails"])

    server = smtplib.SMTP(creds["smtp_server"], creds["smtp_port"])
    server.starttls()

    server.login(
        creds["sender_email"],
        creds["app_password"]
    )

    server.sendmail(
        creds["sender_email"],
        creds["recipient_emails"],
        msg.as_string()
    )

    server.quit()

    # ------------------------
    # EMAIL AUDIT LOG
    # ------------------------
    sender_email = creds["sender_email"]
    sender_name = sender_email.split("@")[0]

    for receiver_email in creds["recipient_emails"]:
        receiver_name = receiver_email.split("@")[0]

        log_email(
            sender_email=sender_email,
            sender_name=sender_name,
            receiver_email=receiver_email,
            receiver_name=receiver_name,
            subject=subject
        )

    print("Report email sent successfully")


# ==================================================
# FAILURE EMAIL (PIPELINE ERROR)
# ==================================================
def send_failure_email(error_message):

    creds_path = BASE_DIR / "config" / "email_config.json"

    with open(creds_path) as f:
        creds = json.load(f)

    subject = "KPI Reporting Pipeline Failure"

    body = f"""
    <html>
    <body style="font-family:Arial, sans-serif;">
        <p><b>An error occurred while executing the reporting pipeline:</b></p>

        <pre style="background:#f8f8f8;border:1px solid #ccc;padding:10px;">
{error_message}
        </pre>

        <p>Please review the pipeline logs.</p>
    </body>
    </html>
    """

    msg = MIMEText(body, "html")

    msg["Subject"] = subject
    msg["From"] = creds["sender_email"]
    msg["To"] = ", ".join(creds["alert_emails"])

    server = smtplib.SMTP(
        creds["smtp_server"],
        creds["smtp_port"]
    )

    server.starttls()

    server.login(
        creds["sender_email"],
        creds["app_password"]
    )

    server.sendmail(
        creds["sender_email"],
        creds["alert_emails"],
        msg.as_string()
    )

    server.quit()

    print("Failure notification sent")
