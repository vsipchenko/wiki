from django.urls import path
from . import views

urlpatterns = [
    path('', views.PageListView.as_view()),
    path(r'<int:page_id>/versions/', views.PageVersionsListView.as_view()),
    path(r'<int:page_id>/versions/<int:version_id>/', views.PageVersionDetailView.as_view()),
    path(r'<int:page_id>/versions/activate/', views.PageVersionActivateView.as_view())
]
