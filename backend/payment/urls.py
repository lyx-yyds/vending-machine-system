from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.PaymentListView.as_view()),
    path('refund/list/', views.RefundListView.as_view()),
    path('refund/process/', views.ProcessRefundView.as_view()),
]