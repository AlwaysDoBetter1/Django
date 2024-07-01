from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from apps.services.utils import unique_slugify
from django.utils import timezone
from django.core.cache import cache

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Personal information')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of Birth')

    class Meta:
        """
        Sorting, table name in the database
        """
        ordering = ('user',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        """
        Saving model fields when they are not filled in
        """

        if not self.slug:
            self.slug = unique_slugify(self, self.user.username, self.slug)
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Returning a string
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Link to profile
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})

    def is_online(self):
        """
        Last 5 minutes online status
        """
        last_seen = cache.get(f'last-seen-{self.user.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False