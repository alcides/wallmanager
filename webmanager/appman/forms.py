from appman.models import *
from django.forms import *


class CategoryForm(ModelForm):
    class Meta:
        model = Category
    fields = ('name')
	
class ApplicationForm(ModelForm):
    class Meta:
        model = Application
    fields = ('name', 'zipfile','icon','category','description')
	
class ApplicationEditForm(ApplicationForm):
    zipfile = FileField(required=False)
    icon = FileField(required=False)

