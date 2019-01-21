from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(r'pages/', include('page.urls')),
]
