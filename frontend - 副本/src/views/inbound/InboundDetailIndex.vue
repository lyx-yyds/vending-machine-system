<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        入库明细 - {{ route.query.inbound_no }}
      </div>
      <div class="header-actions">
        <el-button round icon="Plus" type="primary" @click="createHandler">新增</el-button>
        <el-button round icon="Back" @click="goBack">返回</el-button>
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
        <el-table-column prop="specification" label="规格" width="100"></el-table-column>
        <el-table-column prop="unit_name" label="单位" width="80"></el-table-column>
        <el-table-column prop="quantity" label="入库数量" width="100"></el-table-column>
        <el-table-column prop="cost_price" label="成本单价" width="100"></el-table-column>
        <el-table-column prop="total_amount" label="小计金额" width="120"></el-table-column>
        <el-table-column prop="batch_no" label="批次号" width="150"></el-table-column>
        <el-table-column prop="production_date" label="生产日期" width="120">
          <template #default="{ row }">
            {{ row.production_date || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="expiry_date" label="有效期至" width="120">
          <template #default="{ row }">
            {{ row.expiry_date || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="warning" size="small" @click="editHandler(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteHandler(row)">删除</el-button>
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

    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="600">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="商品ID">
          <el-input-number v-model="formData.product_id" :min="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="商品名称">
          <el-input v-model="formData.product_name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="formData.specification" placeholder="请输入规格"></el-input>
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="formData.unit_name" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="入库数量">
          <el-input-number v-model="formData.quantity" :min="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="成本单价">
          <el-input-number v-model="formData.cost_price" :precision="2" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="小计金额">
          <el-input-number v-model="formData.total_amount" :precision="2" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="批次号">
          <el-input v-model="formData.batch_no" placeholder="请输入批次号"></el-input>
        </el-form-item>
        <el-form-item label="生产日期">
          <el-date-picker v-model="formData.production_date" type="date" placeholder="选择日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="有效期至">
          <el-date-picker v-model="formData.expiry_date" type="date" placeholder="选择日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" placeholder="请输入备注" type="textarea"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="addSubmitHandler">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getInboundDetailList, deleteInboundDetail, addInboundDetail, updateInboundDetail } from '@/api/inbound'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const dialogFormVisible = ref(false)
const dialogTitle = ref('新增明细')

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const formData = reactive({
  id: 0,
  inbound_id: 0,
  product_id: 0,
  product_name: '',
  specification: '',
  unit_id: null as number | null,
  unit_name: '',
  quantity: 1,
  cost_price: 0,
  total_amount: 0,
  batch_no: '',
  production_date: null as string | null,
  expiry_date: null as string | null,
  remark: ''
})

const listData = ref([])

const fetchDetailList = async () => {
  loading.value = true
  try {
    const inbound_id = route.query.inbound_id
    console.log('inbound_id:', inbound_id)
    const response = await getInboundDetailList({ pageNum: 1, pageSize: 10, inbound_id: inbound_id })
    console.log('API response:', response)
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
  router.push('/backend/inbound')
}

const deleteHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该明细吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await deleteInboundDetail(row.id)
    if (result.data.code === 2000) {
      ElMessage.success('删除成功')
      fetchDetailList()
    } else {
      ElMessage.error(result.data.message || '删除失败')
    }
  } catch {
  }
}

const createHandler = () => {
  dialogFormVisible.value = true
  dialogTitle.value = '新增明细'
  formData.id = 0
  formData.inbound_id = Number(route.query.inbound_id) || 0
  formData.product_id = 0
  formData.product_name = ''
  formData.specification = ''
  formData.unit_id = null
  formData.unit_name = ''
  formData.quantity = 1
  formData.cost_price = 0
  formData.total_amount = 0
  formData.batch_no = ''
  formData.production_date = null
  formData.expiry_date = null
  formData.remark = ''
}

const editHandler = (row: any) => {
  dialogFormVisible.value = true
  dialogTitle.value = '编辑明细'
  formData.id = row.id
  formData.inbound_id = row.inbound_id
  formData.product_id = row.product_id
  formData.product_name = row.product_name
  formData.specification = row.specification
  formData.unit_id = row.unit_id
  formData.unit_name = row.unit_name
  formData.quantity = row.quantity
  formData.cost_price = row.cost_price
  formData.total_amount = row.total_amount
  formData.batch_no = row.batch_no
  formData.production_date = row.production_date
  formData.expiry_date = row.expiry_date
  formData.remark = row.remark
}

const addSubmitHandler = async () => {
  if (!formData.product_id) {
    ElMessage.warning('请输入商品ID')
    return
  }

  try {
    if (dialogTitle.value === '新增明细') {
      const res = await addInboundDetail(formData)
      if (res.data.code === 2000) {
        ElMessage.success('新增成功')
        dialogFormVisible.value = false
        fetchDetailList()
      } else {
        ElMessage.error(res.data.message || '新增失败')
      }
    } else {
      const res = await updateInboundDetail(formData)
      if (res.data.code === 2000) {
        ElMessage.success('更新成功')
        dialogFormVisible.value = false
        fetchDetailList()
      } else {
        ElMessage.error(res.data.message || '更新失败')
      }
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
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
}

.header-actions {
  display: flex;
  gap: 10px;
}

.wrap-table {
  background: white;
  padding: 20px;
  border-radius: 8px;
}
</style>