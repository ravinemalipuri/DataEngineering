"""
Notification helpers (email today, can extend to Teams/Webhooks later).
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Dict


class EmailNotifier:
    """Sends success/failure notifications using SMTP settings from config."""

    def __init__(self, config: Dict):
        self.config = config

    def notify(self, success: bool, subject_suffix: str, body: str) -> None:
        if not self.config.get("enabled", False):
            return

        msg = EmailMessage()
        msg["Subject"] = f"[Metadata Ingestion] {'SUCCESS' if success else 'FAILURE'} - {subject_suffix}"
        msg["From"] = self.config["sender"]
        recipients = (
            self.config.get("success_recipients", []) if success else self.config.get("failure_recipients", [])
        )
        msg["To"] = ", ".join(recipients)
        msg.set_content(body)

        smtp = smtplib.SMTP(self.config["smtp_host"], self.config.get("smtp_port", 25))
        try:
            if self.config.get("use_tls", False):
                smtp.starttls()
            smtp.send_message(msg)
        finally:
            smtp.quit()








