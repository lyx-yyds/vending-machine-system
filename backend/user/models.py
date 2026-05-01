from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

# CREATE TABLE t_user (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
#     username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
#     password VARCHAR(200) NOT NULL COMMENT '密码（加密）',
#     real_name VARCHAR(50) COMMENT '真实姓名',
#     phone VARCHAR(20) COMMENT '手机号',
#     email VARCHAR(100) COMMENT '邮箱',
#     role_type INT DEFAULT 2 COMMENT '角色：1-管理员，2-普通用户，3-运营人员',
#     balance DECIMAL(10,2) DEFAULT 0.00 COMMENT '账户余额（储值）',
#     status INT DEFAULT 0 COMMENT '状态：0-正常，1-禁用',
#     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    real_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    role_type = models.IntegerField(default=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 直接给实例添加 is_active 属性，JWT 能直接识别
        self.is_active = self.status == 0 and self.is_delete == 0
    
    REQUIRED_FIELDS = []  # JWT 必需的空列表（无额外必填字段）
    USERNAME_FIELD = 'username'  # 指定用户名字段
    is_anonymous = False  # 非匿名用户
    is_authenticated = True  # 标记为已认证（可选，防止后续报错）


    # 设置密码
    def set_pwd(self,pwd):
        self.password = make_password(pwd)

    def check_pwd(self,pwd):
        return check_password(pwd,self.password)

