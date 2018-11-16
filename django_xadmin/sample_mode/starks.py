from starks.services.starks import starkSite,StarkModelAdmin

from .models import *

class BookConfig(StarkModelAdmin):
    list_display = ['title','price','pdate']

starkSite.register(Book,BookConfig)
starkSite.register(Publish)
starkSite.register(Author)
starkSite.register(AuthorDetail)