from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Post, Comment, Rating


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Admin panel of the category model
    """
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post model admin panel
    """
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    """
    Comment model admin panel
    """
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin panel of the rating model
    """
    pass