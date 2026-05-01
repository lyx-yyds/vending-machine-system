from django.db import models

# Create your models here.


# CREATE TABLE t_order (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID',
#     order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单编号',
#     machine_id INT COMMENT '售货机ID',
#     user_id INT COMMENT '用户ID（可为空表示匿名购买）',
#     total_amount DECIMAL(10,2) NOT NULL COMMENT '订单总金额',
#     pay_amount DECIMAL(10,2) NOT NULL COMMENT '实付金额',
# --     discount_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '优惠金额',
#     order_type INT DEFAULT 1 COMMENT '订单类型：1-线上支付，2-货到付款，3-扫码支付',
#     pay_type INT DEFAULT 1 COMMENT '支付方式：1-微信，2-支付宝，3-会员卡，4-现金',
#     pay_status INT DEFAULT 0 COMMENT '支付状态：0-待支付，1-已支付，2-已退款',
#     pay_time DATETIME COMMENT '支付时间',
#     order_status INT DEFAULT 0 COMMENT '订单状态：0-待处理，1-进行中，2-已完成，3-已取消，4-退款中',
# --     order_source VARCHAR(50) COMMENT '订单来源（如：小程序、APP、机身）',
#     device_no VARCHAR(50) COMMENT '设备编号',
#     cabinet_no VARCHAR(20) COMMENT '取餐柜编号',
#     pickup_code VARCHAR(20) COMMENT '取餐码',
#     expected_pickup_time DATETIME COMMENT '预计取餐时间',
#     actual_pickup_time DATETIME COMMENT '实际取餐时间',
#     cancel_time DATETIME COMMENT '取消时间',
#     cancel_reason VARCHAR(500) COMMENT '取消原因',
#     remark VARCHAR(500) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (machine_id) REFERENCES t_machine(id),
#     FOREIGN KEY (user_id) REFERENCES t_user(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';



class Order(models.Model):
    order_no = models.CharField(max_length=50, unique=True, verbose_name='订单编号')
    machine_id = models.IntegerField(null=True, blank=True, verbose_name='售货机ID')
    user_id = models.IntegerField(verbose_name='用户ID（可为空表示匿名购买）')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='订单总金额')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实付金额')
    order_type = models.IntegerField(default=1, verbose_name='订单类型')
    pay_type = models.IntegerField(default=1, verbose_name='支付方式')
    pay_status = models.IntegerField(default=0, verbose_name='支付状态')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    order_status = models.IntegerField(default=0, verbose_name='订单状态')
    device_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='设备编号')
    cabinet_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='取餐柜编号')
    pickup_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='取餐码')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 't_order'
        verbose_name = '订单'
        verbose_name_plural = '订单'



# -- ----------------------------
# -- 12. 订单明细表
# -- ----------------------------
# DROP TABLE IF EXISTS t_order_detail;
# CREATE TABLE t_order_detail (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '明细ID',
#     order_id INT NOT NULL COMMENT '订单ID',
#     product_id INT NOT NULL COMMENT '商品ID',
#     aisle_id INT COMMENT '货道ID',
#     product_name VARCHAR(100) COMMENT '商品名称（冗余字段）',
#     product_image VARCHAR(200) COMMENT '商品图片（冗余字段）',
#     quantity INT NOT NULL COMMENT '购买数量',
#     unit_price DECIMAL(10,2) NOT NULL COMMENT '单价',
#     total_price DECIMAL(10,2) NOT NULL COMMENT '小计金额',
#     cost_price DECIMAL(10,2) COMMENT '成本单价（冗余字段）',
#     remark VARCHAR(200) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     FOREIGN KEY (order_id) REFERENCES t_order(id),
#     FOREIGN KEY (product_id) REFERENCES t_product(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';


class OrderDetail(models.Model):
    order_id = models.IntegerField(verbose_name='订单ID')
    product_id = models.IntegerField(verbose_name='商品ID')
    aisle_id = models.IntegerField(verbose_name='货道ID')
    product_name = models.CharField(max_length=100, verbose_name='商品名称（冗余字段）')
    product_image = models.CharField(max_length=200, verbose_name='商品图片（冗余字段）')
    quantity = models.IntegerField(verbose_name='购买数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计金额')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='成本单价（冗余字段）')
    remark = models.TextField(max_length=500, null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = 't_order_detail'
        verbose_name = '订单明细'
        verbose_name_plural = '订单明细'
