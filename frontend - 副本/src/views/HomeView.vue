<!-- <script setup lang="ts">
import Aside from '../components/Aside.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleOut = () => {
  sessionStorage.clear()
  router.push('/login')
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header">
        <img class="logo" src="https://picx.zhimg.com/v2-d6f44389971daab7e688e5b37046e4e4_720w.jpg?source=172ae18b" alt="">
        <el-menu mode="horizontal" :default-active="1">
          <el-menu-item index="1">管理员</el-menu-item>
          <el-menu-item index="2" @click="handleOut">退出登录</el-menu-item>
        </el-menu>
      </el-header>
      <el-container class="container">
        <Aside />
        <el-main>
          <main>
            <h1>首页</h1>
          </main>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100vh;
}

.header {
  background-color: #efefef;
  height: 80px;
  border-bottom: 2px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #333;
}

.logo {
  height: 100%;
}

.container {
  height: calc(100vh - 80px);
}
</style> -->



<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <TheWelcome />
  </main>
</template>
