from django.core.mail import send_mail
from asgiref.sync import sync_to_async


def normalize_kenyan_phone(phone):
    phone = phone.strip().replace(" ", "")
    
    if phone.startswith("07") and len(phone) == 10:
        return f"254{phone[1:]}"  # replace 0 with 254
    elif phone.startswith("+254"):
        return phone[1:]  # remove +
    elif phone.startswith("254") and len(phone) == 12:
        return phone
    else:
        raise ValueError("Invalid Kenyan phone number format.")

async def async_send_mail(subject, message, sender, recipients):
    await sync_to_async(send_mail)(
        subject, message, sender, recipients, fail_silently=False
    )