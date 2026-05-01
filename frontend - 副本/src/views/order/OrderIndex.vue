<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        订单管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.order_no" placeholder="请输入订单编号" style="width: 150px" clearable></el-input>
        <el-button round type="primary" icon="Search" @click="searchOrderList">搜索</el-button>
        <el-button round type="danger" icon="Delete" @click="resetSearchHandler">重置</el-button>
      </div>
    </div>
    <div class="wrap-table">
      <el-table :data="listData" v-loading="loading">
        <el-table-column label="序号" width="60">
          <template #default="{ $index }">
            {{ $index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="order_no" label="订单编号" width="180">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.order_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_amount" label="订单总金额" width="120">
          <template #default="{ row }">
            <span style="color: #ff6b00; font-weight: bold;">¥{{ row.total_amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pay_amount" label="实付金额" width="120">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">¥{{ row.pay_amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="order_type" label="订单类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.order_type === 1 ? 'success' : row.order_type === 2 ? 'warning' : 'info'">
              {{ row.order_type === 1 ? '线上支付' : row.order_type === 2 ? '货到付款' : '扫码支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_type" label="支付方式" width="100">
          <template #default="{ row }">
            <el-tag :type="row.pay_type === 1 ? 'success' : row.pay_type === 2 ? 'primary' : row.pay_type === 3 ? 'warning' : 'info'">
              {{ row.pay_type === 1 ? '微信' : row.pay_type === 2 ? '支付宝' : row.pay_type === 3 ? '会员卡' : '现金' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_status" label="支付状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.pay_status === 1 ? 'success' : row.pay_status === 0 ? 'warning' : row.pay_status === 2 ? 'danger' : 'info'">
              {{ row.pay_status === 0 ? '待支付' : row.pay_status === 1 ? '已支付' : row.pay_status === 2 ? '已退款' : '未知' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_status" label="订单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.order_status === 0 ? 'info' : row.order_status === 1 ? 'primary' : row.order_status === 2 ? 'success' : row.order_status === 3 ? 'warning' : 'danger'">
              {{ row.order_status === 0 ? '待处理' : row.order_status === 1 ? '进行中' : row.order_status === 2 ? '已完成' : row.order_status === 3 ? '已取消' : '退款中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pickup_code" label="取餐码" width="100">
          <template #default="{ row }">
            <span style="font-size: 18px; font-weight: bold; color: #409eff;">{{ row.pickup_code }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.create_time }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetails(row)">明细</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchOrderList"
        style="margin-top: 20px"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getOrderList } from '@/api/order'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  order_no: ''
})

const listData = ref([])

const fetchOrderList = async () => {
  loading.value = true
  try {
    const response = await getOrderList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchOrderList = () => {
  page.pageNum = 1
  fetchOrderList()
}

const resetSearchHandler = () => {
  searchForm.order_no = ''
  page.pageNum = 1
  fetchOrderList()
}

const viewDetails = (row: any) => {
  router.push({ path: '/backend/order-detail', query: { order_id: row.id, order_no: row.order_no } })
}

onMounted(() => {
  fetchOrderList()
})
</script>

<style scoped>
.wrap-container {
  padding: 20px;
}

.wrap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.wrap-table {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}
</style>
