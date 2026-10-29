from __future__ import annotations


def send_daily_email(subject: str, body: str, to_email: str) -> dict[str, str]:
    """Placeholder email sender for a future delivery step."""
    return {
        "to": to_email,
        "subject": subject,
        "body": body,
        "status": "not_implemented",
    }
