from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm, widgets as wid
from starks.utils.page import Pagination
from django.db.models import Q

class ViewShowLit(object):

    def __init__(self,stark_model_admin,dataList,request):
        self.stark_model_admin = stark_model_admin
        self.dataList = dataList
        self.request = request
        self.actions = stark_model_admin.actions
        if self.dataList:
            current_page = request.GET.get("page",1)
            self.page = Pagination(dataList.count(),current_page,request.path,request.GET,max_show=9)

            self.page_data = self.dataList[self.page.start:self.page.end]

    def get_actions(self):
        temp =[]
        temp.append({"name":"--------","desc":"--------"})
        for a in self.actions:
            temp.append({"name":a.__name__,"desc":a.desc})
        return temp
    def get_page(self):
        if self.dataList:
            return self.page.page_to_html()
        return None

    def get_table_body(self):
        newDataList = []
        if self.dataList:

            # 用于分页的数据，不是之前的所有数据了
            for item in self.page_data:
                temp = []
                for x in self.stark_model_admin.inner_display_list():
                    if isinstance(x, str):
                        if x in self.stark_model_admin.list_display_links:
                            temp.append(self.stark_model_admin.item_to_link(item, getattr(item, x)))
                            continue
                        temp.append(getattr(item, x))
                    elif callable(x):
                        temp.append(x(self.stark_model_admin, obj=item))

                newDataList.append(temp)
        return newDataList

    def get_table_header(self):
        headerList = []
        for x in self.stark_model_admin.inner_display_list():
            if isinstance(x, str):
                if x == "__str__":
                    headerList.append(self.stark_model_admin.model._meta.model_name.upper())
                else:
                    headerList.append(x)
                    # 中文列名这么做
                    # headerList.append(self.model._meta.getfield(x).verbose_name)
            elif callable(x):
                if self.stark_model_admin.list_display_links and x.__name__ == "edit":
                    continue
                headerList.append(x(self.stark_model_admin, header=True))
        return headerList


class StarkModelAdmin(object):
    list_display = ['__str__']
    list_display_links = []
    search_fields =[]
    actions = []

    def __init__(self, model, admin_site):
        self.model = model
        self.admin_site = admin_site

    def get_urls2(self):
        model_name = self.model._meta.model_name
        label_name = self.model._meta.app_label
        urlpatterns = []
        urlpatterns.append(path('', self.list_view, name="{}_{}_list".format(label_name, model_name)))
        urlpatterns.append(path('add/', self.add_view, name="{}_{}_add".format(label_name, model_name)))
        urlpatterns.append(
            path('<int:id>/change/', self.change_view, name="{}_{}_change".format(label_name, model_name)))
        urlpatterns.append(
            path('<int:id>/delete/', self.deltee_view, name="{}_{}_delete".format(label_name, model_name)))

        return urlpatterns

    @property
    def urls2(self):
        return self.get_urls2(), None, None

    # ----------操作部分---------------
    def item_to_link(self, obj, val):
        model_name = self.model._meta.model_name
        label_name = self.model._meta.app_label
        # 反向解析注意url是否含有参数
        # _url = reverse("{}_{}_add".format(label_name,model_name))
        _url = reverse("{}_{}_change".format(label_name, model_name), args=(obj.id,))

        return mark_safe('<a href="{}">{}</a>'.format(_url, val))

    def edit(self, obj=None, header=False):
        if header:
            return '编辑'
        else:
            model_name = self.model._meta.model_name
            label_name = self.model._meta.app_label
            # 反向解析注意url是否含有参数
            # _url = reverse("{}_{}_add".format(label_name,model_name))
            _url = reverse("{}_{}_change".format(label_name, model_name), args=(obj.nid,))

            return mark_safe('<a href="{}">编辑</a>'.format(_url))

    def remove(self, obj=None, header=False):
        if header:
            return '移除'
        else:
            model_name = self.model._meta.model_name
            label_name = self.model._meta.app_label

            _url = reverse("{}_{}_delete".format(label_name, model_name), args=(obj.nid,))

            return mark_safe('<a href="{}">移除</a>'.format(_url))

    def choice(self, obj=None, header=False):
        if header:
            return mark_safe('<input type="checkbox" class="cb-all" />')
        return mark_safe('<input type="checkbox" class="cb-item" name="cb-cho" value={}>'.format(obj.pk))

    def inner_display_list(self):
        tl = []
        tl.append(StarkModelAdmin.choice)
        tl.extend(self.list_display)
        if not self.list_display_links:
            tl.append(StarkModelAdmin.edit)
        tl.append(StarkModelAdmin.remove)
        return tl

    def get_which_url(self, which):
        model_name = self.model._meta.model_name
        label_name = self.model._meta.app_label

        _url = reverse("{}_{}_{}".format(label_name, model_name, which))
        print(_url)
        return _url

    def get_default_model_from(self):
        class StarkModelForm(ModelForm):
            class Meta:
                model = self.model
                print(model)
                fields = "__all__"

        return StarkModelForm

    def get_sql_filter(self,request):
        user_sf = request.POST.get("search_field")
        sql_q = Q()
        sql_q.connector = "or"
        if user_sf:
            for sf in self.search_fields:
                sql_q.children.append((sf + "__contains", user_sf))

        return sql_q
    # ----------视图部分----------
    def list_view(self, request):
        #过滤
        if request.method == "POST":
            # 区分POST进行什么操作
            if request.POST.get("search_field"):
                dataList = self.model.objects.all().filter(self.get_sql_filter(request))
            elif request.POST.get("action"):
                act_func = getattr(self,request.POST.get("action"))
                qs = self.model.objects.filter(pk__in=request.POST.getlist("cb-cho"))
                act_func(request,qs)
                dataList = self.model.objects.all()
        else:
            dataList = self.model.objects.all()

        vsl = ViewShowLit(self,dataList,request)
        add_url = self.get_which_url('add')
        return render(request, "starks/list.html", locals())

    def deltee_view(self, request, id):
        back_url = self.get_which_url('list')
        if request.method == "POST":
            self.model.objects.filter(nid=id).delete()
            return redirect(back_url)
        return render(request,"starks/del.html",locals())

    def add_view(self, request):
        InnerModelFrom = self.get_default_model_from()
        if request.method == "POST":
            form = InnerModelFrom(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_which_url('list'))
            return render(request, "starks/add.html", locals())

        form = InnerModelFrom()
        return render(request, "starks/add.html", locals())

    def change_view(self, request, id):
        InnerModelFrom = self.get_default_model_from()
        obj = self.model.objects.filter(nid=id).first()
        if request.method == "POST":
            form = InnerModelFrom(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_which_url('list'))
            return render(request, "starks/list.html", locals())

        form = InnerModelFrom(instance=obj)
        return render(request, "starks/change.html", locals())


class StarkSite(object):

    def __init__(self, name='admin'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name

    def register(self, model, admin_class=None):
        if not admin_class:
            admin_class = StarkModelAdmin
        self._registry[model] = admin_class(model, self)

    def get_urls(self):
        urlpatterns = []

        for model, admin_class in self._registry.items():
            model_name = model._meta.model_name
            label_name = model._meta.app_label
            urlpatterns.append(path('{}/{}/'.format(label_name, model_name), admin_class.urls2))

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), None, None


starkSite = StarkSite()
