from appman.models import Application
from django.forms import *

class ApplicationForm(ModelForm):
	class Meta:
		model = Application
		fields = ('name', 'zipfile','icon','category','description')
		
class ApplicationEditForm(ApplicationForm):
    zipfile = FileField(required=False)
    icon = FileField(required=False)

