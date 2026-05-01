from product.models import Product
from django.db import models

# Create your models here.


# CREATE TABLE t_stock (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '库存ID',
#     product_id INT NOT NULL COMMENT '商品ID',
#     machine_id INT COMMENT '设备ID（NULL表示仓库库存）',
#     warehouse_stock INT DEFAULT 0 COMMENT '仓库库存数量',
#     machine_stock INT DEFAULT 0 COMMENT '机器库存数量',
#     total_stock INT DEFAULT 0 COMMENT '总库存数量',
#     min_stock INT DEFAULT 0 COMMENT '最小库存预警值',
#     cost_price DECIMAL(10,2) COMMENT '成本价（记录入库价格）',
#     last_inbound_date DATETIME COMMENT '最后入库时间',
#     last_outbound_date DATETIME COMMENT '最后出库时间',
#     remark VARCHAR(500) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (product_id) REFERENCES t_product(id),
#     FOREIGN KEY (machine_id) REFERENCES t_machine(id),
#     UNIQUE KEY uk_product_machine (product_id, machine_id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='库存表';


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    # machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备')
    warehouse_stock = models.IntegerField(default=0, verbose_name='仓库库存数量')
    machine_stock = models.IntegerField(default=0, verbose_name='机器库存数量')
    total_stock = models.IntegerField(default=0, verbose_name='总库存数量')
    min_stock = models.IntegerField(default=0, verbose_name='最小库存预警值')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='成本价（记录入库价格）')
    last_inbound_date = models.DateTimeField(null=True, blank=True, verbose_name='最后入库时间')
    last_outbound_date = models.DateTimeField(null=True, blank=True, verbose_name='最后出库时间')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        db_table = 't_stock'
        verbose_name = '库存'
        verbose_name_plural = '库存'
