from rest_framework.views import APIView
from rest_framework.response import Response
from ResultVo import ResultVo
from .models import User
from .serializers import LoginSerializer,RegisterSerializer,UserInfoSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
# ===============注册====================================
class RegisterView(APIView):
    def post(self, request):
        ser=RegisterSerializer(data=request.data)
        if ser.is_valid():
            user=ser.save()
            return Response(ResultVo.success("注册成功",UserInfoSerializer(user).data))
        
        return Response(ResultVo.faild(f"参数错误{ser.errors}"))
        

# ===============登录====================================
class LoginView(APIView):
    def post(self, request):
        ser=LoginSerializer(data=request.data)
        if ser.is_valid():
            user=ser.context["user"]
            # token=secrets.token_hex(32) # 简单安全的token
                # 生成 JWT token（自动适配 AUTH_USER_MODEL 配置的表）
            refresh = RefreshToken.for_user(user)
            token=str(refresh.access_token)
            
            return Response(ResultVo.success("登录成功",{"token":token,"refresh":str(refresh),
            "user":UserInfoSerializer(user).data}))
        return Response(ResultVo.faild(f"参数错误{ser.errors}"))
    
    
# ===============登录验证装饰器（给其他接口）====================================
from functools import wraps
def login_require(view_funcs):
    @wraps(view_funcs)
    def wrapper(request,*args,**kwargs):
        token=request.headers.get("token")
        if not token:
            return Response(ResultVo.faild("请先登录",code=401))
        return view_funcs(request,*args,**kwargs)
    return wrapper


class UserListView(APIView):
    def get(self, request):
        page_num = request.GET.get('pageNum', 1)
        page_size = request.GET.get('pageSize', 10)
        username = request.GET.get('username', '')
        real_name = request.GET.get('real_name', '')

        query = User.objects.filter(is_delete=0)
        if username:
            query = query.filter(username__icontains=username)
        if real_name:
            query = query.filter(real_name__icontains=real_name)

        from django.core.paginator import Paginator
        paginator = Paginator(query, page_size)
        page_data = paginator.get_page(page_num)

        result_list = []
        for user in page_data:
            result_list.append({
                'id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'phone': user.phone,
                'email': user.email,
                'role_type': user.role_type,
                'balance': float(user.balance) if user.balance else 0,
                'status': user.status,
                'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S') if user.create_time else None,
            })

        response_data = {
            'total': paginator.count,
            'pageNum': int(page_num),
            'pageSize': page_size,
            'list': result_list
        }
        return Response(ResultVo.success("查询成功", response_data))


class UserStatusUpdateView(APIView):
    def put(self, request):
        user_id = request.data.get('id')
        status = request.data.get('status')
        if not user_id or status is None:
            return Response(ResultVo.faild("参数错误"))
        try:
            user = User.objects.get(id=user_id)
            user.status = status
            user.save()
            return Response(ResultVo.success("状态更新成功"))
        except User.DoesNotExist:
            return Response(ResultVo.faild("用户不存在"))


class UserPasswordResetView(APIView):
    def put(self, request):
        user_id = request.data.get('id')
        new_password = request.data.get('password')
        if not user_id or not new_password:
            return Response(ResultVo.faild("参数错误"))
        try:
            user = User.objects.get(id=user_id)
            user.set_pwd(new_password)
            user.save()
            return Response(ResultVo.success("密码修改成功"))
        except User.DoesNotExist:
            return Response(ResultVo.faild("用户不存在"))


class UserProfileView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response(ResultVo.faild("用户ID不能为空"))
        try:
            user = User.objects.get(id=user_id)
            return Response(ResultVo.success("查询成功", {
                'id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'phone': user.phone,
                'email': user.email,
                'role_type': user.role_type,
                'balance': float(user.balance) if user.balance else 0,
                'status': user.status,
            }))
        except User.DoesNotExist:
            return Response(ResultVo.faild("用户不存在"))

    def put(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response(ResultVo.faild("用户ID不能为空"))
        try:
            user = User.objects.get(id=user_id)
            real_name = request.data.get('real_name')
            phone = request.data.get('phone')
            email = request.data.get('email')
            if real_name:
                user.real_name = real_name
            if phone:
                user.phone = phone
            if email:
                user.email = email
            user.save()
            return Response(ResultVo.success("更新成功"))
        except User.DoesNotExist:
            return Response(ResultVo.faild("用户不存在"))


class ChangePasswordView(APIView):
    def put(self, request):
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user_id or not old_password or not new_password:
            return Response(ResultVo.faild("参数错误"))
        try:
            user = User.objects.get(id=user_id)
            if not user.check_pwd(old_password):
                return Response(ResultVo.faild("原密码错误"))
            user.set_pwd(new_password)
            user.save()
            return Response(ResultVo.success("密码修改成功"))
        except User.DoesNotExist:
            return Response(ResultVo.faild("用户不存在"))