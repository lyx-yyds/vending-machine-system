<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        退款记录管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.order_no" placeholder="请输入订单编号" style="width: 150px" clearable></el-input>
        <el-button round type="primary" icon="Search" @click="searchRefundList">搜索</el-button>
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
        <el-table-column prop="refund_no" label="退款单号" width="180">
          <template #default="{ row }">
            <el-tag type="danger">{{ row.refund_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_no" label="订单编号" width="180">
          <template #default="{ row }">
            <el-tag type="info">{{ row.order_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="refund_amount" label="退款金额" width="120">
          <template #default="{ row }">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ row.refund_amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="refund_type" label="退款类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.refund_type === 1 ? 'success' : 'warning'">
              {{ row.refund_type === 1 ? '原路退回' : '退到余额' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="refund_status" label="退款状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.refund_status === 0 ? 'info' : row.refund_status === 1 ? 'warning' : row.refund_status === 2 ? 'success' : row.refund_status === 3 ? 'danger' : 'info'">
              {{ row.refund_status === 0 ? '待处理' : row.refund_status === 1 ? '处理中' : row.refund_status === 2 ? '已完成' : row.refund_status === 3 ? '已拒绝' : '未知' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="refund_reason" label="退款原因" min-width="150"></el-table-column>
        <el-table-column prop="apply_time" label="申请时间" width="180">
          <template #default="{ row }">
            <el-tag type="info">{{ row.apply_time }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="process_time" label="处理时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.process_time || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.refund_status === 0" type="success" size="small" @click="handleApprove(row)">批准</el-button>
            <el-button v-if="row.refund_status === 0" type="danger" size="small" @click="handleReject(row)">拒绝</el-button>
            <span v-if="row.refund_status !== 0">{{ row.refund_status === 2 ? '已退款' : '已拒绝' }}</span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchRefundList"
        style="margin-top: 20px"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getRefundList, processRefund } from '@/api/payment'
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

const fetchRefundList = async () => {
  loading.value = true
  try {
    const response = await getRefundList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取退款记录列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchRefundList = () => {
  page.pageNum = 1
  fetchRefundList()
}

const resetSearchHandler = () => {
  searchForm.order_no = ''
  page.pageNum = 1
  fetchRefundList()
}

const handleApprove = async (row: any) => {
  try {
    const admin_id = sessionStorage.getItem('user_id')
    const response = await processRefund({
      refund_id: row.id,
      action: 'approve',
      admin_id: admin_id
    })
    if (response.data.code === 2000) {
      ElMessage.success('退款已批准')
      fetchRefundList()
    } else {
      ElMessage.error(response.data.message || '操作失败')
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleReject = async (row: any) => {
  try {
    const admin_id = sessionStorage.getItem('user_id')
    const response = await processRefund({
      refund_id: row.id,
      action: 'reject',
      admin_id: admin_id,
      process_result: '退款申请被拒绝'
    })
    if (response.data.code === 2000) {
      ElMessage.success('已拒绝退款申请')
      fetchRefundList()
    } else {
      ElMessage.error(response.data.message || '操作失败')
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchRefundList()
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
