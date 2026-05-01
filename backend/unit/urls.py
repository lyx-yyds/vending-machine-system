from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.UnitListView.as_view()),
    path('add/', views.UnitAddView.as_view()),
    path('<int:unit_id>/', views.UnitDeleteView.as_view()),
    path('update/', views.UnitUpdateView.as_view()),
    path('simple/', views.UnitSimpleListView.as_view()),
]