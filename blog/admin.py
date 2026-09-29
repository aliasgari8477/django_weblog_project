from django.contrib import admin
from .models import Blog
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ['status', 'datetime_modified', 'datetime_created', 'author', 'title']
    ordering = ['datetime_created', '-status']


admin.site.register(Blog, BlogAdmin)
