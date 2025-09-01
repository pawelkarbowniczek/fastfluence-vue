# app/services/email_service.py

import secrets
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

from .config import settings
from .models import User


# --- helpers -----------------------------------------------------------------

def _sender_email() -> str:
    """Preferuj SENDGRID_FROM_EMAIL; wstecznie zgodne z SMTP_FROM_EMAIL."""
    return getattr(settings, "SENDGRID_FROM_EMAIL", None) or settings.SMTP_FROM_EMAIL

def _sender_name() -> Optional[str]:
    """Opcjonalna nazwa nadawcy."""
    return getattr(settings, "SENDGRID_FROM_NAME", None) or getattr(settings, "SMTP_FROM_NAME", None)


# --- public API ---------------------------------------------------------------

def generate_activation_token() -> str:
    """Generate a secure random token for account activation"""
    return secrets.token_urlsafe(32)


def send_activation_email(user: User, activation_token: str) -> bool:
    """Send activation email using SendGrid (library)."""
    html = get_activation_email_html(user, activation_token)
    subject = "Aktywuj swoje konto FastFluence"
    return send_email_via_sendgrid(
        to_email=user.email,
        subject=subject,
        html_content=html,
        from_email=_sender_email(),
        from_name=_sender_name(),
    )


def send_welcome_email(user: User) -> bool:
    """Send welcome email after successful account activation."""
    html = get_welcome_email_html(user)
    subject = "Witamy w FastFluence! 🎉"
    return send_email_via_sendgrid(
        to_email=user.email,
        subject=subject,
        html_content=html,
        from_email=_sender_email(),
        from_name=_sender_name(),
    )


def send_email_via_sendgrid(
    to_email: str,
    subject: str,
    html_content: str,
    *,
    from_email: str,
    from_name: Optional[str] = None,
) -> bool:
    """
    Send email using SendGrid Python SDK.
    Zwraca True tylko gdy API odpowie 202.
    """
    try:
        if not getattr(settings, "SENDGRID_API_KEY", None):
            raise RuntimeError("Missing SENDGRID_API_KEY in settings")

        sender = Email(from_email, from_name) if from_name else Email(from_email)
        message = Mail(
            from_email=sender,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )

        # (opcjonalnie) przykładowa kategoria:
        # message.category = "transactional"

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code == 202:
            print(f"[SendGrid] Email sent to {to_email}")
            return True

        print(f"[SendGrid] Error {response.status_code}: {response.body}")
        return False

    except Exception as e:
        print(f"[SendGrid] Exception: {e}")
        return False


# --- templates ----------------------------------------------------------------

def get_activation_email_html(user: User, activation_token: str) -> str:
    activation_url = f"{settings.FRONTEND_URL}/activate/{activation_token}"
    return f"""
    <html>
        <body style="font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #111111;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="font-size: 2.5em; font-weight: bold; margin: 0;">
                        <span style="color: #7D3CFF;">Fast</span><span style="color: #D4FF32;">Fluence</span>
                    </h1>
                </div>
                <h2 style="color: #111111;">Witaj {user.display_name}!</h2>
                <p>Dziękujemy za rejestrację w FastFluence - platformie łączącej marki z influencerami.</p>
                <p>Aby aktywować swoje konto i rozpocząć korzystanie z platformy, kliknij w poniższy przycisk:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{activation_url}"
                       style="background: #7D3CFF; color: white; padding: 15px 30px;
                              text-decoration: none; border-radius: 8px; font-weight: bold;
                              display: inline-block; font-size: 16px;">
                        Aktywuj konto
                    </a>
                </div>
                <p>Jeśli przycisk nie działa, skopiuj i wklej poniższy link do przeglądarki:</p>
                <p style="word-break: break-all; color: #7D3CFF;">{activation_url}</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="font-size: 14px; color: #666;">
                    Link aktywacyjny wygaśnie po 24 godzinach.<br>
                    Jeśli nie rejestrowałeś się na FastFluence, zignoruj tę wiadomość.
                </p>
                <div style="text-align: center; margin-top: 30px; font-size: 14px; color: #666;">
                    <p>Zespół FastFluence</p>
                    <p>Platforma dla influencerów i reklamodawców</p>
                </div>
            </div>
        </body>
    </html>
    """


def get_welcome_email_html(user: User) -> str:
    role_text = "reklamodawcy" if user.role == "advertiser" else "twórcy"
    dashboard_text = "Panel reklamodawcy" if user.role == "advertiser" else "Znajdź zlecenia"
    return f"""
    <html>
        <body style="font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #111111;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="font-size: 2.5em; font-weight: bold; margin: 0;">
                        <span style="color: #7D3CFF;">Fast</span><span style="color: #D4FF32;">Fluence</span>
                    </h1>
                    <p style="font-size: 18px; margin: 10px 0; color: #666;">
                        Witamy w społeczności! 🎉
                    </p>
                </div>
                <h2 style="color: #111111;">Cześć {user.display_name}!</h2>
                <p>Twoje konto zostało pomyślnie aktywowane! Jesteś teraz częścią społeczności FastFluence jako <strong>{role_text}</strong>.</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #7D3CFF; margin-top: 0;">Co możesz teraz zrobić:</h3>
                    <ul style="padding-left: 20px;">
                        {"<li>Przeglądać dostępne kampanie marketingowe</li><li>Aplikować do projektów które Cię interesują</li><li>Uzupełnić swoje portfolio w profilu</li>" if user.role == "creator" else "<li>Tworzyć kampanie marketingowe</li><li>Przeglądać profile twórców treści</li><li>Zarządzać swoimi projektami</li>"}
                        <li>Edytować swój profil i dane kontaktowe</li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{settings.FRONTEND_URL}/dashboard"
                       style="background: #7D3CFF; color: white; padding: 15px 30px;
                              text-decoration: none; border-radius: 8px; font-weight: bold;
                              display: inline-block; font-size: 16px;">
                        Przejdź do {dashboard_text}
                    </a>
                </div>
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <div style="text-align: center; margin-top: 30px; font-size: 14px; color: #666;">
                    <p><strong>Potrzebujesz pomocy?</strong></p>
                    <p>Skontaktuj się z nami: <a href="mailto:support@fastfluence.pl" style="color: #7D3CFF;">support@fastfluence.pl</a></p>
                </div>
                <div style="text-align: center; margin-top: 30px; font-size: 14px; color: #666;">
                    <p>Zespół FastFluence</p>
                    <p>Platforma dla influencerów i reklamodawców</p>
                </div>
            </div>
        </body>
    </html>
    """
