import sys
import os

# Add parent folder (Python-Utils) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from send_email_brevo import send_single_email  # ✅ make sure the filename is correct
from celery_config import app

@app.task
def send_email_task(recipient_email, subject, html_content):
    result = send_single_email(
        recipient_email=recipient_email,
        subject=subject,
        html_content=html_content
    )

    # Ensure Celery returns only JSON-serializable data
    return {
        'success': result.get('success'),
        'message': 'Email sent successfully' if result.get('success') else 'Email failed',
        'recipient': result.get('recipient', None),
        'error': str(result.get('error', '')) if not result.get('success') else None
    }
