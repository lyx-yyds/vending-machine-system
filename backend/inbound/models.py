from django.db import models

# Create your models here.


# CREATE TABLE t_inbound_record (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '入库记录ID',
#     inbound_no VARCHAR(50) NOT NULL UNIQUE COMMENT '入库单编号',
#     inbound_type INT NOT NULL COMMENT '入库类型：1-采购入库，2-退货入库，3-调拨入库，4-补货入库',
#     supplier_id INT COMMENT '供应商ID（采购入库时）',
#     machine_id INT COMMENT '售货机ID（补货入库时）',
#     warehouse_id INT COMMENT '仓库ID',
#     total_quantity INT DEFAULT 0 COMMENT '总数量',
#     total_amount DECIMAL(12,2) DEFAULT 0.00 COMMENT '总金额',
#     status INT DEFAULT 0 COMMENT '状态：0-待审核，1-已入库，2-已取消',
#     inbound_time DATETIME COMMENT '实际入库时间',
#     operator_id INT COMMENT '操作员ID',
#     approver_id INT COMMENT '审核人ID',
#     remark VARCHAR(500) COMMENT '备注',
#     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     create_user_id INT DEFAULT 0 COMMENT '创建人ID',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (supplier_id) REFERENCES t_supplier(id),
#     FOREIGN KEY (machine_id) REFERENCES t_machine(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='入库记录表';


class InboundRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='入库记录ID')
    inbound_no = models.CharField(max_length=50, unique=True, verbose_name='入库单编号')
    inbound_type = models.IntegerField(verbose_name='入库类型')
    supplier_id = models.IntegerField(null=True, blank=True, verbose_name='供应商ID（采购入库时）')
    machine_id = models.IntegerField(null=True, blank=True, verbose_name='售货机ID（补货入库时）')
    warehouse_id = models.IntegerField(verbose_name='仓库ID')
    total_quantity = models.IntegerField(default=0, verbose_name='总数量')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='总金额')
    status = models.IntegerField(default=0, verbose_name='状态：0-待审核，1-已入库，2-已取消')
    inbound_time = models.DateTimeField(null=True, blank=True, verbose_name='实际入库时间')
    operator_id = models.IntegerField(null=True, blank=True, verbose_name='操作员ID')
    approver_id = models.IntegerField(null=True, blank=True, verbose_name='审核人ID')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    is_delete = models.IntegerField(default=0, verbose_name='删除标志：0-未删除，1-已删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    create_user_id = models.IntegerField(default=0, verbose_name='创建人ID')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 't_inbound_record'
        verbose_name = '入库记录'
        verbose_name_plural = '入库记录'

# CREATE TABLE t_inbound_detail (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '明细ID',
#     inbound_id INT NOT NULL COMMENT '入库记录ID',
#     product_id INT NOT NULL COMMENT '商品ID',
#     product_name VARCHAR(100) COMMENT '商品名称（冗余）',
#     specification VARCHAR(100) COMMENT '规格（冗余）',
#     unit_id INT COMMENT '单位ID',
#     unit_name VARCHAR(50) COMMENT '单位名称（冗余）',
#     quantity INT NOT NULL COMMENT '入库数量',
#     cost_price DECIMAL(10,2) NOT NULL COMMENT '成本单价',
#     total_amount DECIMAL(12,2) NOT NULL COMMENT '小计金额',
#     batch_no VARCHAR(50) COMMENT '批次号',
#     production_date DATE COMMENT '生产日期',
#     expiry_date DATE COMMENT '有效期至',
#     remark VARCHAR(200) COMMENT '备注',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     FOREIGN KEY (inbound_id) REFERENCES t_inbound_record(id),
#     FOREIGN KEY (product_id) REFERENCES t_product(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='入库明细表';


class InboundDetail(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='明细ID')
    inbound_id = models.IntegerField(verbose_name='入库记录ID')
    product_id = models.IntegerField(verbose_name='商品ID')
    product_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='商品名称（冗余）')
    specification = models.CharField(max_length=100, null=True, blank=True, verbose_name='规格（冗余）')
    unit_id = models.IntegerField(null=True, blank=True, verbose_name='单位ID')
    unit_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='单位ID（冗余）')
    quantity = models.IntegerField(verbose_name='入库数量')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成本单价')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='小计金额')
    batch_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='批次号')
    production_date = models.DateField(null=True, blank=True, verbose_name='生产日期')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='有效期至')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')      


    class Meta:
        db_table = 't_inbound_detail'
        verbose_name = '入库明细'
        verbose_name_plural = '入库明细'
