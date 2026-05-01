from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.SpecificationListView.as_view()),
    path('add/', views.SpecificationAddView.as_view()),
    path('<int:spec_id>/', views.SpecificationDeleteView.as_view()),
    path('update/', views.SpecificationUpdateView.as_view()),
    path('simple/', views.SpecificationSimpleListView.as_view()),
]