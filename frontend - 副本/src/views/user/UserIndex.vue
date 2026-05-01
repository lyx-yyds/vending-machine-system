<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        用户管理
      </div>
      <div class="header-actions">
        <el-input v-model="searchForm.username" placeholder="请输入用户名" style="width: 150px" clearable></el-input>
        <el-input v-model="searchForm.real_name" placeholder="请输入真实姓名" style="width: 150px" clearable></el-input>
        <el-button round type="primary" icon="Search" @click="searchUserList">搜索</el-button>
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
        <el-table-column prop="username" label="用户名" width="120">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.username }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="真实姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="130"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="180"></el-table-column>
        <el-table-column prop="role_type" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role_type === 1 ? 'danger' : row.role_type === 2 ? 'info' : 'success'">
              {{ row.role_type === 1 ? '管理员' : row.role_type === 2 ? '普通用户' : '运营人员' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="账户余额" width="120">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">¥{{ row.balance }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'danger'">
              {{ row.status === 0 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            <el-tag type="info">{{ row.create_time }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="warning" size="small" @click="handleToggleStatus(row)">
              {{ row.status === 0 ? '禁用' : '启用' }}
            </el-button>
            <el-button type="primary" size="small" @click="handleResetPassword(row)">重置密码</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="prev, pager, next,total,jumper"
        v-model:total="page.total"
        v-model:page-size="page.pageSize"
        v-model:current-page="page.pageNum"
        @current-change="fetchUserList"
        style="margin-top: 20px"
      />
    </div>

    <el-dialog v-model="passwordDialogVisible" title="重置密码" width="400px">
      <el-form :model="passwordForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="passwordForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.password" type="password" show-password placeholder="请输入新密码"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmResetPassword">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getUserList, updateUserStatus, resetUserPassword } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)

const page = reactive({
  pageNum: 1,
  pageSize: 10,
  total: 0
})

const searchForm = reactive({
  username: '',
  real_name: ''
})

const listData = ref([])

const passwordDialogVisible = ref(false)
const passwordForm = reactive({
  id: 0,
  username: '',
  password: ''
})

const fetchUserList = async () => {
  loading.value = true
  try {
    const response = await getUserList({ ...page, ...searchForm })
    if (response.data.code === 2000) {
      listData.value = response.data.data.list
      page.total = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '获取列表失败')
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const searchUserList = () => {
  page.pageNum = 1
  fetchUserList()
}

const resetSearchHandler = () => {
  searchForm.username = ''
  searchForm.real_name = ''
  page.pageNum = 1
  fetchUserList()
}

const handleToggleStatus = async (row: any) => {
  const action = row.status === 0 ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定要${action}用户"${row.username}"吗?`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const newStatus = row.status === 0 ? 1 : 0
    const response = await updateUserStatus({ id: row.id, status: newStatus })
    if (response.data.code === 2000) {
      ElMessage.success(`${action}成功`)
      fetchUserList()
    } else {
      ElMessage.error(response.data.message || `${action}失败`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${action}失败:`, error)
    }
  }
}

const handleResetPassword = (row: any) => {
  passwordForm.id = row.id
  passwordForm.username = row.username
  passwordForm.password = ''
  passwordDialogVisible.value = true
}

const confirmResetPassword = async () => {
  if (!passwordForm.password) {
    ElMessage.warning('请输入新密码')
    return
  }
  try {
    const response = await resetUserPassword({ id: passwordForm.id, password: passwordForm.password })
    if (response.data.code === 2000) {
      ElMessage.success('密码修改成功')
      passwordDialogVisible.value = false
    } else {
      ElMessage.error(response.data.message || '密码修改失败')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error('密码修改失败')
  }
}

onMounted(() => {
  fetchUserList()
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
