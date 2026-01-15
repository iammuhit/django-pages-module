from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import generic

from mayacms.contrib.pages.models import Page


class PageView(generic.DetailView):
    model = Page
    template_name = 'pages/view.html'
    context_object_name = 'page'
    
    def get_object(self):
        path = self.kwargs.get('path', '').strip('/')
        path = f'/{path}'

        if path == 'favicon.ico':
            raise Http404()

        try:
            if path == '/':
                page = Page.objects.get(Q(path=path) | Q(is_home=True))
            else:
                page = Page.objects.get(path=path, is_home=False)
        except Exception:
            raise Http404()

        return page
