from django.db.models import get_models, signals
from django.conf import settings
from django.contrib.sites.models import Site

from appman import models as app_models


def create_default_category(app, created_models, verbosity, **kwargs):
    from appman.models import Category
    if Category in created_models:
        Category.objects.create(name=settings.DEFAULT_CATEGORY)

def create_default_documentation(app, created_models, verbosity, **kwargs):
    from django.contrib.flatpages.models import FlatPage
    f = FlatPage.objects.create(title="Documentation", url="/documentation/", template_name="flatpages/docs.html", content="Please fill this.Please fill this.Please fill this.Please fill this.Please fill this.Please fill this.Please fill this.")
    f.sites.add(Site.objects.get(id=1))
    f.save()
    
signals.post_syncdb.connect(create_default_category,
    sender=app_models, dispatch_uid = "appman.management.create_default_category")
    

signals.post_syncdb.connect(create_default_documentation,
    sender=app_models, dispatch_uid = "appman.management.create_default_documentation")