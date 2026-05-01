from django.db import models

# Create your models here.


# CREATE TABLE t_product_category (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '分类ID',
#     category_code VARCHAR(50) NOT NULL UNIQUE COMMENT '分类编码',
#     category_name VARCHAR(100) NOT NULL COMMENT '分类名称',
#     parent_id INT DEFAULT 0 COMMENT '父级ID（0表示顶级）',
#     sort_order INT DEFAULT 0 COMMENT '排序',
#     status INT DEFAULT 0 COMMENT '状态：0-正常，1-禁用',
#     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

class ProductCategory(models.Model):
    category_code = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=100)
    parent_id = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 't_product_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'


# CREATE TABLE t_product (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '商品ID',
#     product_code VARCHAR(50) NOT NULL UNIQUE COMMENT '商品编码',
#     product_name VARCHAR(100) NOT NULL COMMENT '商品名称',
#     category_id INT COMMENT '分类ID',
#     unit_id INT COMMENT '单位ID',
#     brand_id INT COMMENT '品牌ID',
#     specification_id INT COMMENT '规格ID',
#     cost_price DECIMAL(10,2) DEFAULT 0.00 COMMENT '成本价',
#     selling_price DECIMAL(10,2) NOT NULL COMMENT '售价',
#     image_url VARCHAR(200) COMMENT '商品图片URL',
#     remark VARCHAR(500) COMMENT '备注',
#     status INT DEFAULT 1 COMMENT '状态：0-下架，1-上架',
#     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     create_user_id INT DEFAULT 0 COMMENT '创建人ID',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#     FOREIGN KEY (category_id) REFERENCES t_product_category(id),
#     FOREIGN KEY (unit_id) REFERENCES t_unit(id),
#     FOREIGN KEY (brand_id) REFERENCES t_brand(id),
#     FOREIGN KEY (specification_id) REFERENCES t_specification(id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';


class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    category_id = models.IntegerField()
    unit_id = models.IntegerField()
    brand_id = models.IntegerField()
    specification_id = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=200, null=True)
    remark = models.TextField(null=True)
    status = models.IntegerField(default=1)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user_id = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 't_product'
        verbose_name = '商品'
        verbose_name_plural = '商品'


# CREATE TABLE t_supplier (
#     id INT PRIMARY KEY AUTO_INCREMENT COMMENT '供应商ID',
#     supplier_code VARCHAR(50) NOT NULL UNIQUE COMMENT '供应商编码',
#     supplier_name VARCHAR(100) NOT NULL COMMENT '供应商名称',
#     contact_person VARCHAR(50) COMMENT '联系人',
#     contact_phone VARCHAR(20) COMMENT '联系电话',
#     address VARCHAR(200) COMMENT '地址',
#     remark VARCHAR(500) COMMENT '备注',
#     status INT DEFAULT 0 COMMENT '状态：0-正常，1-禁用',
#     is_delete INT DEFAULT 0 COMMENT '删除标志：0-未删除，1-已删除',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供应商表';

class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, unique=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50, null=True)
    contact_phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    remark = models.TextField(null=True)
    status = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 't_supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'
       
