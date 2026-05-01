<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        订单明细 - {{ route.query.order_no }}
      </div>
      <el-button round type="primary" icon="Back" @click="goBack">返回</el-button>
    </div>
    <div class="wrap-table">
      <el-table :data="listData" v-loading="loading">
        <el-table-column label="序号" width="60">
          <template #default="{ $index }">
            {{ $index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="商品名称" width="150"></el-table-column>
        <el-table-column prop="product_image" label="商品图片" width="120">
          <template #default="{ row }">
            <el-image v-if="row.product_image" :src="row.product_image" style="width: 60px; height: 60px;" fit="cover"></el-image>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="购买数量" width="100"></el-table-column>
        <el-table-column prop="unit_price" label="单价" width="100">
          <template #default="{ row }">
            <span style="color: #ff6b00;">¥{{ row.unit_price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="total_price" label="小计金额" width="120">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">¥{{ row.total_price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="cost_price" label="成本单价" width="100">
          <template #default="{ row }">
            <span>¥{{ row.cost_price || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="aisle_id" label="货道ID" width="80"></el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.create_time }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchDetailList"
        style="margin-top: 20px"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getOrderDetailList } from '@/api/order'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loading = ref(false)

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const listData = ref([])

const fetchDetailList = async () => {
  loading.value = true
  try {
    const order_id = route.query.order_id
    const response = await getOrderDetailList({ pageNum: 1, pageSize: 10, order_id: order_id })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取明细列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchDetailList()
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

.wrap-table {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}
</style>
