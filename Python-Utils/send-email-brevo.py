import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

# Load environment variables from config.env file
load_dotenv('config.env')

def send_single_email(recipient_email=None, recipient_name=None, subject=None, html_content=None, sender_name=None, sender_email=None, api_key=None):
    """
    Send a single transactional email using SendinBlue/Brevo API
    
    Args:
        recipient_email (str): Recipient's email address (optional, uses env var if not provided)
        recipient_name (str): Recipient's name (optional, uses env var if not provided)
        subject (str): Email subject (optional, uses default if not provided)
        html_content (str): HTML content of the email (optional, uses default if not provided)
        sender_name (str): Sender's name (optional, uses env var if not provided)
        sender_email (str): Sender's email address (optional, uses env var if not provided)
        api_key (str): API key (optional, uses env var if not provided)
    
    Returns:
        dict: Response containing success status and message
    """
    
    # Get configuration from config.env file
    if not api_key:
        api_key = os.getenv('SENDINBLUE_API_KEY')
    
    if not recipient_email:
        recipient_email = os.getenv('DEFAULT_RECIPIENT_EMAIL')
    
    if not recipient_name:
        recipient_name = os.getenv('DEFAULT_RECIPIENT_NAME', '')
    
    if not sender_name:
        sender_name = os.getenv('DEFAULT_SENDER_NAME', 'Your Company')
    
    if not sender_email:
        sender_email = os.getenv('DEFAULT_SENDER_EMAIL', 'your.email@company.com')
    
    if not subject:
        subject = "Default Subject - Email from Config"
    
    if not html_content:
        html_content = "<h2>Hello!</h2><p>This is a test email sent using configuration from config.env file!</p><p>Thank you for your attention!</p>"
    
    # Validate required fields
    if not api_key:
        return {
            'success': False,
            'error': 'API key not found. Please check config.env file'
        }
    
    if not recipient_email:
        return {
            'success': False,
            'error': 'Recipient email not found. Please provide recipient_email or set DEFAULT_RECIPIENT_EMAIL in config.env'
        }
    
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        
        # Create transactional email
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": recipient_email, "name": recipient_name}],
            sender={"name": sender_name, "email": sender_email},
            subject=subject,
            html_content=html_content
        )
        
        # Use TransactionalEmailsApi for single emails
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        response = api_instance.send_transac_email(email)
        
        print(f"Email sent successfully to {recipient_email}")
        print(f"Message ID: {response.message_id}")
        
        return {
            'success': True,
            'response': response,
            'message_id': response.message_id,
            'recipient': recipient_email
        }
        
    except ApiException as e:
        error_msg = f"API Error: {e}"
        print(f"Error sending email: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Error sending email: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }

def load_email_config_info():
    """Display current email configuration loaded from config.env"""
    print("=== Email Configuration ===")
    print(f"API Key: {'*' * 8 + os.getenv('SENDINBLUE_API_KEY', 'Not set')[-4:] if os.getenv('SENDINBLUE_API_KEY') else 'Not set'}")
    print(f"Default Sender: {os.getenv('DEFAULT_SENDER_NAME', 'Not set')} <{os.getenv('DEFAULT_SENDER_EMAIL', 'Not set')}>")
    print(f"Default Recipient: {os.getenv('DEFAULT_RECIPIENT_NAME', 'Not set')} <{os.getenv('DEFAULT_RECIPIENT_EMAIL', 'Not set')}>")
    print("=" * 27)

# Example usage
if __name__ == "__main__":
    # Display current configuration
    load_email_config_info()
    
    # Send email using configuration from config.env
    result = send_single_email(
        subject="Special Announcement from Config!",
        html_content="<h2>Hello!</h2><p>This email was sent using configuration loaded from config.env file!</p><p>All settings are now centralized and secure!</p>"
    )
    
    if result['success']:
        print("Email delivery initiated successfully!")
        print(f"Sent to: {result['recipient']}")
    else:
        print(f"Failed to send email: {result['error']}")
