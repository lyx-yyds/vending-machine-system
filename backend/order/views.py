from .serializers import OrderSerializer, OrderDetailSerializer
from .models import Order, OrderDetail
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from datetime import datetime


class OrderListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        order_no = request.GET.get('order_no', '')

        query = Order.objects.all()
        if order_no:
            query = query.filter(order_no__icontains=order_no)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for order in page_data:
            result_list.append({
                'id': order.id,
                'order_no': order.order_no,
                'machine_id': order.machine_id,
                'user_id': order.user_id,
                'total_amount': float(order.total_amount) if order.total_amount else 0,
                'pay_amount': float(order.pay_amount) if order.pay_amount else 0,
                'order_type': order.order_type,
                'pay_type': order.pay_type,
                'pay_status': order.pay_status,
                'pay_time': order.pay_time.strftime('%Y-%m-%d %H:%M:%S') if order.pay_time else None,
                'order_status': order.order_status,
                'device_no': order.device_no,
                'cabinet_no': order.cabinet_no,
                'pickup_code': order.pickup_code,
                'remark': order.remark,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S') if order.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class MyOrderListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        user_id = request.GET.get('user_id', '')
        order_no = request.GET.get('order_no', '')

        query = Order.objects.all()
        if user_id:
            query = query.filter(user_id=user_id)
        if order_no:
            query = query.filter(order_no__icontains=order_no)

        query = query.order_by('-create_time')

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for order in page_data:
            result_list.append({
                'id': order.id,
                'order_no': order.order_no,
                'machine_id': order.machine_id,
                'user_id': order.user_id,
                'total_amount': float(order.total_amount) if order.total_amount else 0,
                'pay_amount': float(order.pay_amount) if order.pay_amount else 0,
                'order_type': order.order_type,
                'pay_type': order.pay_type,
                'pay_status': order.pay_status,
                'pay_time': order.pay_time.strftime('%Y-%m-%d %H:%M:%S') if order.pay_time else None,
                'order_status': order.order_status,
                'device_no': order.device_no,
                'cabinet_no': order.cabinet_no,
                'pickup_code': order.pickup_code,
                'remark': order.remark,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S') if order.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class OrderDetailListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        order_id = request.GET.get('order_id', '')

        query = OrderDetail.objects.all()
        if order_id:
            query = query.filter(order_id=order_id)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for detail in page_data:
            result_list.append({
                'id': detail.id,
                'order_id': detail.order_id,
                'product_id': detail.product_id,
                'aisle_id': detail.aisle_id,
                'product_name': detail.product_name,
                'product_image': detail.product_image,
                'quantity': detail.quantity,
                'unit_price': float(detail.unit_price) if detail.unit_price else 0,
                'total_price': float(detail.total_price) if detail.total_price else 0,
                'cost_price': float(detail.cost_price) if detail.cost_price else 0,
                'remark': detail.remark,
                'create_time': detail.create_time.strftime('%Y-%m-%d %H:%M:%S') if detail.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class CreateOrderView(APIView):
    def post(self, request):
        import traceback
        try:
            user_id = request.data.get('user_id')
            machine_id = request.data.get('machine_id', 1)
            remarks = request.data.get('remark', '')
            items = request.data.get('items', [])

            if not user_id:
                return Response(ResultVo.faild("用户ID不能为空"))
            if not items or len(items) == 0:
                return Response(ResultVo.faild("购物车不能为空"))

            from datetime import datetime
            order_no = f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            total_amount = 0
            order_details = []
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity', 1)

                try:
                    from product.models import Product
                    product = Product.objects.get(id=product_id)
                    price = float(product.selling_price) if product.selling_price else 0
                    item_total = price * quantity
                    total_amount += item_total

                    order_details.append({
                        'product_id': product_id,
                        'product_name': product.product_name,
                        'product_image': product.image_url or '',
                        'quantity': quantity,
                        'unit_price': price,
                        'total_price': item_total,
                    })
                except Product.DoesNotExist:
                    return Response(ResultVo.faild(f"商品ID {product_id} 不存在"))

            import random
            pickup_code = str(random.randint(1000, 9999))

            order = Order.objects.create(
                order_no=order_no,
                machine_id=1,
                user_id=int(user_id),
                total_amount=total_amount,
                pay_amount=total_amount,
                order_type=1,
                pay_type=1,
                pay_status=0,
                order_status=0,
                pickup_code=pickup_code,
                remark=remarks,
            )

            for detail in order_details:
                OrderDetail.objects.create(
                    order_id=order.id,
                    product_id=detail['product_id'],
                    aisle_id=0,
                    product_name=detail['product_name'],
                    product_image=detail['product_image'],
                    quantity=detail['quantity'],
                    unit_price=detail['unit_price'],
                    total_price=detail['total_price'],
                )

            return Response(ResultVo.success("下单成功", {
                'order_id': order.id,
                'order_no': order.order_no,
                'pickup_code': order.pickup_code,
                'total_amount': float(order.total_amount),
            }))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"下单失败: {str(e)}"))


class PayOrderView(APIView):
    def put(self, request):
        import traceback
        order_id = request.data.get('order_id')
        pay_type = request.data.get('pay_type', 1)
        if not order_id:
            return Response(ResultVo.faild("订单ID不能为空"))
        try:
            order = Order.objects.get(id=order_id)
            if order.pay_status == 1:
                return Response(ResultVo.faild("订单已支付，请勿重复支付"))

            order.pay_status = 1
            order.order_status = 1
            order.pay_type = pay_type
            order.pay_time = datetime.now()
            order.save()

            from payment.models import Payment
            from user.models import User
            import random
            payment_no = f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

            user_obj = None
            if order.user_id:
                user_obj = User.objects.get(id=order.user_id)

            Payment.objects.create(
                payment_no=payment_no,
                order_id=order,
                order_no=order.order_no,
                user_id=user_obj,
                pay_type=pay_type,
                pay_amount=order.pay_amount,
                pay_status=1,
                pay_time=datetime.now(),
            )

            return Response(ResultVo.success("支付成功"))
        except Order.DoesNotExist:
            return Response(ResultVo.faild("订单不存在"))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"支付失败: {str(e)}"))


class RefundOrderView(APIView):
    def post(self, request):
        import traceback
        order_id = request.data.get('order_id')
        refund_reason = request.data.get('refund_reason', '用户申请退款')
        if not order_id:
            return Response(ResultVo.faild("订单ID不能为空"))
        try:
            order = Order.objects.get(id=order_id)
            if order.pay_status != 1:
                return Response(ResultVo.faild("只有已支付的订单才能退款"))

            from payment.models import Refund
            import random
            refund_no = f"REF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

            from user.models import User
            user_obj = None
            if order.user_id:
                user_obj = User.objects.get(id=order.user_id)

            Refund.objects.create(
                refund_no=refund_no,
                order_id=order,
                order_no=order.order_no,
                user_id=user_obj,
                refund_amount=order.pay_amount,
                refund_type=1,
                refund_reason=refund_reason,
                refund_status=0,
            )

            return Response(ResultVo.success("退款申请已提交"))
        except Order.DoesNotExist:
            return Response(ResultVo.faild("订单不存在"))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"退款失败: {str(e)}"))
