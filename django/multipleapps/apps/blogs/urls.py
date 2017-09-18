from django.conf.urls import url
from . import views           

urlpatterns = [
    url(r'^$', views.index),     
    url(r'^new$', views.new),
    url(r'^create$', views.create),
    url(r'^(?P<blog_id>\d+)$', views.show),
    url(r'^edit/(?P<blog_id>\d+)$', views.edit),
    url(r'^delete/(?P<blog_id>\d+)$', views.destroy),
]