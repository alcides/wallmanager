from appman.models import *
from django.forms import *
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
	
class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('name', 'zipfile','icon','category','description')
	
class ApplicationEditForm(ApplicationForm):
    zipfile = FileField(required=False)
    icon = FileField(required=False)

class UserCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = RegexField(label=("Username"), max_length=30, regex=r'^\w+$')
    email = EmailField(label=("Email"))
    password1 = CharField(label=("Password"), widget=PasswordInput)
    password2 = CharField(label=("Password confirmation"), widget=PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        self.error_dict['username']= settings.DEFAULT_USERNAME_ERROR
        self.error_username_html= settings.DEFAULT_USERNAME_ERROR
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        
        if not password1 or not password2:
            self.error_dict['password1']= settings.DEFAULT_INEXISTENT_PASSWD_ERROR
            self.error_password1_html= settings.DEFAULT_INEXISTENT_PASSWD_ERROR

	elif password1 != password2:
            self.error_dict['password2']= settings.DEFAULT_PASSWD_ERROR
            self.error_password2_html= settings.DEFAULT_PASSWD_ERROR
        return password2

    def clean_email(self):
	email = self.cleaned_data["email"].strip()
        if '@student.dei.uc.pt' in email or '@dei.uc.pt' in email:
            return email
        else:
            self.error_dict['email'] = settings.DEFAULT_EMAIL_ERROR
            self.error_email_html = settings.DEFAULT_EMAIL_ERROR
    
    def get_validation_errors(self,info):
        self.error_dict = {}
	self.info = {}
        self.cleaned_data = info
        self.info["email"] = self.clean_email()
        self.info["username"] =self.clean_username()
        self.info["password"] = self.clean_password2()
        return self.error_dict
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.info["username"]
	user.set_password(self.info["password"])
        user.email = self.info['email']

	##send confirmation email
	email_from = 'wallmanager@dei.uc.pt'
	email_to = self.cleaned_data['email']
	message = 'Dear ' + user.username + ', \nYour registration has been sucessfully complete.\n Best regards'
	send_mail('[WallManager] Registration Complete', message, email_from, [email_to])

	if commit:
            user.save()
        return user
