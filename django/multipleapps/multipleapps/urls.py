from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.blogs.urls')),
    url(r'^blogs/', include('apps.blogs.urls')),
    url(r'^surveys/', include('apps.surveys.urls')),
    url(r'^users/', include('apps.users.urls'))
]
