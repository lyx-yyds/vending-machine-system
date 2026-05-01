<template>
  <div class="wrap-container">
    <div class="wrap-header">
      <div class="header-title">
        个人资料
      </div>
    </div>
    <div class="wrap-content">
      <el-card class="profile-card">
        <el-form :model="profileForm" label-width="100px" style="max-width: 500px;">
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" disabled></el-input>
          </el-form-item>
          <el-form-item label="真实姓名">
            <el-input v-model="profileForm.real_name" placeholder="请输入真实姓名"></el-input>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="profileForm.phone" placeholder="请输入手机号"></el-input>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="profileForm.email" placeholder="请输入邮箱"></el-input>
          </el-form-item>
          <el-form-item label="角色">
            <el-tag :type="profileForm.role_type === 1 ? 'danger' : profileForm.role_type === 2 ? 'info' : 'success'">
              {{ profileForm.role_type === 1 ? '管理员' : profileForm.role_type === 2 ? '普通用户' : '运营人员' }}
            </el-tag>
          </el-form-item>
          <el-form-item label="账户余额">
            <span style="color: #67c23a; font-weight: bold;">¥{{ profileForm.balance }}</span>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleUpdateProfile">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="password-card" style="margin-top: 20px;">
        <template #header>
          <div class="card-header">
            <span>修改密码</span>
          </div>
        </template>
        <el-form :model="passwordForm" label-width="100px" style="max-width: 500px;">
          <el-form-item label="原密码">
            <el-input v-model="passwordForm.old_password" type="password" show-password placeholder="请输入原密码"></el-input>
          </el-form-item>
          <el-form-item label="新密码">
            <el-input v-model="passwordForm.new_password" type="password" show-password placeholder="请输入新密码"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getUserProfile, updateUserProfile, changePassword } from '@/api/user'
import { ElMessage } from 'element-plus'

const profileForm = reactive({
  id: 0,
  username: '',
  real_name: '',
  phone: '',
  email: '',
  role_type: 0,
  balance: 0
})

const passwordForm = reactive({
  old_password: '',
  new_password: ''
})

const fetchProfile = async () => {
  const user_id = sessionStorage.getItem('user_id')
  if (!user_id) {
    ElMessage.error('用户未登录')
    return
  }
  try {
    const response = await getUserProfile({ user_id })
    if (response.data.code === 2000) {
      Object.assign(profileForm, response.data.data)
    } else {
      ElMessage.error(response.data.message || '获取资料失败')
    }
  } catch (error) {
    console.error('获取资料失败:', error)
    ElMessage.error('获取资料失败')
  }
}

const handleUpdateProfile = async () => {
  try {
    const response = await updateUserProfile({
      id: profileForm.id,
      real_name: profileForm.real_name,
      phone: profileForm.phone,
      email: profileForm.email
    })
    if (response.data.code === 2000) {
      ElMessage.success('更新成功')
      fetchProfile()
    } else {
      ElMessage.error(response.data.message || '更新失败')
    }
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  }
}

const handleChangePassword = async () => {
  if (!passwordForm.old_password || !passwordForm.new_password) {
    ElMessage.warning('请填写完整')
    return
  }
  if (passwordForm.new_password.length < 6) {
    ElMessage.warning('新密码长度不能少于6位')
    return
  }
  const user_id = sessionStorage.getItem('user_id')
  try {
    const response = await changePassword({
      user_id,
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    if (response.data.code === 2000) {
      ElMessage.success('密码修改成功')
      passwordForm.old_password = ''
      passwordForm.new_password = ''
    } else {
      ElMessage.error(response.data.message || '密码修改失败')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error('密码修改失败')
  }
}

onMounted(() => {
  fetchProfile()
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
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.wrap-content {
  max-width: 600px;
}

.profile-card,
.password-card {
  border-radius: 8px;
}

.card-header {
  font-weight: bold;
}
</style>
