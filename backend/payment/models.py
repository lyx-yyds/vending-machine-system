from django.db import models
from order.models import Order
from user.models import User

# Create your models here.


# CREATE TABLE t_payment (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '支付ID',
#     payment_no VARCHAR(50) NOT NULL UNIQUE COMMENT '支付流水号',
#     order_id INT NOT NULL COMMENT '订单ID',
#     order_no VARCHAR(50) NOT NULL COMMENT '订单编号（冗余）',
#     user_id INT COMMENT '用户ID',
#     pay_type INT NOT NULL COMMENT '支付方式：1-微信，2-支付宝，3-会员卡，4-现金',
#     pay_amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
#     pay_status INT DEFAULT 0 COMMENT '支付状态：0-待支付，1-成功，2-失败，3-已撤销',
#     pay_time DATETIME COMMENT '支付时间',
#     transaction_id VARCHAR(100) COMMENT '第三方交易流水号',
#     remark VARCHAR(500) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (order_id) REFERENCES t_order(id),
#     FOREIGN KEY (user_id) REFERENCES t_user(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付记录表';

class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    order_no = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_column='user_id')
    pay_type = models.IntegerField(default=1)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_status = models.IntegerField(default=0)
    pay_time = models.DateTimeField(null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    remark = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 't_payment'
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'





# -- ----------------------------
# -- 14. 退款记录表
# -- ----------------------------
# DROP TABLE IF EXISTS t_refund;
# CREATE TABLE t_refund (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '退款ID',
#     refund_no VARCHAR(50) NOT NULL UNIQUE COMMENT '退款单号',
#     order_id INT NOT NULL COMMENT '订单ID',
#     order_no VARCHAR(50) NOT NULL COMMENT '订单编号（冗余）',
#     user_id INT COMMENT '用户ID',
#     refund_amount DECIMAL(10,2) NOT NULL COMMENT '退款金额',
#     refund_type INT DEFAULT 1 COMMENT '退款类型：1-原路退回，2-退到余额',
#     refund_reason VARCHAR(500) NOT NULL COMMENT '退款原因',
#     refund_status INT DEFAULT 0 COMMENT '退款状态：0-待处理，1-处理中，2-已完成，3-已拒绝',
#     apply_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
#     process_time DATETIME COMMENT '处理时间',
#     process_result VARCHAR(500) COMMENT '处理结果',
#     admin_id INT COMMENT '处理人ID',
#     remark VARCHAR(500) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (order_id) REFERENCES t_order(id),
#     FOREIGN KEY (user_id) REFERENCES t_user(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='退款记录表';


class Refund(models.Model):
    refund_no = models.CharField(max_length=50, unique=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    order_no = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_column='user_id', related_name='user_refunds')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_type = models.IntegerField(default=1)
    refund_reason = models.TextField()
    refund_status = models.IntegerField(default=0)
    apply_time = models.DateTimeField(auto_now_add=True)
    process_time = models.DateTimeField(null=True)
    process_result = models.CharField(max_length=500, null=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_column='admin_id', related_name='admin_refunds')
    remark = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_refund'
        verbose_name = '退款记录'
        verbose_name_plural = '退款记录'
   