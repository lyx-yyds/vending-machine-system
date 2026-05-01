<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        商品单位管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.unit_name" placeholder="请输入单位名称" style="width: 150px" clearable></el-input>
        <el-button round icon="Plus" type="primary" @click="createHandler">新增</el-button>
        <el-button round type="primary" icon="Search" @click="searchUnitList">搜索</el-button>
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
        <el-table-column prop="unit_code" label="单位编码" width="150">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.unit_code }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="unit_name" label="单位名称" width="150"></el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
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
        @current-change="fetchUnitList"
        style="margin-top: 20px"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="600">
      <el-form :model="formData" label-width="100px">
        <el-form-item v-show="dialogTitle === '编辑单位'" label="单位编码">
          <el-input disabled v-model="formData.unit_code"></el-input>
        </el-form-item>
        <el-form-item label="单位名称" required>
          <el-input v-model="formData.unit_name" placeholder="请输入单位名称（如：个、瓶、盒）"></el-input>
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
import { getUnitList, deleteUnit, addUnit, updateUnit } from '@/api/unit'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const dialogFormVisible = ref(false)
const dialogTitle = ref('新增单位')

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  unit_name: ''
})

const formData = reactive({
  id: 0,
  unit_code: '',
  unit_name: '',
  remark: '',
  status: 0
})

const listData = ref([])

const fetchUnitList = async () => {
  loading.value = true
  try {
    const response = await getUnitList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取单位列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchUnitList = () => {
  page.pageNum = 1
  fetchUnitList()
}

const resetSearchHandler = () => {
  searchForm.unit_name = ''
  page.pageNum = 1
  fetchUnitList()
}

const deleteHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该单位吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await deleteUnit(row.id)
    if (result.data.code === 2000) {
      ElMessage.success('删除成功')
      fetchUnitList()
    } else {
      ElMessage.error(result.data.message || '删除失败')
    }
  } catch {
  }
}

const createHandler = () => {
  dialogFormVisible.value = true
  dialogTitle.value = '新增单位'
  formData.id = 0
  formData.unit_code = ''
  formData.unit_name = ''
  formData.remark = ''
  formData.status = 0
}

const editHandler = (row: any) => {
  dialogFormVisible.value = true
  dialogTitle.value = '编辑单位'
  formData.id = row.id
  formData.unit_code = row.unit_code
  formData.unit_name = row.unit_name
  formData.remark = row.remark
  formData.status = row.status
}

const addSubmitHandler = async () => {
  if (!formData.unit_name) {
    ElMessage.warning('请输入单位名称')
    return
  }

  try {
    if (dialogTitle.value === '新增单位') {
      const res = await addUnit(formData)
      if (res.data.code === 2000) {
        ElMessage.success('新增成功')
        dialogFormVisible.value = false
        fetchUnitList()
      } else {
        ElMessage.error(res.data.message || '新增失败')
      }
    } else {
      const res = await updateUnit(formData)
      if (res.data.code === 2000) {
        ElMessage.success('更新成功')
        dialogFormVisible.value = false
        fetchUnitList()
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
  fetchUnitList()
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
