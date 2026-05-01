# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from os import path,makedirs
from time import time
from .serializer import UploadFileSerializer
from ResultVo import ResultVo
from django.conf import settings
from uuid import uuid4
# Create your views here.


class UploadFileView(APIView):
    def post(self, request):
        serializer=UploadFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(ResultVo.faild("参数错误"))
        
        # 获取文件
        file_obj=serializer.validated_data['file']
        # {file:"xxx/sss/1.png"}  ['xxx/sss/1','.png']
        # 文件名：时间戳+原后缀
        ext=path.splitext(file_obj.name)[-1]
        file_name=f"{uuid4()}{ext}"

        # 保存路径
        save_dir=path.join(settings.MEDIA_ROOT,"uploads")
        
        if not path.exists(save_dir):
            makedirs(save_dir)
        # media/uploads/   20040908223333.png
        file_path=path.join(save_dir,file_name)

        # 写入文件
        with open(file_path,"wb+") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        
        # 返回可访问URL
        file_url=f"{settings.MEDIA_URL}uploads/{file_name}"
        return Response(ResultVo.success("上传成功",{
            "url":file_url,
            "name":file_obj.name,
            "size":file_obj.size
        }))