# 售货机管理系统 (Vending Machine Management System)

基于 Vue 3 + Django REST Framework 的售货机后台管理系统，支持商品管理、库存管理、订单管理、支付管理等功能。

## 技术栈

### 前端
- Vue 3 + TypeScript
- Element Plus UI 组件库
- Vue Router 路由管理
- Axios HTTP 请求
- Vite 构建工具

### 后端
- Python 3.13
- Django 6.0
- Django REST Framework
- MySQL 数据库
- JWT 认证

## 功能模块

| 模块 | 功能 |
|-----|------|
| 商品管理 | 商品分类、商品信息、商品单位、商品规格 |
| 库存管理 | 商品入库、入库记录、库存查询、库存预警 |
| 订单管理 | 订单列表、订单详情、订单状态管理 |
| 支付管理 | 支付记录、退款处理 |
| 用户管理 | 用户列表、角色管理、个人资料 |
| 商城购物 | 商品浏览、购物车、下单支付 |

## 项目结构

```
my_project/
├── backend/                 # Django 后端
│   ├── backend/            # 项目配置
│   ├── user/               # 用户模块
│   ├── product/            # 商品模块
│   ├── inbound/            # 入库模块
│   ├── order/              # 订单模块
│   ├── payment/            # 支付模块
│   ├── stock/              # 库存模块
│   └── ...
├── frontend/               # Vue 前端
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 公共组件
│   │   ├── router/        # 路由配置
│   │   └── ...
│   └── package.json
└── README.md
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 访问地址

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000

## 默认账号

| 角色 | 用户名 | 密码 |
|-----|-------|------|
| 管理员 | admin | admin123 |
| 普通用户 | user | user123 |

## 权限说明

- **管理员**：拥有所有功能权限
- **普通用户**：商城购物、个人订单、个人资料

## 主要特性

- 完整的商品管理流程（分类 → 商品 → 入库 → 库存）
- 支持图片上传功能
- 订单支付与退款流程
- 库存自动更新与预警
- 响应式布局设计
- JWT 身份认证

## 开发团队

- 开发者：lyx-yyds
- 创建时间：2026年

## 许可证

MIT License