<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        供应商管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.supplier_name" placeholder="请输入供应商名称" style="width: 150px" clearable></el-input>
        <el-button round icon="Plus" type="primary" @click="createHandler">新增</el-button>
        <el-button round type="primary" icon="Search" @click="searchSupplierList">搜索</el-button>
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
        <el-table-column prop="supplier_code" label="供应商编码" width="200">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.supplier_code }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="supplier_name" label="供应商名称" width="150"></el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="120"></el-table-column>
        <el-table-column prop="contact_phone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'danger'">
              {{ row.status === 0 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            <el-tag type="success">{{ row.create_time }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editHandler(row)">编辑</el-button>
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
        @current-change="fetchSupplierList"
        style="margin-top: 20px"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="600">
      <el-form :model="formData" label-width="100px">
        <el-form-item v-show="dialogTitle === '编辑供应商'" label="供应商编码">
          <el-input disabled v-model="formData.supplier_code"></el-input>
        </el-form-item>
        <el-form-item label="供应商名称">
          <el-input v-model="formData.supplier_name" placeholder="请输入供应商名称"></el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="formData.contact_person" placeholder="请输入联系人"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="formData.contact_phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="formData.address" placeholder="请输入地址"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" placeholder="请输入备注" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="formData.status" :active-value="0" :inactive-value="1"></el-switch>
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
import { getSupplierList, deleteSupplier, addSupplier, updateSupplier } from '@/api/product'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const dialogFormVisible = ref(false)
const dialogTitle = ref('新增供应商')

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  supplier_name: ''
})

const formData = reactive({
  id: 0,
  supplier_code: '',
  supplier_name: '',
  contact_person: '',
  contact_phone: '',
  address: '',
  remark: '',
  status: 0
})

const listData = ref([])

const fetchSupplierList = async () => {
  loading.value = true
  try {
    const response = await getSupplierList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取供应商列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchSupplierList = () => {
  page.pageNum = 1
  fetchSupplierList()
}

const resetSearchHandler = () => {
  searchForm.supplier_name = ''
  page.pageNum = 1
  fetchSupplierList()
}

const deleteHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该供应商吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await deleteSupplier(row.id)
    if (result.data.code === 2000) {
      ElMessage.success('删除成功')
      fetchSupplierList()
    } else {
      ElMessage.error(result.data.message || '删除失败')
    }
  } catch {
  }
}

const createHandler = () => {
  dialogFormVisible.value = true
  dialogTitle.value = '新增供应商'
  formData.id = 0
  formData.supplier_code = ''
  formData.supplier_name = ''
  formData.contact_person = ''
  formData.contact_phone = ''
  formData.address = ''
  formData.remark = ''
  formData.status = 0
}

const editHandler = (row: any) => {
  dialogFormVisible.value = true
  dialogTitle.value = '编辑供应商'
  formData.id = row.id
  formData.supplier_code = row.supplier_code
  formData.supplier_name = row.supplier_name
  formData.contact_person = row.contact_person
  formData.contact_phone = row.contact_phone
  formData.address = row.address
  formData.remark = row.remark
  formData.status = row.status
}

const addSubmitHandler = async () => {
  if (!formData.supplier_name) {
    ElMessage.warning('请输入供应商名称')
    return
  }

  try {
    if (dialogTitle.value === '新增供应商') {
      const res = await addSupplier(formData)
      if (res.data.code === 2000) {
        ElMessage.success('新增成功')
        dialogFormVisible.value = false
        fetchSupplierList()
      } else {
        ElMessage.error(res.data.message || '新增失败')
      }
    } else {
      const res = await updateSupplier(formData)
      if (res.data.code === 2000) {
        ElMessage.success('更新成功')
        dialogFormVisible.value = false
        fetchSupplierList()
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
  fetchSupplierList()
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
  flex-wrap: wrap;
}

.wrap-table {
  background: white;
  padding: 20px;
  border-radius: 8px;
}
</style>