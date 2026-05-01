from django.urls import path
from . import views

urlpatterns = [
    path('record/list/', views.InboundRecordListView.as_view()),
    path('record/add/', views.InboundRecordAddView.as_view()),
    path('record/<int:inbound_id>/', views.InboundRecordDeleteView.as_view()),
    path('record/update/', views.InboundRecordUpdateView.as_view()),
    path('record/confirm/', views.InboundConfirmView.as_view()),
    path('detail/list/', views.InboundDetailListView.as_view()),
    path('detail/add/', views.InboundDetailAddView.as_view()),
    path('detail/<int:detail_id>/', views.InboundDetailDeleteView.as_view()),
    path('detail/update/', views.InboundDetailUpdateView.as_view()),
]