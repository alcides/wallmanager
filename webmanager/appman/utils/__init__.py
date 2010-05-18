import os, platform
from django.conf import settings
from appman.models import WallManager

def get_contact_admin_email():
    try:
        email = WallManager.objects.all()[0].contact
    except IndexError:
        email = settings.DEFAULT_TO_EMAIL
    return email
    
def reboot_os():
    if platform.system()[:3].lower() == "win":
        os.system("shutdown -r -t 1")
    else:
        print "Reboot in Windows"