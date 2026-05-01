from .serializers import PaymentSerializer, RefundSerializer
from .models import Payment, Refund
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo


class PaymentListView(APIView):
    def get(self, request):
        import traceback
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        order_no = request.GET.get('order_no', '')

        try:
            query = Payment.objects.all()
            if order_no:
                query = query.filter(order_no__icontains=order_no)

            paginator = Paginator(query, page_size)
            page_data = paginator.get_page(page_num)

            result_list = []
            for payment in page_data:
                result_list.append({
                    'id': payment.id,
                    'payment_no': payment.payment_no,
                    'order_id': payment.order_id.id if payment.order_id else None,
                    'order_no': payment.order_no,
                    'user_id': payment.user_id.id if payment.user_id else None,
                    'pay_type': payment.pay_type,
                    'pay_amount': float(payment.pay_amount) if payment.pay_amount else 0,
                    'pay_status': payment.pay_status,
                    'pay_time': payment.pay_time.strftime('%Y-%m-%d %H:%M:%S') if payment.pay_time else None,
                    'transaction_id': payment.transaction_id,
                    'remark': payment.remark,
                    'create_time': payment.create_time.strftime('%Y-%m-%d %H:%M:%S') if payment.create_time else None,
                })

            response_data = {
                'total': paginator.count,
                'pageNum': int(page_num),
                'pageSize': page_size,
                'list': result_list
            }
            return Response(ResultVo.success("查询成功", response_data))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"查询失败: {str(e)}"))


class RefundListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        order_no = request.GET.get('order_no', '')

        query = Refund.objects.all()
        if order_no:
            query = query.filter(order_no__icontains=order_no)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for refund in page_data:
            result_list.append({
                'id': refund.id,
                'refund_no': refund.refund_no,
                'order_id': refund.order_id.id if refund.order_id else None,
                'order_no': refund.order_no,
                'user_id': refund.user_id.id if refund.user_id else None,
                'refund_amount': float(refund.refund_amount) if refund.refund_amount else 0,
                'refund_type': refund.refund_type,
                'refund_reason': refund.refund_reason,
                'refund_status': refund.refund_status,
                'apply_time': refund.apply_time.strftime('%Y-%m-%d %H:%M:%S') if refund.apply_time else None,
                'process_time': refund.process_time.strftime('%Y-%m-%d %H:%M:%S') if refund.process_time else None,
                'process_result': refund.process_result,
                'remark': refund.remark,
                'create_time': refund.create_time.strftime('%Y-%m-%d %H:%M:%S') if refund.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class ProcessRefundView(APIView):
    def put(self, request):
        import traceback
        from datetime import datetime
        refund_id = request.data.get('refund_id')
        action = request.data.get('action')
        process_result = request.data.get('process_result', '')
        admin_id = request.data.get('admin_id')

        if not refund_id or not action:
            return Response(ResultVo.faild("参数不完整"))
        try:
            refund = Refund.objects.get(id=refund_id)
            if refund.refund_status != 0:
                return Response(ResultVo.faild("该退款申请已处理，请勿重复操作"))

            from user.models import User
            admin_obj = None
            if admin_id:
                try:
                    admin_obj = User.objects.get(id=admin_id)
                except User.DoesNotExist:
                    pass

            if action == 'approve':
                refund.refund_status = 2
                refund.order_id.pay_status = 2
                refund.order_id.order_status = 3
                refund.order_id.save()
                process_result = '退款已批准，钱款将原路退回'
            elif action == 'reject':
                refund.refund_status = 3
                process_result = process_result or '退款申请被拒绝'
            else:
                return Response(ResultVo.faild("无效的操作"))

            refund.admin_id = admin_obj
            refund.process_time = datetime.now()
            refund.process_result = process_result
            refund.save()

            return Response(ResultVo.success("处理成功"))
        except Refund.DoesNotExist:
            return Response(ResultVo.faild("退款记录不存在"))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"处理失败: {str(e)}"))
