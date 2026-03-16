import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.post("/api/contact")
    def contact():
        data = request.get_json(force=True, silent=True) or {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()

        if not name or not email or not message:
            return (
                jsonify({"ok": False, "error": "All fields are required."}),
                400,
            )

        try:
            _send_email_notification(name=name, email=email, message=message)
        except Exception as exc:  # noqa: BLE001
            # In a real app you would log this to a monitoring system
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": "We could not send your message right now. Please try again later.",
                        "detail": str(exc),
                    }
                ),
                500,
            )

        return jsonify({"ok": True})

    @app.post("/api/chat")
    def chat():
        data = request.get_json(force=True, silent=True) or {}
        name = (data.get("name") or "").strip()
        from_channel = (data.get("from") or "").strip()
        message = (data.get("message") or "").strip()

        if not message:
            return (
                jsonify({"ok": False, "error": "Message cannot be empty."}),
                400,
            )

        # This is where you would forward the chat message to your phone / WhatsApp
        # via a provider like Twilio. For now we send an email notification so you
        # still get real-time alerts.
        try:
            _send_chat_notification(
                name=name or "Website visitor",
                from_channel=from_channel or "chat-widget",
                message=message,
            )
        except Exception as exc:  # noqa: BLE001
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": "We could not send your message right now.",
                        "detail": str(exc),
                    }
                ),
                500,
            )

        # Basic bot-style auto reply for the UI while you respond manually from email/phone
        return jsonify(
            {
                "ok": True,
                "reply": "Thanks for reaching out! I’ve received your message and will reply personally as soon as I can.",
            }
        )

    return app


def _send_email_notification(*, name: str, email: str, message: str) -> None:
    # Default to your Gmail if OWNER_EMAIL is not set
    owner_email = os.getenv("OWNER_EMAIL") or "christianilungamulumba@gmail.com"
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not (owner_email and smtp_host and smtp_user and smtp_password):
        raise RuntimeError(
            "Email is not configured. Set OWNER_EMAIL, SMTP_HOST, SMTP_PORT, "
            "SMTP_USER and SMTP_PASSWORD in the .env file."
        )

    subject = f"New enquiry from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = owner_email
    msg["To"] = owner_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)


def _send_chat_notification(*, name: str, from_channel: str, message: str) -> None:
    # Notify you via email (same as contact form)
    owner_email = os.getenv("OWNER_EMAIL") or "christianilungamulumba@gmail.com"
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not (owner_email and smtp_host and smtp_user and smtp_password):
        raise RuntimeError(
            "Chat notifications are not configured. Set OWNER_EMAIL, SMTP_HOST, "
            "SMTP_PORT, SMTP_USER and SMTP_PASSWORD in the .env file."
        )

    subject = f"New chat message from {name}"
    body = f"Channel: {from_channel}\nName: {name}\n\nMessage:\n{message}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = owner_email
    msg["To"] = owner_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)

