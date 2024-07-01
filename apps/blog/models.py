from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from apps.services.utils import unique_slugify
from taggit.managers import TaggableManager

class PostManager(models.Manager):
    """
    Custom manager for post model
    """

    def get_queryset(self):
        """
        List of posts (SQL query filtered by published status)
        """
        return super().get_queryset().select_related('author', 'category').filter(status='published')

class Category(MPTTModel):
    """
    Nesting category model
    """
    title = models.CharField(max_length=255, verbose_name='Name of category')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Category description', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Parent category'
    )

    class MPTTMeta:
        """
        Sort by nesting
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Sorting, model name in the admin panel, table with data
        """
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'app_categories'

    def get_absolute_url(self):
        """
        We get a direct link to the category
        """
        return reverse('post_by_category', kwargs={'slug': self.slug})


    def __str__(self):
        """
        Returning the category title
        """
        return self.title


class Post(models.Model):
    """
    Post model for our blog
    """

    STATUS_OPTIONS = (
        ('published', 'Published'),
        ('draft', 'Draft')
    )

    title = models.CharField(verbose_name='Post title', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Short description', max_length=500)
    text = models.TextField(verbose_name='Full text of the entry')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Category')
    thumbnail = models.ImageField(default='default.jpg',
        verbose_name='Post image',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    tags = TaggableManager()
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Record status', max_length=10)
    create = models.DateTimeField(auto_now_add=True, verbose_name='Add time')
    update = models.DateTimeField(auto_now=True, verbose_name='Update time')
    author = models.ForeignKey(to=User, verbose_name='Author', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Updated', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Attached', default=False)

    objects = models.Manager()
    custom = PostManager()

    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Receive a direct link to the article
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        When saving, we generate a slug and check for uniqueness
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)

    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])

class Comment(MPTTModel):
    """
    Tree Comment Model
    """

    STATUS_OPTIONS = (
        ('published', 'Published'),
        ('draft', 'Draft')
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Note', related_name='comments')
    author = models.ForeignKey(User, verbose_name='Comment author', on_delete=models.CASCADE, related_name='comments_author')
    content = models.TextField(verbose_name='Comment body', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Add time', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Updated time', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Post status', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Parents comment', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
        Sort by nesting
        """
        order_insertion_by = ('-time_create',)

    class Meta:
        """
        Sorting, model name in the admin panel, table in the data
        """
        ordering = ['-time_create']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author}:{self.content}'

class Rating(models.Model):
    """
    Rating model: Like - Dislike
    """
    post = models.ForeignKey(to=Post, verbose_name='Note', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(to=User, verbose_name='User', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Meaning', choices=[(1, 'Like'), (-1, 'Dislike')])
    time_create = models.DateTimeField(verbose_name='Add time', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Address')

    class Meta:
        unique_together = ('post', 'ip_address')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create', 'value'])]
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return self.post.title