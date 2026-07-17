"""Email utility functions."""
from emails import Message
from app.core.config import settings


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send an email.
    
    Args:
        to_email: Recipient email
        subject: Email subject
        html_content: HTML content
        
    Returns:
        True if sent successfully
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"Email disabled - would send to {to_email}: {subject}")
        return False
    
    try:
        message = Message(
            subject=subject,
            html=html_content,
            mail_from=(settings.SMTP_FROM_NAME, settings.SMTP_FROM_EMAIL),
        )
        
        response = message.send(
            to=to_email,
            smtp={
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT,
                "user": settings.SMTP_USER,
                "password": settings.SMTP_PASSWORD,
                "tls": True,
            }
        )
        
        return response.status_code == 250
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_verification_email(to_email: str, token: str) -> bool:
    """Send email verification email."""
    verification_url = f"{settings.FRONTEND_URL}/verify/{token}"
    
    html = f"""
    <html>
        <body>
            <h2>Welcome to AlumniConnect!</h2>
            <p>Please click the link below to verify your email:</p>
            <a href="{verification_url}">Verify Email</a>
            <p>Or copy this link: {verification_url}</p>
        </body>
    </html>
    """
    
    return send_email(to_email, "Verify your AlumniConnect account", html)


def send_approval_email(to_email: str, request_title: str) -> bool:
    """Send request approval notification."""
    html = f"""
    <html>
        <body>
            <h2>Request Approved!</h2>
            <p>Your referral request for <strong>{request_title}</strong> has been approved.</p>
            <p>Alumni can now view and submit referrals for your request.</p>
        </body>
    </html>
    """
    
    return send_email(to_email, "Your request has been approved", html)
