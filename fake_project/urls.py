from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from django.urls import path,include

urlpatterns = [
    path('',include('fake_app.urls')),
    # url(r'^$',views.index,name='index'),
    # url(r'^$',views.signup,name='signup'),
    # url(r'^hello/',include('fake_app.urls')),
    path('admin/', admin.site.urls),
]
