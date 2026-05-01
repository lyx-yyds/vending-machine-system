<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        支付记录管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.order_no" placeholder="请输入订单编号" style="width: 150px" clearable></el-input>
        <el-button round type="primary" icon="Search" @click="searchPaymentList">搜索</el-button>
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
        <el-table-column prop="payment_no" label="支付流水号" width="180">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.payment_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_no" label="订单编号" width="180">
          <template #default="{ row }">
            <el-tag type="info">{{ row.order_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_type" label="支付方式" width="100">
          <template #default="{ row }">
            <el-tag :type="row.pay_type === 1 ? 'success' : row.pay_type === 2 ? 'primary' : row.pay_type === 3 ? 'warning' : 'info'">
              {{ row.pay_type === 1 ? '微信' : row.pay_type === 2 ? '支付宝' : row.pay_type === 3 ? '会员卡' : '现金' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_amount" label="支付金额" width="120">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">¥{{ row.pay_amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pay_status" label="支付状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.pay_status === 1 ? 'success' : row.pay_status === 0 ? 'warning' : row.pay_status === 2 ? 'danger' : 'info'">
              {{ row.pay_status === 0 ? '待支付' : row.pay_status === 1 ? '成功' : row.pay_status === 2 ? '失败' : row.pay_status === 3 ? '已撤销' : '未知' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pay_time" label="支付时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.pay_time || '-' }}</el-tag>
          </template>
        </el-table-column>
        <!-- <el-table-column prop="transaction_id" label="第三方交易流水号" width="180">
          <template #default="{ row }">
            <span>{{ row.transaction_id || '-' }}</span>
          </template>
        </el-table-column> -->
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            <el-tag type="info">{{ row.create_time }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchPaymentList"
        style="margin-top: 20px"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getPaymentList } from '@/api/payment'
import { ElMessage } from 'element-plus'

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

const fetchPaymentList = async () => {
  loading.value = true
  try {
    const response = await getPaymentList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取支付记录列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchPaymentList = () => {
  page.pageNum = 1
  fetchPaymentList()
}

const resetSearchHandler = () => {
  searchForm.order_no = ''
  page.pageNum = 1
  fetchPaymentList()
}

onMounted(() => {
  fetchPaymentList()
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
