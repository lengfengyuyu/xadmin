from django.contrib import admin

# Register your models here.

from .models import *

class BookConfig(admin.ModelAdmin):
    list_filter = ['title','authors','publish']

admin.site.register(Book,BookConfig)
admin.site.register(Author)
admin.site.register(AuthorDetail)
admin.site.register(Publish)