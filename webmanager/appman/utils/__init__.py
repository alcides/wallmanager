from django.contrib.auth.models import User
from django.conf import settings

def get_contact_admin_email():
    try:
        email_to = User.objects.filter(is_superuser=True)[0].email
    except IndexError:
        email_to = settingsDEFAULT_FROM_EMAIL
    return email_to
