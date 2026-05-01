<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        商品信息管理
      </div>
      <div class="header-actions">
        <!-- <el-select v-model="searchForm.category_id" placeholder="选择分类" clearable style="width: 150px">
          <el-option v-for="item in categoryList" :key="item.id" :label="item.category_name" :value="item.id" />
        </el-select> -->
        <el-input v-model="searchForm.product_name" placeholder="请输入商品名称" style="width: 150px" clearable></el-input>
        <el-button round icon="Plus" type="primary" @click="createHandler">新增</el-button>
        <el-button round type="primary" icon="Search" @click="searchProductList">搜索</el-button>
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
        <el-table-column prop="product_code" label="商品编码" width="200">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.product_code }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="商品名称" width="150"></el-table-column>
        <el-table-column prop="category_name" label="分类名称" width="120">
          <template #default="{ row }">
            <el-tag type="success">{{ row.category_name || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cost_price" label="成本价" width="100"></el-table-column>
        <el-table-column prop="selling_price" label="售价" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'danger'">
              {{ row.status === 0 ? '上架' : '下架' }}
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
        @current-change="fetchProductList"
        style="margin-top: 20px"
      />
    </div>

    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="600">
      <el-form :model="formData" label-width="100px">
        <el-form-item v-show="dialogTitle === '编辑商品'" label="商品编码">
          <el-input disabled v-model="formData.product_code"></el-input>
        </el-form-item>
        <el-form-item label="商品名称">
          <el-input v-model="formData.product_name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        <el-form-item label="商品分类">
          <el-select v-model="formData.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="item in categoryList" :key="item.id" :label="item.category_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="成本价">
          <el-input-number v-model="formData.cost_price" :precision="2" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="售价">
          <el-input-number v-model="formData.selling_price" :precision="2" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="图片URL">
          <el-input v-model="formData.image_url" placeholder="请输入图片URL"></el-input>
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
import { getProductList, deleteProduct, addProduct, updateProduct, getCategorySimple } from '@/api/product'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const dialogFormVisible = ref(false)
const dialogTitle = ref('新增商品')

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  product_name: '',
  category_id: ''
})

const categoryList = ref<any[]>([])

const formData = reactive({
  id: 0,
  product_code: '',
  product_name: '',
  category_id: '',
  cost_price: 0,
  selling_price: 0,
  image_url: '',
  remark: '',
  status: 1
})

const listData = ref([])

const fetchCategoryList = async () => {
  try {
    const response = await getCategorySimple()
    if (response.data.code === 2000) {
      categoryList.value = response.data.data
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

const fetchProductList = async () => {
  loading.value = true
  try {
    const response = await getProductList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchProductList = () => {
  page.pageNum = 1
  fetchProductList()
}

const resetSearchHandler = () => {
  searchForm.product_name = ''
  searchForm.category_id = ''
  page.pageNum = 1
  fetchProductList()
}

const deleteHandler = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const result = await deleteProduct(row.id)
    if (result.data.code === 2000) {
      ElMessage.success('删除成功')
      fetchProductList()
    } else {
      ElMessage.error(result.data.message || '删除失败')
    }
  } catch {
    // 用户取消操作
  }
}

const createHandler = () => {
  dialogFormVisible.value = true
  dialogTitle.value = '新增商品'
  formData.id = 0
  formData.product_code = ''
  formData.product_name = ''
  formData.category_id = ''
  formData.cost_price = 0
  formData.selling_price = 0
  formData.image_url = ''
  formData.remark = ''
  formData.status = 1
}

const editHandler = (row: any) => {
  dialogFormVisible.value = true
  dialogTitle.value = '编辑商品'
  formData.id = row.id
  formData.product_code = row.product_code
  formData.product_name = row.product_name
  formData.category_id = row.category_id
  formData.cost_price = row.cost_price
  formData.selling_price = row.selling_price
  formData.image_url = row.image_url
  formData.remark = row.remark
  formData.status = row.status
}

const addSubmitHandler = async () => {
  if (!formData.product_name) {
    ElMessage.warning('请输入商品名称')
    return
  }
  if (!formData.category_id) {
    ElMessage.warning('请选择商品分类')
    return
  }

  try {
    if (dialogTitle.value === '新增商品') {
      const res = await addProduct(formData)
      if (res.data.code === 2000) {
        ElMessage.success('新增成功')
        dialogFormVisible.value = false
        fetchProductList()
      } else {
        ElMessage.error(res.data.message || '新增失败')
      }
    } else {
      const res = await updateProduct(formData)
      if (res.data.code === 2000) {
        ElMessage.success('更新成功')
        dialogFormVisible.value = false
        fetchProductList()
      } else {
        ElMessage.error(res.data.message || '更新失败')
      }
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchCategoryList()
  fetchProductList()
})
</script>

<style scoped>
.wrap-container {
  padding: 20px;
}

.wrap-header {
  margin-bottom: 20px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
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