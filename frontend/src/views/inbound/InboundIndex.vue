<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        商品入库
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.inbound_no" placeholder="请输入入库单号" style="width: 180px" clearable></el-input>
        <el-button round icon="Plus" type="primary" @click="createHandler">新增</el-button>
        <el-button round type="primary" icon="Search" @click="searchInboundList">搜索</el-button>
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
        <el-table-column prop="inbound_no" label="入库单号" width="220">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.inbound_no }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="inbound_type" label="入库类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getInboundTypeTag(row.inbound_type)">
              {{ getInboundTypeName(row.inbound_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_quantity" label="总数量" width="100"></el-table-column>
        <el-table-column prop="total_amount" label="总金额" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="inbound_time" label="入库时间" width="180">
          <template #default="{ row }">
            {{ row.inbound_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="明细" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ row.details?.length || 0 }} 条</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetails(row)">明细</el-button>
            <el-button v-if="row.status === 0" type="success" size="small" @click="confirmHandler(row)">确认入库</el-button>
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
        @current-change="fetchInboundList"
        style="margin-top: 20px"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="1200px" @closed="resetDetails">
      <el-form :model="formData" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入库类型">
              <el-select v-model="formData.inbound_type" placeholder="请选择入库类型" style="width: 100%">
                <el-option label="采购入库" :value="1"></el-option>
                <el-option label="退货入库" :value="2"></el-option>
                <el-option label="调拨入库" :value="3"></el-option>
                <el-option label="补货入库" :value="4"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="仓库ID">
              <el-input-number v-model="formData.warehouse_id" :min="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="总数量">
              <el-input-number v-model="formData.total_quantity" :min="0" style="width: 100%" disabled></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总金额">
              <el-input-number v-model="formData.total_amount" :precision="2" :min="0" style="width: 100%" disabled></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="formData.status" style="width: 100%">
                <el-option label="待审核" :value="0"></el-option>
                <el-option label="已入库" :value="1"></el-option>
                <el-option label="已取消" :value="2"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注">
              <el-input v-model="formData.remark" placeholder="请输入备注"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <div class="detail-section">
        <div class="detail-header">
          <span>入库明细</span>
          <el-button v-if="dialogTitle === '新增入库'" type="primary" size="small" @click="addDetail">添加商品</el-button>
        </div>
        <el-table :data="details" border size="small">
          <el-table-column label="商品ID" prop="product_id" width="100">
            <template #default="{ row, $index }">
              <el-input-number v-if="dialogTitle === '新增入库'" v-model="row.product_id" :min="1" size="small" controls-position="right" @change="calcTotals" style="width: 90px"></el-input-number>
              <span v-else>{{ row.product_id }}</span>
            </template>
          </el-table-column>
          <el-table-column label="商品名称" prop="product_name" min-width="140">
            <template #default="{ row, $index }">
              <el-input v-if="dialogTitle === '新增入库'" v-model="row.product_name" placeholder="商品名称" size="small"></el-input>
              <span v-else>{{ row.product_name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="规格" prop="specification" min-width="120">
            <template #default="{ row }">
              <el-select v-if="dialogTitle === '新增入库'" v-model="row.specification" placeholder="请选择规格" size="small" style="width: 100%">
                <el-option v-for="spec in specificationList" :key="spec.id" :label="spec.spec_name" :value="spec.spec_name"></el-option>
              </el-select>
              <span v-else>{{ row.specification_display || row.specification || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="单位" prop="unit_name" width="100">
            <template #default="{ row }">
              <el-select v-if="dialogTitle === '新增入库'" v-model="row.unit_id" placeholder="请选择单位" size="small" style="width: 100%">
                <el-option v-for="unit in unitList" :key="unit.id" :label="unit.unit_name" :value="unit.id"></el-option>
              </el-select>
              <span v-else>{{ row.unit_name_display || row.unit_name || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="批次号" prop="batch_no" min-width="130">
            <template #default="{ row }">
              <el-input v-if="dialogTitle === '新增入库'" v-model="row.batch_no" placeholder="批次号" size="small"></el-input>
              <span v-else>{{ row.batch_no || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="生产日期" prop="production_date" width="140">
            <template #default="{ row }">
              <el-date-picker v-if="dialogTitle === '新增入库'" v-model="row.production_date" type="date" placeholder="生产日期" size="small" style="width: 130px"></el-date-picker>
              <span v-else>{{ row.production_date || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="有效期至" prop="expiry_date" width="140">
            <template #default="{ row }">
              <el-date-picker v-if="dialogTitle === '新增入库'" v-model="row.expiry_date" type="date" placeholder="有效期至" size="small" style="width: 130px"></el-date-picker>
              <span v-else>{{ row.expiry_date || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="数量" prop="quantity" width="110">
            <template #default="{ row }">
              <el-input-number v-if="dialogTitle === '新增入库'" v-model="row.quantity" :min="1" size="small" controls-position="right" @change="calcTotals" style="width: 100px"></el-input-number>
              <span v-else>{{ row.quantity }}</span>
            </template>
          </el-table-column>
          <el-table-column label="成本单价" prop="cost_price" width="130">
            <template #default="{ row }">
              <el-input-number v-if="dialogTitle === '新增入库'" v-model="row.cost_price" :precision="2" :min="0" size="small" controls-position="right" @change="calcTotals" style="width: 120px"></el-input-number>
              <span v-else>{{ row.cost_price }}</span>
            </template>
          </el-table-column>
          <el-table-column label="小计" prop="total_amount" width="120">
            <template #default="{ row }">
              {{ ((row.quantity || 0) * (row.cost_price || 0)).toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="remark" min-width="150">
            <template #default="{ row }">
              <el-input v-if="dialogTitle === '新增入库'" v-model="row.remark" placeholder="备注" size="small"></el-input>
              <span v-else>{{ row.remark || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column v-if="dialogTitle === '新增入库'" label="操作" width="80" fixed="right">
            <template #default="{ $index }">
              <el-button type="danger" size="small" @click="removeDetail($index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

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
import { useRouter } from 'vue-router'
import { getInboundRecordList, deleteInboundRecord, addInboundRecord, updateInboundRecord, confirmInboundRecord } from '@/api/inbound'
import { getUnitSimple } from '@/api/unit'
import { getSpecificationSimple } from '@/api/specification'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const dialogFormVisible = ref(false)
const dialogTitle = ref('新增入库')

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  inbound_no: ''
})

const formData = reactive({
  id: 0,
  inbound_no: '',
  inbound_type: 1,
  supplier_id: null as number | null,
  machine_id: null as number | null,
  warehouse_id: 1,
  total_quantity: 0,
  total_amount: 0,
  status: 0,
  inbound_time: null as string | null,
  operator_id: null as number | null,
  approver_id: null as number | null,
  remark: ''
})

interface DetailItem {
  id: number
  product_id: number
  product_name: string
  specification: string
  unit_id: number | null
  unit_name: string
  quantity: number
  cost_price: number
  total_amount: number
  batch_no: string
  production_date: string | null
  expiry_date: string | null
  remark: string
}

const details = ref<DetailItem[]>([])
const unitList = ref<{id: number, unit_code: string, unit_name: string}[]>([])
const specificationList = ref<{id: number, spec_code: string, spec_name: string}[]>([])

const listData = ref([])

const getInboundTypeName = (type: number) => {
  const map: Record<number, string> = { 1: '采购入库', 2: '退货入库', 3: '调拨入库', 4: '补货入库' }
  return map[type] || type
}

const getInboundTypeTag = (type: number) => {
  const map: Record<number, string> = { 1: 'success', 2: 'warning', 3: 'info', 4: 'primary' }
  return map[type] || 'info'
}

const getStatusName = (status: number) => {
  const map: Record<number, string> = { 0: '待审核', 1: '已入库', 2: '已取消' }
  return map[status] || status
}

const getStatusTag = (status: number) => {
  const map: Record<number, string> = { 0: 'warning', 1: 'success', 2: 'info' }
  return map[status] || 'info'
}

const calcTotals = () => {
  let totalQty = 0
  let totalAmt = 0
  details.value.forEach(d => {
    totalQty += d.quantity || 0
    totalAmt += (d.quantity || 0) * (d.cost_price || 0)
  })
  formData.total_quantity = totalQty
  formData.total_amount = totalAmt
}

const addDetail = () => {
  details.value.push({
    id: 0,
    product_id: 0,
    product_name: '',
    specification: '',
    unit_id: null,
    unit_name: '',
    quantity: 1,
    cost_price: 0,
    total_amount: 0,
    batch_no: '',
    production_date: null,
    expiry_date: null,
    remark: ''
  })
}

const removeDetail = (index: number) => {
  details.value.splice(index, 1)
  calcTotals()
}

const resetDetails = () => {
  details.value = []
}

const fetchInboundList = async () => {
  loading.value = true
  try {
    const response = await getInboundRecordList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取入库列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchInboundList = () => {
  page.pageNum = 1
  fetchInboundList()
}

const resetSearchHandler = () => {
  searchForm.inbound_no = ''
  page.pageNum = 1
  fetchInboundList()
}

const viewDetails = (row: any) => {
  console.log('viewDetails called, row:', row)
  router.push({ path: '/backend/inbound-detail', query: { inbound_id: row.id, inbound_no: row.inbound_no } })
}

const confirmHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要确认入库吗？确认后将更新库存。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await confirmInboundRecord({ inbound_id: row.id })
    if (result.data.code === 2000) {
      ElMessage.success('入库确认成功，库存已更新')
      fetchInboundList()
    } else {
      ElMessage.error(result.data.message || '操作失败')
    }
  } catch {
  }
}

const deleteHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该入库记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await deleteInboundRecord(row.id)
    if (result.data.code === 2000) {
      ElMessage.success('删除成功')
      fetchInboundList()
    } else {
      ElMessage.error(result.data.message || '删除失败')
    }
  } catch {
  }
}

const createHandler = () => {
  dialogFormVisible.value = true
  dialogTitle.value = '新增入库'
  formData.id = 0
  formData.inbound_no = ''
  formData.inbound_type = 1
  formData.supplier_id = null
  formData.machine_id = null
  formData.warehouse_id = 1
  formData.total_quantity = 0
  formData.total_amount = 0
  formData.status = 0
  formData.inbound_time = null
  formData.operator_id = null
  formData.approver_id = null
  formData.remark = ''
  details.value = []
}

const editHandler = (row: any) => {
  dialogFormVisible.value = true
  dialogTitle.value = '编辑入库'
  formData.id = row.id
  formData.inbound_no = row.inbound_no
  formData.inbound_type = row.inbound_type
  formData.supplier_id = row.supplier_id
  formData.machine_id = row.machine_id
  formData.warehouse_id = row.warehouse_id
  formData.total_quantity = row.total_quantity
  formData.total_amount = row.total_amount
  formData.status = row.status
  formData.inbound_time = row.inbound_time
  formData.operator_id = row.operator_id
  formData.approver_id = row.approver_id
  formData.remark = row.remark
  details.value = row.details?.map((d: any) => ({
    id: d.id || 0,
    product_id: d.product_id || 0,
    product_name: d.product_name || '',
    specification: d.specification || '',
    unit_id: d.unit_id || null,
    unit_name: d.unit_name || '',
    quantity: d.quantity || 1,
    cost_price: d.cost_price || 0,
    total_amount: d.total_amount || 0,
    batch_no: d.batch_no || '',
    production_date: d.production_date || null,
    expiry_date: d.expiry_date || null,
    remark: d.remark || ''
  })) || []
}

const addSubmitHandler = async () => {
  if (details.value.length === 0) {
    ElMessage.warning('请添加至少一条入库明细')
    return
  }

  calcTotals()

  const formatDetails = details.value.map((d: any) => ({
    ...d,
    production_date: d.production_date instanceof Date ? d.production_date.toISOString().split('T')[0] : d.production_date,
    expiry_date: d.expiry_date instanceof Date ? d.expiry_date.toISOString().split('T')[0] : d.expiry_date
  }))

  try {
    const submitData = {
      ...formData,
      details: formatDetails
    }
    if (dialogTitle.value === '新增入库') {
      const res = await addInboundRecord(submitData)
      if (res.data.code === 2000) {
        ElMessage.success('新增成功')
        dialogFormVisible.value = false
        fetchInboundList()
      } else {
        ElMessage.error(res.data.message || '新增失败')
      }
    } else {
      const res = await updateInboundRecord(submitData)
      if (res.data.code === 2000) {
        ElMessage.success('更新成功')
        dialogFormVisible.value = false
        fetchInboundList()
      } else {
        ElMessage.error(res.data.message || '更新失败')
      }
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

onMounted(async () => {
  fetchInboundList()
  await fetchSelectData()
})

const fetchSelectData = async () => {
  try {
    const [unitRes, specRes] = await Promise.all([
      getUnitSimple(),
      getSpecificationSimple()
    ])
    if (unitRes.data.code === 2000) {
      unitList.value = unitRes.data.data
    }
    if (specRes.data.code === 2000) {
      specificationList.value = specRes.data.data
    }
  } catch (error) {
    console.error('获取下拉数据失败:', error)
  }
}
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
  flex-wrap: wrap;
}

.wrap-table {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.detail-section {
  margin-top: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-weight: bold;
}
</style>