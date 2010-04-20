from django.db.models import get_models, signals
from django.conf import settings

from appman import models as app_models


def create_default_category(app, created_models, verbosity, **kwargs):
    from appman.models import Category
    if Category in created_models:
        Category.objects.create(name=settings.DEFAULT_CATEGORY)

signals.post_syncdb.connect(create_default_category,
    sender=app_models, dispatch_uid = "appman.management.create_default_category")