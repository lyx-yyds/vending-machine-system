from .serializers import ProductSerializer, ProductCategorySerializer, SupplierSerializer
from .models import Product, ProductCategory, Supplier
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from uuid import uuid4
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


# ===============商品分类====================================
class CategoryListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        category_name = request.GET.get('category_name', '')

        query = ProductCategory.objects.filter(is_delete=0)
        if category_name:
            query = query.filter(category_name__icontains=category_name)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        serializer_data = ProductCategorySerializer(page_data, many=True)
        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': serializer_data.data
        }
        return Response(ResultVo.success("查询成功", response_data))


class CategoryAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        category_code = 'CATE_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + uuid_random
        request_data['category_code'] = category_code

        serializer = ProductCategorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class CategoryUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        category_id = request_data.get('id')
        if not category_id:
            return Response(ResultVo.faild("分类id不能为空"))

        try:
            category = ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            return Response(ResultVo.faild("分类不存在"))

        for key, value in request_data.items():
            if key != 'id' and key != 'category_code':
                setattr(category, key, value)
        category.save()
        return Response(ResultVo.success("更新成功"))


class CategoryDeleteView(APIView):
    def delete(self, request, category_id):
        try:
            category = ProductCategory.objects.get(id=category_id)
            category.is_delete = 1
            category.save()
            return Response(ResultVo.success("删除成功"))
        except ProductCategory.DoesNotExist:
            return Response(ResultVo.faild("分类不存在"))


# ===============商品====================================
class ProductListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        product_name = request.GET.get('product_name', '')
        category_id = request.GET.get('category_id', '')

        query = Product.objects.filter(is_delete=0)
        if product_name:
            query = query.filter(product_name__icontains=product_name)
        if category_id:
            query = query.filter(category_id=category_id)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        serializer_data = ProductSerializer(page_data, many=True)
        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': serializer_data.data
        }
        return Response(ResultVo.success("查询成功", response_data))


class ProductAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        product_code = 'PD_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + uuid_random
        request_data['product_code'] = product_code

# 后面换真实的id
        if 'unit_id' not in request_data or not request_data['unit_id']:
            request_data['unit_id'] = 1
        if 'brand_id' not in request_data or not request_data['brand_id']:
            request_data['brand_id'] = 1
        if 'specification_id' not in request_data or not request_data['specification_id']:
            request_data['specification_id'] = 1
        if not request_data.get('image_url'):
            request_data['image_url'] = ''

        serializer = ProductSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class ProductUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        product_id = request_data.get('id')
        if not product_id:
            return Response(ResultVo.faild("商品id不能为空"))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(ResultVo.faild("商品不存在"))

        for key, value in request_data.items():
            if key != 'id' and key != 'product_code':
                setattr(product, key, value)
        product.save()
        return Response(ResultVo.success("更新成功"))


class ProductDeleteView(APIView):
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.is_delete = 1
            product.save()
            return Response(ResultVo.success("删除成功"))
        except Product.DoesNotExist:
            return Response(ResultVo.faild("商品不存在"))


class CategorySimpleListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.filter(is_delete=0).order_by('sort_order')
        serializer_data = ProductCategorySerializer(categories, many=True)
        return Response(ResultVo.success("查询成功", serializer_data.data))


# ===============供应商====================================
class SupplierListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        supplier_name = request.GET.get('supplier_name', '')

        query = Supplier.objects.filter(is_delete=0)
        if supplier_name:
            query = query.filter(supplier_name__icontains=supplier_name)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        serializer_data = SupplierSerializer(page_data, many=True)
        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': serializer_data.data
        }
        return Response(ResultVo.success("查询成功", response_data))


class SupplierAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        supplier_code = 'SUP_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + uuid_random
        request_data['supplier_code'] = supplier_code

        serializer = SupplierSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class SupplierUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        supplier_id = request_data.get('id')
        if not supplier_id:
            return Response(ResultVo.faild("供应商id不能为空"))

        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return Response(ResultVo.faild("供应商不存在"))

        for key, value in request_data.items():
            if key != 'id' and key != 'supplier_code':
                setattr(supplier, key, value)
        supplier.save()
        return Response(ResultVo.success("更新成功"))


class SupplierDeleteView(APIView):
    def delete(self, request, supplier_id):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier.is_delete = 1
            supplier.save()
            return Response(ResultVo.success("删除成功"))
        except Supplier.DoesNotExist:
            return Response(ResultVo.faild("供应商不存在"))