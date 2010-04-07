import string
import poplib
import socket
from django.forms.fields import email_re
from django.contrib.auth.models import User

AUTHORIZED_SERVERS = {'student.dei.uc.pt':'stu','eden.dei.uc.pt':'ede'}

class StudentPopBackend:
    def auth_pop3_server(self, email=None, password=None):
        domain = ''
        username = ''
        if email_re.search(email):
            username = email[:email.find('@')]
            domain = email[email.find('@')+1:]
            
        if username and domain in AUTHORIZED_SERVERS.keys():
            try:
                m = poplib.POP3_SSL(domain)
                m.user(username)
                m.pass_(password)
                return bool(m.stat())
            except:
                return False
    
    def authenticate(self, username=None, password=None):
        if not self.auth_pop3_server(username, password):
            return None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            from random import choice
            temp_pass = ""
            new_user = ''
            domain = ''
            if email_re.search(username):
                domain = username[username.find('@')+1:]
                new_user = username[:username.find('@')]
                new_user = new_user + '_' + AUTHORIZED_SERVERS[domain]
                new_user = string.lower(new_user)
            for i in range(8):
                temp_pass = temp_pass + choice(string.letters)
            user = User.objects.create_user(new_user,username,temp_pass)
            user.is_staff = False
            user.save()
        return user
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        