from django.contrib.auth.models import User

def get_contact_admin_email():
    try:
        email_to = User.objects.filter(is_superuser=True)[0].email
    except IndexError:
        email_to = DEFAULT_EMAIL_FROM
    return email_to
