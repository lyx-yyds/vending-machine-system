from django.urls import path
from . import views

urlpatterns = [
    # 商品分类
    path('category/list/', views.CategoryListView.as_view()),
    path('category/add/', views.CategoryAddView.as_view()),
    path('category/<int:category_id>/', views.CategoryDeleteView.as_view()),
    path('category/update/', views.CategoryUpdateView.as_view()),
    path('category/simple/', views.CategorySimpleListView.as_view()),
    # 商品
    path('list/', views.ProductListView.as_view()),
    path('add/', views.ProductAddView.as_view()),
    path('<int:product_id>/', views.ProductDeleteView.as_view()),
    path('update/', views.ProductUpdateView.as_view()),
    # 供应商
    path('supplier/list/', views.SupplierListView.as_view()),
    path('supplier/add/', views.SupplierAddView.as_view()),
    path('supplier/<int:supplier_id>/', views.SupplierDeleteView.as_view()),
    path('supplier/update/', views.SupplierUpdateView.as_view()),
]