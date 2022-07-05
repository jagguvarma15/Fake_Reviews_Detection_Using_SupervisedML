from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^register/',views.register,name='register'),
    url(r'^register/login', views.login, name='login'),
    url(r'^login',views.login,name='login'),
    url(r'^loghome',views.loghome,name='loghome'),
    url(r'^upload',views.upload,name='upload'),
    url(r'^viewdata',views.viewdata,name='viewdata'),
    url(r'^model',views.models,name='models'),
    url(r'^prediction',views.prediction,name='prediction'),
    url(r'^about',views.about,name='about')
]