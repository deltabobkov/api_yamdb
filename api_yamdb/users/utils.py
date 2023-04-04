import secrets
import string

from django.core.mail import send_mail


def generate_confirm_code():
    alphabet = string.ascii_letters + string.digits
    confirm_code = ''.join(secrets.choice(alphabet) for i in range(10))
    return confirm_code


def mail_send(subject: str, message: str, sender: str, recipients: list[str]):
    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=recipients,
        fail_silently=False,
    )
