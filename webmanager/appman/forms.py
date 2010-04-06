from appman.models import Application
from django.forms import ModelForm

class ApplicationForm(ModelForm):
	class Meta:
		model = Application
		fields = ('name', 'zipfile','icon','category','description')