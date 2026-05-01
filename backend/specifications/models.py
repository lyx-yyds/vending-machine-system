from django.db import models

# Create your models here.


# CREATE TABLE t_specification (
# --     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '规格ID',
# --     spec_code VARCHAR(50) NOT NULL UNIQUE COMMENT '规格编码',
# --     spec_name VARCHAR(100) NOT NULL COMMENT '规格名称（如：500ml、1L）',
# --     remark VARCHAR(200) COMMENT '备注',
# --     status INT DEFAULT 0 COMMENT '状态：0-正常，1-禁用',
# --     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
# --     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
# --     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
# -- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='规格表';

class Specification(models.Model):
    spec_code = models.CharField(max_length=50, unique=True, verbose_name='规格编码')
    spec_name = models.CharField(max_length=100, verbose_name='规格名称')
    remark = models.TextField(max_length=200, null=True, blank=True, verbose_name='备注')
    status = models.IntegerField(default=0, verbose_name='状态')
    is_delete = models.IntegerField(default=0, verbose_name='删除标志')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 't_specification'
        verbose_name = '规格'
        verbose_name_plural = '规格'