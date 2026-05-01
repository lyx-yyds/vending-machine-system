import logging
logger = logging.getLogger(__name__)

from .serializers import InboundRecordSerializer, InboundDetailSerializer, InboundRecordSimpleSerializer
from .models import InboundRecord, InboundDetail
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from uuid import uuid4
from datetime import datetime


class InboundRecordListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        inbound_no = request.GET.get('inbound_no', '')

        query = InboundRecord.objects.filter(is_delete=0)
        if inbound_no:
            query = query.filter(inbound_no__icontains=inbound_no)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for record in page_data:
            logger.info(f"Processing inbound record: {record.id}, inbound_no: {record.inbound_no}")
            record_data = {
                'id': record.id,
                'inbound_no': record.inbound_no,
                'inbound_type': record.inbound_type,
                'supplier_id': record.supplier_id,
                'machine_id': record.machine_id,
                'warehouse_id': record.warehouse_id,
                'total_quantity': record.total_quantity,
                'total_amount': float(record.total_amount) if record.total_amount else 0,
                'status': record.status,
                'inbound_time': record.inbound_time.strftime('%Y-%m-%d %H:%M:%S') if record.inbound_time else None,
                'operator_id': record.operator_id,
                'approver_id': record.approver_id,
                'remark': record.remark,
                'is_delete': record.is_delete,
                'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S') if record.create_time else None,
                'create_user_id': record.create_user_id,
                'update_time': record.update_time.strftime('%Y-%m-%d %H:%M:%S') if record.update_time else None,
            }
            details = InboundDetail.objects.filter(inbound_id=record.id)
            details_list = []
            for d in details:
                details_list.append({
                    'id': d.id,
                    'inbound_id': d.inbound_id,
                    'product_id': d.product_id,
                    'product_name': d.product_name,
                    'specification': d.specification,
                    'unit_id': d.unit_id,
                    'unit_name': d.unit_name,
                    'quantity': d.quantity,
                    'cost_price': float(d.cost_price) if d.cost_price else 0,
                    'total_amount': float(d.total_amount) if d.total_amount else 0,
                    'batch_no': d.batch_no,
                    'production_date': d.production_date.isoformat() if d.production_date else None,
                    'expiry_date': d.expiry_date.isoformat() if d.expiry_date else None,
                    'remark': d.remark,
                })
            record_data['details'] = details_list
            logger.info(f"Inbound {record.id} has {len(details_list)} details in response")
            result_list.append(record_data)

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class InboundRecordAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        inbound_no = 'INB_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + uuid_random
        request_data['inbound_no'] = inbound_no

        details_data = request_data.get('details', [])
        if not isinstance(details_data, list):
            details_data = []
        logger.info(f"Received {len(details_data)} details for inbound")

        serializer = InboundRecordSerializer(data=request_data)
        if serializer.is_valid():
            inbound_record = serializer.save()
            inbound_record.inbound_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inbound_record.save()
            logger.info(f"Saved inbound record {inbound_record.id}")

            for detail_data in details_data:
                detail_data['inbound_id'] = inbound_record.id
                if 'total_amount' not in detail_data or not detail_data['total_amount']:
                    detail_data['total_amount'] = float(detail_data.get('quantity', 0)) * float(detail_data.get('cost_price', 0))
                detail_serializer = InboundDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    logger.info(f"Saved detail for inbound {inbound_record.id}")
                else:
                    return Response(ResultVo.faild(f"明细保存失败{detail_serializer.errors}"))

            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class InboundRecordUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        inbound_id = request_data.get('id')
        if not inbound_id:
            return Response(ResultVo.faild("入库记录id不能为空"))

        try:
            inbound = InboundRecord.objects.get(id=inbound_id)
        except InboundRecord.DoesNotExist:
            return Response(ResultVo.faild("入库记录不存在"))

        details_data = request_data.get('details', [])
        if not isinstance(details_data, list):
            details_data = []

        for key, value in request_data.items():
            if key != 'id' and key != 'inbound_no':
                setattr(inbound, key, value)
        inbound.save()

        if details_data:
            InboundDetail.objects.filter(inbound_id=inbound_id).delete()
            for detail_data in details_data:
                detail_data['inbound_id'] = inbound.id
                detail_serializer = InboundDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()

        return Response(ResultVo.success("更新成功"))


class InboundRecordDeleteView(APIView):
    def delete(self, request, inbound_id):
        try:
            inbound = InboundRecord.objects.get(id=inbound_id)
            inbound.is_delete = 1
            inbound.save()
            return Response(ResultVo.success("删除成功"))
        except InboundRecord.DoesNotExist:
            return Response(ResultVo.faild("入库记录不存在"))


class InboundDetailListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        inbound_id = request.GET.get('inbound_id', '')

        logger.info(f"InboundDetailListView: inbound_id={inbound_id}, type={type(inbound_id)}")

        valid_inbound_ids = InboundRecord.objects.filter(is_delete=0).values_list('id', flat=True)
        query = InboundDetail.objects.filter(inbound_id__in=valid_inbound_ids)
        if inbound_id:
            query = query.filter(inbound_id=inbound_id)

        logger.info(f"Query count: {query.count()}")

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        serializer_data = InboundDetailSerializer(page_data, many=True)
        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': serializer_data.data
        }
        return Response(ResultVo.success("查询成功", response_data))


class InboundDetailAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()

        serializer = InboundDetailSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class InboundDetailUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        detail_id = request_data.get('id')
        if not detail_id:
            return Response(ResultVo.faild("明细id不能为空"))

        try:
            detail = InboundDetail.objects.get(id=detail_id)
        except InboundDetail.DoesNotExist:
            return Response(ResultVo.faild("明细不存在"))

        for key, value in request_data.items():
            if key != 'id':
                setattr(detail, key, value)
        detail.save()
        return Response(ResultVo.success("更新成功"))


class InboundDetailDeleteView(APIView):
    def delete(self, request, detail_id):
        try:
            detail = InboundDetail.objects.get(id=detail_id)
            detail.delete()
            return Response(ResultVo.success("删除成功"))
        except InboundDetail.DoesNotExist:
            return Response(ResultVo.faild("明细不存在"))


class InboundConfirmView(APIView):
    def put(self, request):
        import traceback
        inbound_id = request.data.get('inbound_id')
        if not inbound_id:
            return Response(ResultVo.faild("入库记录ID不能为空"))
        try:
            inbound = InboundRecord.objects.get(id=inbound_id)
            if inbound.status != 0:
                return Response(ResultVo.faild("该入库记录已处理，请勿重复操作"))

            inbound.status = 1
            inbound.inbound_time = datetime.now()
            inbound.save()

            details = InboundDetail.objects.filter(inbound_id=inbound_id)
            from stock.models import Stock

            for detail in details:
                stock, created = Stock.objects.get_or_create(
                    product_id=detail.product_id,
                    defaults={
                        'warehouse_stock': 0,
                        'machine_stock': 0,
                        'total_stock': 0,
                        'cost_price': detail.cost_price,
                        'last_inbound_date': datetime.now(),
                    }
                )

                if inbound.inbound_type == 4:
                    stock.machine_stock += detail.quantity
                else:
                    stock.warehouse_stock += detail.quantity

                stock.total_stock = stock.warehouse_stock + stock.machine_stock
                stock.cost_price = detail.cost_price
                stock.last_inbound_date = datetime.now()
                stock.save()

            return Response(ResultVo.success("入库确认成功，库存已更新"))
        except InboundRecord.DoesNotExist:
            return Response(ResultVo.faild("入库记录不存在"))
        except Exception as e:
            traceback.print_exc()
            return Response(ResultVo.faild(f"操作失败: {str(e)}"))