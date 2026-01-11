from django.urls import path, re_path
from django.views.generic import RedirectView

from mayacms.contrib.pages import views

app_name = 'mayacms.contrib.pages'

urlpatterns = [
    path('', views.PageView.as_view(), name='pages.home'),
    path('<path:path>/', views.PageView.as_view(), name='pages.view'),
]
