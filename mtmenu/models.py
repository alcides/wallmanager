import os, sys

# Go back one directory and adds it to sys.path
add_dir = lambda x: sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), *x))
add_dir(['..'])
add_dir(['..', 'webmanager'])

# Set needed environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'webmanager.settings'

# webmanager models can now be imported
from webmanager.appman import models

if __name__ == '__main__':
    # Debug print
    print models.Application.objects.all()


