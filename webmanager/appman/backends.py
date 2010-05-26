import string
import ldap
from django.conf import settings
from django.forms.fields import email_re
from django.contrib.auth.models import User

class StudentPopBackend:
    def auth_ldap_server(self, email=None, password=None):
        domain = ''
        username = ''
        if email_re.search(email):
            dn = settings.AUTH_LDAP_USER_BASE(email)

            try:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,settings.AUTH_LDAP_CERT)

                l = ldap.initialize(settings.AUTH_LDAP_SERVER)
                l.start_tls_s()
                l.simple_bind_s(dn, password)

                # Builds real name to fill in register, and force auth check.
                me = l.search_s(l.whoami_s()[3:],ldap.SCOPE_SUBTREE)
                ln = me[0][1]['sn'][0]
                fn = me[0][1]['givenName'][0].split()[0]
                return "%s %s" % (fn, ln)

            except ldap.INVALID_CREDENTIALS:
                # Name or password were bad. Fail.
                return False
            except ldap.LDAPError, e:
                return False
        else:
            return False
    
    def authenticate(self, username=None, password=None):
        ldap_res = self.auth_ldap_server(username, password)
        if not ldap_res:
            return None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            temp_pass = User.objects.make_random_password()
            user = User.objects.create_user(ldap_res,username,temp_pass)
            user.is_staff = False
            user.save()
        return user
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
