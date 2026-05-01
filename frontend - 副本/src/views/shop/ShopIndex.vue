<template>
  <div class="shop-container">
    <div class="shop-header">
      <h2>商品浏览</h2>
      <div class="cart-info" @click="showCart = true">
        <el-badge :value="cartCount" :hidden="cartCount === 0">
          <el-button icon="ShoppingCart">购物车</el-button>
        </el-badge>
      </div>
    </div>

    <div class="category-tabs">
      <el-radio-group v-model="selectedCategory" size="large">
        <el-radio-button :value="0">全部</el-radio-button>
        <el-radio-button v-for="cat in categoryList" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <div class="product-grid">
      <div v-for="product in filteredProducts" :key="product.id" class="product-card">
        <div class="product-image">
          <img v-if="product.image" :src="product.image" :alt="product.name">
          <div v-else class="no-image">暂无图片</div>
        </div>
        <div class="product-info">
          <h4>{{ product.name }}</h4>
          <p class="product-spec">{{ product.spec_name || '默认规格' }}</p>
          <p class="product-price">¥{{ product.price }}</p>
          <div class="product-stock" v-if="product.stock > 0">库存: {{ product.stock }}</div>
          <div class="product-stock out-of-stock" v-else>缺货</div>
          <div class="product-actions">
            <el-input-number v-if="product.stock > 0" v-model="product.quantity" :min="1" :max="product.stock" size="small"/>
            <el-button
              v-if="product.stock > 0"
              type="primary"
              size="small"
              @click="addToCart(product)"
              :disabled="product.quantity <= 0"
            >加入购物车</el-button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredProducts.length === 0 && !loading" class="empty-tip">
      暂无商品
    </div>

    <el-drawer v-model="showCart" title="购物车" size="400px" direction="rtl">
      <div class="cart-items" v-if="cartItems.length > 0">
        <div v-for="(item, index) in cartItems" :key="index" class="cart-item">
          <div class="cart-item-info">
            <span class="cart-item-name">{{ item.name }}</span>
            <span class="cart-item-price">¥{{ item.price }}</span>
          </div>
          <div class="cart-item-actions">
            <el-input-number v-model="item.quantity" :min="1" :max="item.stock" size="small" @change="updateCartItem(item)"/>
            <el-button type="danger" size="small" @click="removeFromCart(index)">删除</el-button>
          </div>
        </div>
      </div>
      <div v-else class="cart-empty">
        购物车是空的
      </div>
      <div class="cart-footer" v-if="cartItems.length > 0">
        <div class="cart-total">
          <span>总计: </span>
          <span class="total-price">¥{{ cartTotal }}</span>
        </div>
        <el-button type="primary" size="large" @click="handleCheckout" :loading="placing">提交订单</el-button>
      </div>
    </el-drawer>

    <el-dialog v-model="showOrderSuccess" title="下单成功" width="400px" :close-on-click-modal="false">
      <div class="order-success-content">
        <el-icon class="success-icon" color="#67c23a" :size="60"><CircleCheckFilled /></el-icon>
        <p>您的取餐码是: <span class="pickup-code">{{ orderResult.pickup_code }}</span></p>
        <p>订单编号: {{ orderResult.order_no }}</p>
        <p>订单金额: ¥{{ orderResult.total_amount }}</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="goToMyOrders">查看我的订单</el-button>
        <el-button @click="continueShopping">继续购物</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProductList } from '@/api/product'
import { getCategoryList } from '@/api/product'
import { createOrder } from '@/api/order'
import { ElMessage } from 'element-plus'
import { CircleCheckFilled } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const selectedCategory = ref(0)
const categoryList = ref<any[]>([])
const productList = ref<any[]>([])
const showCart = ref(false)
const showOrderSuccess = ref(false)
const placing = ref(false)

interface CartItem {
  product_id: number
  name: string
  price: number
  quantity: number
  stock: number
  image: string
}

const cartItems = ref<CartItem[]>([])

const filteredProducts = computed(() => {
  if (selectedCategory.value === 0) {
    return productList.value
  }
  return productList.value.filter(p => p.category_id === selectedCategory.value)
})

const cartCount = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

const cartTotal = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2)
})

const orderResult = ref({
  order_no: '',
  pickup_code: '',
  total_amount: 0
})

const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await getProductList({ pageNum: 1, pageSize: 100 })
    if (response.data.code === 2000) {
      productList.value = response.data.data.list.map((p: any) => ({
        id: p.id,
        name: p.product_name,
        price: p.selling_price || p.price,
        image: p.image_url || p.image,
        category_id: p.category_id,
        category_name: p.category_name,
        stock: p.stock || 99,
        quantity: 1
      }))
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await getCategoryList({ pageNum: 1, pageSize: 100 })
    if (response.data.code === 2000) {
      categoryList.value = response.data.data.list
    }
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const addToCart = (product: any) => {
  const existingItem = cartItems.value.find(item => item.product_id === product.id)
  if (existingItem) {
    if (existingItem.quantity < product.stock) {
      existingItem.quantity++
    } else {
      ElMessage.warning('库存不足')
    }
  } else {
    cartItems.value.push({
      product_id: product.id,
      name: product.name,
      price: parseFloat(product.price) || 0,
      quantity: product.quantity || 1,
      stock: product.stock,
      image: product.image || ''
    })
  }
  ElMessage.success('已加入购物车')
}

const updateCartItem = (item: CartItem) => {
}

const removeFromCart = (index: number) => {
  cartItems.value.splice(index, 1)
}

const handleCheckout = async () => {
  if (cartItems.value.length === 0) {
    ElMessage.warning('购物车是空的')
    return
  }

  const user_id = sessionStorage.getItem('user_id')
  if (!user_id) {
    ElMessage.error('请先登录')
    router.push('/login')
    return
  }

  placing.value = true
  try {
    const items = cartItems.value.map(item => ({
      product_id: item.product_id,
      quantity: item.quantity
    }))

    const response = await createOrder({
      user_id,
      machine_id: 1,
      items
    })

    if (response.data.code === 2000) {
      orderResult.value = response.data.data
      showCart.value = false
      showOrderSuccess.value = true
      cartItems.value = []
    } else {
      ElMessage.error(response.data.message || '下单失败')
    }
  } catch (error: any) {
    console.error('下单失败:', error)
    ElMessage.error(error.response?.data?.message || '下单失败')
  } finally {
    placing.value = false
  }
}

const goToMyOrders = () => {
  showOrderSuccess.value = false
  router.push('/backend/my-order')
}

const continueShopping = () => {
  showOrderSuccess.value = false
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
})
</script>

<style scoped>
.shop-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background: #f5f5f5;
}

.shop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.shop-header h2 {
  margin: 0;
  color: #333;
}

.cart-info {
  cursor: pointer;
}

.category-tabs {
  margin-bottom: 20px;
  background: #fff;
  padding: 15px;
  border-radius: 8px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  height: 160px;
  overflow: hidden;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #999;
  font-size: 14px;
}

.product-info {
  padding: 15px;
}

.product-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-spec {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #999;
}

.product-price {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #f56c6c;
  font-weight: bold;
}

.product-stock {
  font-size: 12px;
  color: #67c23a;
  margin-bottom: 10px;
}

.product-stock.out-of-stock {
  color: #f56c6c;
}

.product-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.product-actions .el-input-number {
  width: 100px;
}

.empty-tip {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 16px;
}

.cart-items {
  padding: 0 10px;
}

.cart-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.cart-item-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.cart-item-name {
  font-weight: bold;
}

.cart-item-price {
  color: #f56c6c;
}

.cart-item-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart-empty {
  text-align: center;
  padding: 60px 0;
  color: #999;
}

.cart-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  border-top: 1px solid #eee;
  background: #fff;
}

.cart-total {
  margin-bottom: 15px;
  font-size: 16px;
}

.total-price {
  font-size: 24px;
  color: #f56c6c;
  font-weight: bold;
}

.order-success-content {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  margin-bottom: 20px;
}

.pickup-code {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}
</style>
