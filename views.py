from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from app.modules.pages.models import Page


class PageView(generic.DetailView):
    model = Page
    template_name = 'pages/view.html'
    context_object_name = 'page'
    
    def get_object(self):
        path = self.kwargs.get('path', '').strip('/')

        if not path:
            page = Page.objects.get(Q(path='/') | Q(is_home=True))
        else:
            page = Page.objects.get(path='/' + path)

        return page
