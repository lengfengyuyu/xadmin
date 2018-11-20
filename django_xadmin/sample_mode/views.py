from django.shortcuts import render

# Create your views here.
from .models import Book,Publish
def page_show(request):

    # for i in range(0,100):
    #     Publish.objects.create(name='分页'+str(i),city="bj",email="test@test.com")

    current_page = request.GET.get("page",1)
    all_count = Publish.objects.all().count()
    base_url = request.path
    from starks.utils.page import Pagination

    pagination = Pagination(all_count,current_page,base_url,max_show=11)
    print(pagination.start)
    print(pagination.end)

    publish_list = Publish.objects.all()[pagination.start:pagination.end]
    page_html = pagination.page_to_html()
    return render(request,'sample_mode/index.html',locals())