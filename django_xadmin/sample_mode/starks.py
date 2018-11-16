from starks.services.starks import starkSite,StarkModelAdmin

from .models import *

class BookConfig(StarkModelAdmin):
    list_display = ['title','author']

starkSite.register(Book)
starkSite.register(Publish)
starkSite.register(Author)
starkSite.register(AuthorDetail)