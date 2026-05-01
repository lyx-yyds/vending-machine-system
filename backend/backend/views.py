from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from ResultVo import ResultVo
from order.models import Order, OrderDetail
from product.models import Product
from stock.models import Stock
from user.models import User
from payment.models import Payment, Refund
import datetime


class DashboardView(APIView):
    def get(self, request):
        try:
            today = timezone.now().date()
            start_of_day = timezone.make_aware(
                datetime.datetime.combine(today, datetime.time.min)
            )
            end_of_day = timezone.make_aware(
                datetime.datetime.combine(today, datetime.time.max)
            )

            today_orders = Order.objects.filter(
                create_time__gte=start_of_day,
                create_time__lte=end_of_day
            )

            today_order_count = today_orders.count()
            today_revenue = today_orders.aggregate(
                total=Sum('pay_amount')
            )['total'] or 0

            total_products = Product.objects.count()
            total_users = User.objects.count()

            pending_orders = Order.objects.filter(order_status=0).count()

            low_stock_count = Stock.objects.filter(
                warehouse_stock__lt=10
            ).count()

            recent_orders = Order.objects.order_by('-create_time')[:10]

            recent_order_list = []
            for order in recent_orders:
                recent_order_list.append({
                    'id': order.id,
                    'order_no': order.order_no,
                    'total_amount': float(order.total_amount),
                    'pay_status': order.pay_status,
                    'order_status': order.order_status,
                    'create_time': order.create_time.strftime('%Y-%m-%d %H:%M') if order.create_time else '',
                })

            return Response(ResultVo.success("获取成功", {
                'today_order_count': today_order_count,
                'today_revenue': float(today_revenue),
                'total_products': total_products,
                'total_users': total_users,
                'pending_orders': pending_orders,
                'low_stock_count': low_stock_count,
                'recent_orders': recent_order_list,
            }))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(ResultVo.faild(f"获取失败: {str(e)}"))