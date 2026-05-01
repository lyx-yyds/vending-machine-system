<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getDashboard } from '@/api/dashboard'
import { ElMessage } from 'element-plus'
import {
  ShoppingCart,
  Money,
  Goods,
  User,
  List,
  Warning,
  ArrowRight,
  Refresh
} from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const stats = ref({
  today_order_count: 0,
  today_revenue: 0,
  total_products: 0,
  total_users: 0,
  pending_orders: 0,
  low_stock_count: 0,
  recent_orders: [] as any[]
})

const fetchDashboard = async () => {
  loading.value = true
  try {
    const response = await getDashboard()
    if (response.data.code === 2000) {
      stats.value = response.data.data
    } else {
      ElMessage.error(response.data.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: number) => {
  switch (status) {
    case 0: return 'warning'
    case 1: return 'success'
    case 2: return 'primary'
    case 3: return 'info'
    default: return 'info'
  }
}

const getStatusText = (status: number) => {
  switch (status) {
    case 0: return '待处理'
    case 1: return '已完成'
    case 2: return '进行中'
    case 3: return '已取消'
    default: return '未知'
  }
}

const getPayStatusType = (status: number) => {
  switch (status) {
    case 0: return 'warning'
    case 1: return 'success'
    case 2: return 'danger'
    default: return 'info'
  }
}

const getPayStatusText = (status: number) => {
  switch (status) {
    case 0: return '未支付'
    case 1: return '已支付'
    case 2: return '已退款'
    default: return '未知'
  }
}

const goToOrder = () => {
  router.push('/backend/order')
}

const goToStock = () => {
  router.push('/backend/stock')
}

const goToProduct = () => {
  router.push('/backend/product-category')
}

const goToUser = () => {
  router.push('/backend/user')
}

const goToInbound = () => {
  router.push('/backend/inbound')
}

const goToPayment = () => {
  router.push('/backend/payment')
}

onMounted(() => {
  fetchDashboard()
})
</script>

<template>
  <div class="home-container" v-loading="loading">
    <div class="home-header">
      <div class="header-left">
        <h2>售货机管理系统</h2>
        <span class="subtitle">Vending Machine Management System</span>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" circle @click="fetchDashboard" title="刷新数据"></el-button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card" @click="goToOrder">
        <div class="stat-icon order-icon">
          <el-icon :size="32"><ShoppingCart /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.today_order_count }}</div>
          <div class="stat-label">今日订单</div>
        </div>
      </div>

      <div class="stat-card" @click="goToPayment">
        <div class="stat-icon revenue-icon">
          <el-icon :size="32"><Money /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">¥{{ stats.today_revenue.toFixed(2) }}</div>
          <div class="stat-label">今日收入</div>
        </div>
      </div>

      <div class="stat-card" @click="goToProduct">
        <div class="stat-icon product-icon">
          <el-icon :size="32"><Goods /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_products }}</div>
          <div class="stat-label">商品总数</div>
        </div>
      </div>

      <div class="stat-card" @click="goToUser">
        <div class="stat-icon user-icon">
          <el-icon :size="32"><User /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">用户总数</div>
        </div>
      </div>

      <div class="stat-card" @click="goToOrder">
        <div class="stat-icon pending-icon">
          <el-icon :size="32"><List /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pending_orders }}</div>
          <div class="stat-label">待处理订单</div>
        </div>
      </div>

      <div class="stat-card" @click="goToStock">
        <div class="stat-icon warning-icon">
          <el-icon :size="32"><Warning /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.low_stock_count }}</div>
          <div class="stat-label">库存预警</div>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <div class="panel recent-orders">
        <div class="panel-header">
          <h3>最新订单</h3>
          <el-button type="primary" link @click="goToOrder">
            查看更多 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
        </div>
        <div class="panel-body">
          <el-table :data="stats.recent_orders" style="width: 100%" :max-height="400">
            <el-table-column prop="order_no" label="订单编号" width="180">
              <template #default="{ row }">
                <el-tag type="primary">{{ row.order_no }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_amount" label="金额" width="100">
              <template #default="{ row }">
                <span style="color: #f56c6c; font-weight: bold;">¥{{ row.total_amount }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="pay_status" label="支付状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getPayStatusType(row.pay_status)">
                  {{ getPayStatusText(row.pay_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="order_status" label="订单状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.order_status)">
                  {{ getStatusText(row.order_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="下单时间" />
          </el-table>
        </div>
      </div>

      <div class="panel quick-actions">
        <div class="panel-header">
          <h3>快捷操作</h3>
        </div>
        <div class="panel-body">
          <div class="action-grid">
            <div class="action-item" @click="goToProduct">
              <div class="action-icon">
                <el-icon :size="28"><Goods /></el-icon>
              </div>
              <span>商品管理</span>
            </div>
            <div class="action-item" @click="goToInbound">
              <div class="action-icon">
                <el-icon :size="28"><List /></el-icon>
              </div>
              <span>商品入库</span>
            </div>
            <div class="action-item" @click="goToStock">
              <div class="action-icon">
                <el-icon :size="28"><Warning /></el-icon>
              </div>
              <span>库存管理</span>
            </div>
            <div class="action-item" @click="goToOrder">
              <div class="action-icon">
                <el-icon :size="28"><ShoppingCart /></el-icon>
              </div>
              <span>订单管理</span>
            </div>
            <div class="action-item" @click="goToPayment">
              <div class="action-icon">
                <el-icon :size="28"><Money /></el-icon>
              </div>
              <span>支付管理</span>
            </div>
            <div class="action-item" @click="goToUser">
              <div class="action-icon">
                <el-icon :size="28"><User /></el-icon>
              </div>
              <span>用户管理</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 84px);
}

.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left h2 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.header-left .subtitle {
  color: #909399;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.order-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.revenue-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.product-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.user-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.pending-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.warning-icon {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-top: 4px;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.panel-body {
  padding: 16px 20px;
}

.recent-orders {
  min-height: 400px;
}

.quick-actions .panel-body {
  padding: 20px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 12px;
  background: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background: #e4e7ed;
  transform: scale(1.02);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.action-item span {
  color: #606266;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>