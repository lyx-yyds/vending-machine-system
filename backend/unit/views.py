from .serializers import UnitSerializer
from .models import Unit
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from uuid import uuid4


class UnitListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        unit_name = request.GET.get('unit_name', '')

        query = Unit.objects.filter(is_delete=0)
        if unit_name:
            query = query.filter(unit_name__icontains=unit_name)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for unit in page_data:
            result_list.append({
                'id': unit.id,
                'unit_code': unit.unit_code,
                'unit_name': unit.unit_name,
                'remark': unit.remark,
                'status': unit.status,
                'create_time': unit.create_time.strftime('%Y-%m-%d %H:%M:%S') if unit.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class UnitAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        unit_code = 'UNIT_' + uuid_random.upper()
        request_data['unit_code'] = unit_code
        serializer = UnitSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class UnitUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        unit_id = request_data.get('id')
        if not unit_id:
            return Response(ResultVo.faild("单位id不能为空"))

        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            return Response(ResultVo.faild("单位不存在"))

        for key, value in request_data.items():
            if key != 'id' and key != 'create_time':
                setattr(unit, key, value)
        unit.save()
        return Response(ResultVo.success("更新成功"))


class UnitDeleteView(APIView):
    def delete(self, request, unit_id):
        try:
            unit = Unit.objects.get(id=unit_id)
            unit.is_delete = 1
            unit.save()
            return Response(ResultVo.success("删除成功"))
        except Unit.DoesNotExist:
            return Response(ResultVo.faild("单位不存在"))


class UnitSimpleListView(APIView):
    def get(self, request):
        units = Unit.objects.filter(is_delete=0).order_by('id')
        result_list = []
        for unit in units:
            result_list.append({
                'id': unit.id,
                'unit_code': unit.unit_code,
                'unit_name': unit.unit_name,
            })
        return Response(ResultVo.success("查询成功", result_list))
