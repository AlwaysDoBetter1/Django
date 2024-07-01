from django.conf import settings
from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug, slug_field):
    """
    Generator of unique SLUGs for models, if such an SLUG exists.
    """
    model = instance.__class__
    unique_slug = slug_field
    if not slug_field:
        unique_slug = slugify(slug)
    elif model.objects.filter(slug=slug_field) and model.objects.filter(slug=slug_field).last().id != instance.id:
        unique_slug = f'{slugify(slug)}-{uuid4().hex[:8]}'
    return unique_slug

def file_directory_path(instance, filename):
    """Creating a directory for saving photos."""
    filename = f'{uuid4().hex[:8]}.{filename.split(".")[-1]}'
    path = (f'{settings.MEDIA_ROOT}/images/'
            f'{instance.__class__.__name__}/{instance.slug}/{filename}')
    return path