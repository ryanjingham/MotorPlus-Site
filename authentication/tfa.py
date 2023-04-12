import random
import string
from django.conf import settings 
from django.core.mail import send_mail


def generate_verification_code(length=6):
    """Generate a secret key of specified length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_tfa_email(email, secret_key):
    """Send an email with the secret key to the user."""
    subject = 'Your secret key for 2FA registration'
    message = f'Your secret key is: {secret_key}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)