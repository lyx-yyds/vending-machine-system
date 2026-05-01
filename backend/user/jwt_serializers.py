from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.contrib.auth import authenticate

# 自定义 JWT 序列化器
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 重写用户名密码校验逻辑，适配你的自定义 User 表
    def validate(self, attrs):
        # 从请求中获取用户名密码
        username = attrs.get("username")
        password = attrs.get("password")
        
        # 手动校验你的自定义 User 表
        user = User.objects.filter(username=username, is_deleted=0).first()
        if not user or not user.check_password(password):
            raise self.fail("no_active_account")  # 统一错误提示
        if user.status == 1:
            raise self.fail("account_disabled")
        
        # 生成 JWT token
        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            # 自定义返回字段（可选）
            "user_id": user.id,
            "username": user.username
        }
        return data

# 自定义 JWT 视图
from rest_framework_simplejwt.views import TokenObtainPairView
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer