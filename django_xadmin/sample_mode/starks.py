from starks.services.starks import starkSite,StarkModelAdmin

from .models import *

class BookConfig(StarkModelAdmin):

    #注意处理多对多
    list_display = ['title','price','pdate','publish','authors']
    search_fields = ['title','price']
    list_filter = [ 'authors','publish']

    def ppprint(self,request,queryset):
        print(queryset)

    ppprint.desc = "打印操作"
    actions = [ppprint]

class PublishConfig(StarkModelAdmin):
    list_display = ['name','city']


starkSite.register(Book,BookConfig)
starkSite.register(Publish,PublishConfig)
starkSite.register(Author)
starkSite.register(AuthorDetail)