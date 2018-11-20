import copy
class Pagination(object):
    def __init__(self,data_num,current_page,url_prefix,params,per_page=10,max_show=3):
        self.data_num = data_num
        self.url_prefix = url_prefix
        self.per_page = per_page
        self.max_show = max_show

        # 算一共有多少页
        self.page_num,more = divmod(data_num,per_page)
        if more:
            self.page_num += 1
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1

        # 确定当前请求页不越界
        if self.current_page < 1:
            self.current_page = 1
        elif self.current_page > self.page_num:
            self.current_page = self.page_num

        # 算出一半
        self.half_show = max_show // 2

        # 最左边显示的页码
        if self.current_page - self.half_show < 2:
            self.page_start = 1
            self.page_end = self.max_show
        #如果右边越界
        elif self.current_page + self.half_show >= self.page_num:
            self.page_end = self.page_num
            self.page_start = self.current_page - self.half_show
        else:
            self.page_start = self.current_page - self.half_show
            self.page_end = self.current_page + self.half_show

        self.params = copy.deepcopy(params)
    @property
    def start(self):
        return (self.current_page-1)*self.per_page

    @property
    def end(self):
        return self.current_page* self.per_page

    def page_to_html(self):
        h =[]
        h.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))
        if self.current_page == 1:
            h.append('<li class="disabled"><a href="#">&laquo;</a></li>'.format(self.current_page))
        else:
            h.append('<li><a href="{}?page={}">&laquo;</a></li>'.format(self.url_prefix,self.current_page-1))

        for i in range(self.page_start,self.page_end+1):
            self.params['page']=i
            if i == self.current_page:
                tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix,self.current_page)

            else:
                tmp = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix,self.params.urlencode(),i)

            h.append(tmp)

        if self.current_page == self.page_num:
            h.append('<li class="disabled"><a href="#">&raquo;</a></li>'.format(self.current_page))
        else:
            h.append('<li><a href="{}?page={}">&raquo;</a></li>'.format(self.url_prefix,self.current_page+1))

        h.append('<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix,self.page_num))

        return "".join(h)
