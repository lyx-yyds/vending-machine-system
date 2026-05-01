import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      // 注册页面
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/backend',
      name: 'backend',
      component: () => import('../layout/Layout.vue'),
      redirect: '/backend/home',
      children: [
        {
          // 首页
          path: 'home',
          name: 'home',
          component: () => import('../views/HomeView.vue')
        },
        {
          // 商品管理
          path: 'product-category',
          name: 'product-category',
          component: () => import('../views/ProductCategory/ProductCategoryView.vue')
        },
        {
          // 商品信息
          path: 'product-info',
          name: 'product-info',
          component: () => import('../views/Product/ProductInfo.vue')
        },
        {
          // 供应商管理
          path: 'supplier',
          name: 'supplier',
          component: () => import('../views/Product/SupplierIndex.vue')
        },
        {
          // 商品单位
          path: 'unit',
          name: 'unit',
          component: () => import('../views/Product/ProductUnitIndex.vue')
        },
        {
                // 商品规格
          path: 'specifications',
          name: 'specifications',
          component: () => import('../views/specifications/SpecificationIndex.vue')
        },
        {
          // 商品入库
          path: 'inbound',
          name: 'inbound',
          component: () => import('../views/inbound/InboundIndex.vue')
        },
        {
          // 入库明细
          path: 'inbound-detail',
          name: 'inbound-detail',
          component: () => import('../views/inbound/InboundDetailIndex.vue')
        },
        {
          // 订单管理
          path: 'order',
          name: 'order',
          component: () => import('../views/order/OrderIndex.vue')
        },
        {
          // 订单详情
          path: 'order-detail',
          name: 'order-detail',
          component: () => import('../views/order/OrderDetailIndex.vue')
        },
        {
          // 支付管理
          path: 'payment',
          name: 'payment',
          component: () => import('../views/payment/PaymentIndex.vue')
        },
        {
          // 退款管理
          path: 'refund',
          name: 'refund',
          component: () => import('../views/payment/RefundIndex.vue')
        },
        {
          // 库存管理
          path: 'stock',
          name: 'stock',
          component: () => import('../views/stock/StockIndex.vue')
        },
        {
          // 用户管理
          path: 'user',
          name: 'user',
          component: () => import('../views/user/UserIndex.vue')
        },
        {
          // 个人资料
          path: 'profile',
          name: 'profile',
          component: () => import('../views/user/ProfileIndex.vue')
        },
        {
          // 我的订单
          path: 'my-order',
          name: 'my-order',
          component: () => import('../views/order/MyOrderIndex.vue')
        },
        {
          // 商城购物
          path: 'shop',
          name: 'shop',
          component: () => import('../views/shop/ShopIndex.vue')
        },
      ]
    }
  ],
})

export default router