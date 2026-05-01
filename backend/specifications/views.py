from .serializers import SpecificationSerializer
from .models import Specification
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from uuid import uuid4


class SpecificationListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        spec_name = request.GET.get('spec_name', '')

        query = Specification.objects.filter(is_delete=0)
        if spec_name:
            query = query.filter(spec_name__icontains=spec_name)

        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for spec in page_data:
            result_list.append({
                'id': spec.id,
                'spec_code': spec.spec_code,
                'spec_name': spec.spec_name,
                'remark': spec.remark,
                'status': spec.status,
                'create_time': spec.create_time.strftime('%Y-%m-%d %H:%M:%S') if spec.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class SpecificationAddView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        uuid_random = uuid4().hex[:6]
        spec_code = 'SPEC_' + uuid_random.upper()
        request_data['spec_code'] = spec_code
        serializer = SpecificationSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResultVo.success("添加成功"))
        return Response(ResultVo.faild(f"添加失败{serializer.errors}"))


class SpecificationUpdateView(APIView):
    def put(self, request):
        request_data = request.data.copy()
        spec_id = request_data.get('id')
        if not spec_id:
            return Response(ResultVo.faild("规格id不能为空"))

        try:
            spec = Specification.objects.get(id=spec_id)
        except Specification.DoesNotExist:
            return Response(ResultVo.faild("规格不存在"))

        for key, value in request_data.items():
            if key != 'id' and key != 'create_time':
                setattr(spec, key, value)
        spec.save()
        return Response(ResultVo.success("更新成功"))


class SpecificationDeleteView(APIView):
    def delete(self, request, spec_id):
        try:
            spec = Specification.objects.get(id=spec_id)
            spec.is_delete = 1
            spec.save()
            return Response(ResultVo.success("删除成功"))
        except Specification.DoesNotExist:
            return Response(ResultVo.faild("规格不存在"))


class SpecificationSimpleListView(APIView):
    def get(self, request):
        specs = Specification.objects.filter(is_delete=0).order_by('id')
        result_list = []
        for spec in specs:
            result_list.append({
                'id': spec.id,
                'spec_code': spec.spec_code,
                'spec_name': spec.spec_name,
            })
        return Response(ResultVo.success("查询成功", result_list))
