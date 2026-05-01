<script setup lang="ts">
// layout调用了Aside组件，用于显示侧边栏
import Aside from '@/components/Aside.vue';
import { ref } from 'vue';
const userInfo = ref(JSON.parse(sessionStorage.getItem('user')))
const handleOut = () => {
    sessionStorage.clear();
    window.location.href = '/login'
}

</script>

<template>
    <!-- layout布局 -->
    <div class="common-layout">
        <el-container>
            <el-header class="header">
                <img class="logo"
                    src="https://picx.zhimg.com/v2-d6f44389971daab7e688e5b37046e4e4_720w.jpg?source=172ae18b" alt="">
                <el-menu mode="horizontal" :default-active="1">
                    <el-menu-item index="2">关于我们</el-menu-item>
                    <el-menu-item index="3">联系我们</el-menu-item>
                    <el-menu-item index="1">{{ userInfo.username }}</el-menu-item>
                    <el-menu-item index="2" @click="handleOut">退出登录</el-menu-item>
                    <!-- <el-menu-item index="2">关于我们</el-menu-item>
                    <el-menu-item index="3">联系我们</el-menu-item> -->
                </el-menu>
            </el-header>
            <el-container class="container">
                <Aside></Aside>
                <el-main>
                    <RouterView />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<style>
.common-layout {
    /* background-color: red; */
    height: 100vh;
}

.header {
    background-color: #efefef;
    height: 80px;
    border-bottom: 2px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #eee;
}


.logo {
    height: 100%;
}

.container {

    /* background-color: aquamarine; */
    height: calc(100vh - 80px);
}

.aside {
    width: 240px;
    /* background-color: blueviolet; */
}
</style>
<style>
.wrap-container {
    padding: 20px;
}

.wrap-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    background-color: rgb(241, 240, 240);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)
}

.header-title {
    font-size: 24px;
    font-weight: bold;
}
</style>
