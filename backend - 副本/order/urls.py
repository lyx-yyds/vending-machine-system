from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.OrderListView.as_view()),
    path('my-list/', views.MyOrderListView.as_view()),
    path('detail/list/', views.OrderDetailListView.as_view()),
    path('create/', views.CreateOrderView.as_view()),
    path('pay/', views.PayOrderView.as_view()),
    path('refund/', views.RefundOrderView.as_view()),
]
