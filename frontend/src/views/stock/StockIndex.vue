<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        库存管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.product_name" placeholder="请输入商品名称" style="width: 150px" clearable></el-input>
        <el-input v-model="searchForm.product_code" placeholder="请输入商品编码" style="width: 150px" clearable></el-input>
        <el-button round type="primary" icon="Search" @click="searchStockList">搜索</el-button>
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
        <el-table-column prop="product_name" label="商品名称" width="150"></el-table-column>
        <el-table-column prop="product_code" label="商品编码" width="120">
          <template #default="{ row }">
            <el-tag type="info">{{ row.product_code }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warehouse_stock" label="仓库库存" width="100">
          <template #default="{ row }">
            <span style="color: #409eff; font-weight: bold;">{{ row.warehouse_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="machine_stock" label="机器库存" width="100">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">{{ row.machine_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="total_stock" label="总库存" width="100">
          <template #default="{ row }">
            <span style="color: #f56c6c; font-weight: bold; font-size: 16px;">{{ row.total_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="min_stock" label="预警值" width="80"></el-table-column>
        <el-table-column prop="cost_price" label="成本价" width="100">
          <template #default="{ row }">
            <span>¥{{ row.cost_price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="last_inbound_date" label="最后入库时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.last_inbound_date || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_outbound_date" label="最后出库时间" width="180">
          <template #default="{ row }">
            <el-tag type="warning">{{ row.last_outbound_date || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="120"></el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchStockList"
        style="margin-top: 20px"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getStockList } from '@/api/stock'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  product_name: '',
  product_code: ''
})

const listData = ref([])

const fetchStockList = async () => {
  loading.value = true
  try {
    const response = await getStockList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取库存列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchStockList = () => {
  page.pageNum = 1
  fetchStockList()
}

const resetSearchHandler = () => {
  searchForm.product_name = ''
  searchForm.product_code = ''
  page.pageNum = 1
  fetchStockList()
}

onMounted(() => {
  fetchStockList()
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
