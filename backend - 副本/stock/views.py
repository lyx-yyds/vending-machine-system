from .serializers import StockSerializer
from .models import Stock
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo


class StockListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        product_name = request.GET.get('product_name', '')
        product_code = request.GET.get('product_code', '')

        query = Stock.objects.all().select_related('product')
        if product_name:
            query = query.filter(product__product_name__icontains=product_name)
        if product_code:
            query = query.filter(product__product_code__icontains=product_code)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for stock in page_data:
            result_list.append({
                'id': stock.id,
                'product_id': stock.product_id,
                'product_name': stock.product.product_name if stock.product else '',
                'product_code': stock.product.product_code if stock.product else '',
                'warehouse_stock': stock.warehouse_stock,
                'machine_stock': stock.machine_stock,
                'total_stock': stock.total_stock,
                'min_stock': stock.min_stock,
                'cost_price': float(stock.cost_price) if stock.cost_price else 0,
                'last_inbound_date': stock.last_inbound_date.strftime('%Y-%m-%d %H:%M:%S') if stock.last_inbound_date else None,
                'last_outbound_date': stock.last_outbound_date.strftime('%Y-%m-%d %H:%M:%S') if stock.last_outbound_date else None,
                'remark': stock.remark,
                'create_time': stock.create_time.strftime('%Y-%m-%d %H:%M:%S') if stock.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))
