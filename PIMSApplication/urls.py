
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from PIMSApplication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/ui/article/fetch/sorted', views.ui_article_fetch_sorted),
    url(r'^api/v1/admin/article/fetch', views.article_list_admin),
    url(r'^api/v1/admin/article/category/delete', views.article_delete_category_admin),
    url(r'^api/v1/ui/article/fetch', views.ui_article_fetch_all),

]