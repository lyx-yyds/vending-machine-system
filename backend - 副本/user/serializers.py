from rest_framework import serializers
from .models import User


# 注册序列化器
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields=["username","password","confirm_password","real_name","phone","email","role_type"]

    def validate(self,data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("两次密码不一致")
        if User.objects.filter(username=data["username"],is_delete=0).exists():
            raise serializers.ValidationError("用户名已存在")
        return data

    
    def create(self,validated_data):
        validated_data.pop("confirm_password")
        user=User(**validated_data)
        user.set_pwd(validated_data["password"]) # 密码加密
        user.save()
        return user
    
# 登录序列化器
class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField()
    class Meta:
        model = User
        fields=["username","password"]

    def validate(self, data):
        user=User.objects.filter(username=data["username"],is_delete=0).first()
        if not user or not user.check_pwd(data["password"]):
            raise serializers.ValidationError("用户名或密码错误")
        if user.status==1:
            raise serializers.ValidationError("该用户已被禁用")
        self.context["user"]=user
        return data
    


# 获取用户信息 （不包含密码）
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","username","real_name","phone","email","status","role_type"]

