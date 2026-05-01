<template>
    <!-- <el-aside width="200px" height="100%">
        <el-scrollbar style="height: 100%;"> -->
    <!-- 启动vue-router 路由模式 -->

    <!-- </el-scrollbar>
    </el-aside> -->
    <div class="slide-bar-wrap ">
        <el-menu :router="true" :default-openeds="['1', '3']">
            <template v-for="item in menudata" :key="item.name">
                <el-sub-menu class="sub-menu-wrap" :index="item.index"
                    v-if="item.access.includes(accessMap[role_type])">
                    <template #title>
                        <el-icon>
                            <component :is="item.icon" />
                        </el-icon>{{ item.name }}
                    </template>
                    <!-- route 属性，进行路由跳转 -->
                    <template v-for="child in item.children" :key="child.name">
                        <el-menu-item class="el-menu-item" :index="child.index" :route="child.route"
                            v-if="child.access.includes(accessMap[role_type])">{{ child.name
                            }}</el-menu-item>
                    </template>
                    <!-- </el-menu-item-group> -->
                </el-sub-menu>
            </template>
        </el-menu>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';

const accessMap = ref({
    1: 'admin',
    2: 'user'
})
const role_type = ref(sessionStorage.getItem('role_type'))
// const role_type = ref(accessMap[sessionStorage.getItem('role_type')])




const menudata = ref([
    {
        name: '首页',
        icon: 'HomeFilled',
        access: ['admin', 'user'],
        children: [
            {
                name: '控制台',
                route: '/backend/home',
                access: ['admin', 'user'],
            }
        ]
    },
    {
        name: '基础数据管理',
        icon: 'message',
        access: ['admin'],
        children: [
            {
                name: '商品类别',
                route: '/backend/product-category',
                access: ['admin'],
            },
            {
                name: '商品信息',
                route: '/backend/product-info',
                access: ['admin'],
            },
            {
                name: '商品单位',
                route: '/backend/unit',
                access: ['admin'],
            },
            {
                name: '商品规格',
                route: '/backend/specifications',
                access: ['admin'],
            }

        ]
    },
    {
        name: '商品管理',
        icon: 'setting',
        access: ['admin'],
        children: [
            
            {
                name: '供应商管理',
                route: '/backend/supplier',
                access: ['admin'],
            },
            {
                name: '商品入库',
                route: '/backend/inbound',
                access: ['admin'],
            },
            {
                name: '入库记录',
                route: '/backend/inbound-detail',
                access: ['admin'],
            }
        ]
    },
    {
        name: '订单管理',
        icon: 'setting',
        access: ['admin'],
        children: [
            {
                name: '订单列表',
                route: '/backend/order',
                access: ['admin'],
            },
            {
                name: '订单详情',
                route: '/backend/order-detail',
                access: ['admin'],
            }
        ]
    },
    {
        name: '支付管理',
        icon: 'setting',
        access: ['admin'],
        children: [
            {
                name: '支付记录',
                route: '/backend/payment',
                access: ['admin'],
            },
            {
                name: '退款记录',
                route: '/backend/refund',
                access: ['admin'],
            }
        ]
    },
    {
        name: '库存管理',
        icon: 'setting',
        access: ['admin'],
        children: [
            {
                name: '库存列表',
                route: '/backend/stock',
                access: ['admin'],
            },
        ]
    },
    {
        name: '用户管理',
        icon: 'setting',
        access: ['admin'],
        children: [
            {
                name: '用户列表',
                route: '/backend/user',
                access: ['admin'],
            },
        ]
    },
    {
        name: '商城',
        icon: 'shopping',
        access: ['user'],
        children: [
            {
                name: '商品浏览',
                route: '/backend/shop',
                access: ['user'],
            },
        ]
    },
    {
        name: '个人中心',
        icon: 'user',
        access: ['user'],
        children: [
            {
                name: '个人资料',
                route: '/backend/profile',
                access: ['user'],
            },
            {
                name: '我的订单',
                route: '/backend/my-order',
                access: ['user'],
            },
        ]
    }
    
]);

// 申请单管理
// path: 'borrow-list',
//     name: 'borrow-list',
//         component: () => import('../views/Borrow/BorrowRequestList.vue')

const createIndexForMenu = (menu) => {
    const result = menu.map((item, index) => {
        // console.log(item, index);
        const parentIndex = `${index + 1}`;
        item.index = parentIndex;
        if (item.children) {
            item.children.map((childItem, childIndex) => {
                const childIndexStr = `${parentIndex}-${childIndex + 1}`;
                childItem.index = childIndexStr;
            })
        }
        // return createIndex(item, parentIndex, index);
    });
    // console.log(menudata.value);
    return result;
};
createIndexForMenu(menudata.value);

</script>
<style scoped>
:root {
    --el-menu-active-color: var(--el-color-primary);
    --el-menu-text-color: #fff;
    --el-menu-bg-color: #222d3c;
    --el-menu-hover-bg-color: #0e1114;
    --el-menu-item-height: 56px;
    --el-menu-sub-item-height: calc(var(--el-menu-item-height) - 6px);
    --el-menu-horizontal-height: 60px;
}
</style>
<style scoped>
.slide-bar-wrap {
    color: aliceblue !important;
    height: calc(100vh - 80px);
    width: 240px;
    /* height: 100%; */
    /* background-color: #334154; */
}
</style>
<!-- <style scoped>
.slide-bar-wrap {
    color: aliceblue !important;
    height: calc(100vh - 80px);
    width: 240px;
    /* height: 100%; */
    background-color: #334154;
}

.sub-menu-wrap {
    background-color: #334154;
    color: aliceblue !important;
}

.el-sub-menu {
    color: aliceblue !important;
}



.el-sub-menu__title {
    color: aliceblue !important;
}

.el-sub-menu__title:hover {
    color: #334154 !important;
}

.el-menu-item-group {
    background-color: #334154;
    color: aliceblue !important;

}

.el-menu-item {
    background-color: #222d3c;
    color: aliceblue !important;
}

.el-menu-item:hover {
    background-color: #0e1114;
    color: aliceblue !important;
}
</style> -->