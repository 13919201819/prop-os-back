import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("propos.email")

# Storage for active OTP codes in-memory (email -> { code, expires_at })
OTP_STORE: Dict[str, Dict[str, Any]] = {}

async def send_brevo_otp_email(to_email: str, otp_code: str, user_name: str = "", is_password_reset: bool = False) -> bool:
    """
    Dispatches a real-time transactional email containing the 6-digit OTP code
    via the Brevo (Sendinblue) API from noreply@themistrai.com.
    """
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    recipient_name = user_name or to_email.split("@")[0]
    
    if is_password_reset:
        subject_title = f"[{otp_code}] Your PropOS Password Reset Code"
        email_header_title = "PropOS Password Reset"
        message_body = "We received a request to reset your password for your <strong>PropOS</strong> account. Please use the 6-digit verification code below to reset your password:"
    else:
        subject_title = f"[{otp_code}] Your PropOS Account Verification Code"
        email_header_title = "PropOS Account Verification"
        message_body = "Thank you for registering with <strong>PropOS</strong>. To complete your account signup and access your workspace dashboard, please use the 6-digit verification code below:"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>{email_header_title}</title>
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }}
        .container {{ max-width: 580px; margin: 40px auto; background: #1e293b; border-radius: 16px; padding: 36px; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); }}
        .header {{ text-align: center; padding-bottom: 24px; border-bottom: 1px solid #334155; }}
        .logo {{ font-size: 28px; font-weight: 800; color: #38bdf8; letter-spacing: -0.5px; }}
        .subtitle {{ font-size: 14px; color: #94a3b8; margin-top: 4px; }}
        .content {{ padding: 32px 0; text-align: center; }}
        .greeting {{ font-size: 18px; color: #cbd5e1; margin-bottom: 16px; text-align: left; }}
        .message {{ font-size: 15px; color: #94a3b8; line-height: 1.6; text-align: left; margin-bottom: 28px; }}
        .otp-box {{ background: #0f172a; border: 2px dashed #0284c7; border-radius: 12px; padding: 20px; display: inline-block; margin: 10px 0 24px; width: 80%; }}
        .otp-code {{ font-size: 38px; font-weight: 800; letter-spacing: 10px; color: #38bdf8; font-family: monospace; }}
        .warning {{ font-size: 13px; color: #f59e0b; margin-top: 16px; background: rgba(245, 158, 11, 0.1); padding: 10px 14px; border-radius: 8px; text-align: left; }}
        .footer {{ border-top: 1px solid #334155; padding-top: 20px; text-align: center; font-size: 12px; color: #64748b; margin-top: 28px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="logo">🏙️ PropOS</div>
          <div class="subtitle">Real Estate AI Sales & SaaS Automation Platform</div>
        </div>
        <div class="content">
          <div class="greeting">Hello {recipient_name},</div>
          <div class="message">
            {message_body}
          </div>
          <div class="otp-box">
            <div class="otp-code">{otp_code}</div>
          </div>
          <div class="warning">
            ⚠️ This code is valid for <strong>5 minutes</strong>. For security reasons, please do not share this code with anyone.
          </div>
        </div>
        <div class="footer">
          Sent automatically by <strong>PropOS Platform</strong> &bull; <a href="https://themistrai.com" style="color: #38bdf8; text-decoration: none;">themistrai.com</a><br>
          If you did not request this verification code, please ignore this email.
        </div>
      </div>
    </body>
    </html>
    """

    payload = {
        "sender": {
            "name": settings.BREVO_FROM_NAME,
            "email": settings.BREVO_FROM_EMAIL
        },
        "to": [
            {
                "email": to_email,
                "name": recipient_name
            }
        ],
        "subject": subject_title,
        "htmlContent": html_content
    }

    try:
        logger.info(f"Dispatching Brevo OTP email to: {to_email} (From: {settings.BREVO_FROM_EMAIL})")
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Brevo OTP email successfully delivered to {to_email}. MessageID: {response.json().get('messageId', 'OK')}")
                return True
            else:
                logger.error(f"Brevo API error ({response.status_code}): {response.text}")
                return False
    except Exception as e:
        logger.error(f"Failed to dispatch Brevo OTP email to {to_email}: {str(e)}", exc_info=True)
        return False
