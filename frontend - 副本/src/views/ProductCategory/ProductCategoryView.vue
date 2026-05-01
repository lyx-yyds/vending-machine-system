<template>
    <div class="wrap-container">
        <div class="wrap-header">
            <div class="header-title">
                新增商品分类
            </div>
            <div class="header-actions">
                <el-input placeholder="请输入商品分类名称" v-model="searchCategoryName"></el-input>
                <el-button round icon="plus" type="primary" @click="createHandler">新增</el-button>
                <el-button round color="purple" icon="search" @click="searchCategoryList">搜索</el-button>
                <el-button round type="danger" icon="delete">重置</el-button>     
            </div>
        </div>
        <div class="wrap-table">
            <el-table :data="listData">
                <el-table-column label="序号" width="80">
                    <template #default="{ $index }">
                        {{ $index + 1 }}
                    </template>
                </el-table-column>
                <el-table-column prop="category_code" label="商品分类编号" width="200">
                    <template #default="{ row }">
                        <el-tag type="primary">{{ row.category_code }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="category_name" label="商品分类名称" width="120"></el-table-column>   

                <el-table-column prop="remark" label="备注"></el-table-column>
                <el-table-column prop="status" label="状态">
                    <template #default="{ row }">
                        <el-switch v-model="row.status" :active-value="0" :inactive-value="1"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column prop="create_time" label="创建时间">
                    <template #default="{ row }">
                        <el-tag type="success">{{ row.create_time }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="update_time" label="更新时间">
                    <template #default="{ row }">
                        <el-tag>{{ row.update_time }}</el-tag>
                    </template>
                </el-table-column>

                <el-table-column>
                    <template #default="{ row }">
                        <el-button type="primary" size="small" @click="editHandler(row)">编辑</el-button>
                        <el-button type="danger" size="small" @click="deleteHanlder(row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination background layout="prev, pager, next,total,jumper" v-model:total="page.total"
                v-model:page-size="page.pageSize" v-model:current-page="page.pageNum"
                @current-change="fetchCategoryList" />
        </div>


        <el-dialog v-model="dialogFormVisible" :title="dialogTitle" width="500">
            <el-form :model="formData" label-width="100px">
                <el-form-item v-show="dialogTitle === '编辑商品分类' ? true : false" label="商品分类编号">
                    <el-input disabled v-model="formData.category_code"></el-input>
                </el-form-item>
                <el-form-item label="商品分类名称">
                    <el-input v-model="formData.category_name"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="formData.remark"></el-input>
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
import { getCategoryList, deleteCategory, addCategory, updateCategory } from '@/api/product';
import { ElMessage, ElMessageBox } from 'element-plus';
import { reactive, ref } from 'vue';
// 定义组件的状态变量
const dialogFormVisible = ref(false) // 对话框的显示状态
const dialogTitle = ref('新增商品分类') // 对话框的标题 

// 分页数据
const page = reactive({
    pageNum: 1,
    pageSize: 10,
    total: 0
})

const searchCategoryName = ref('')


// form表单数据
const formData = reactive({
    id: 0,
    category_code: '',
    category_name: '',
    remark: '',
    status: 1,
})

const searchCategoryList = async () => {    
    try {

        //                       promise对象
        const response = await getCategoryList({ ...page, category_name: searchCategoryName.value });
        if (response.data.code === 2000) {
            console.log('商品分类列表数据:', response.data.data);
            listData.value = response.data.data.list;
            // 分页数据的更新
            page.total = response.data.data.total
            page.pageSize = response.data.data.pageSize
            page.pageNum = response.data.data.pageNum
        } else {
            console.error('获取品牌列表失败:', response.data.message);
        }
        console.log('品牌列表数据:', response.data);
        // 在这里可以将获取到的数据赋值给组件的状态变量，以便在模板中使用
    } catch (error) {
        console.error('获取品牌列表失败:', error);
    }
}

// 定义组件的状态变量
const listData = ref([]); // 品牌列表数据
// 获取商品分类列表数据
const fetchCategoryList = async () => {
    try {

        //                       promise对象
        const response = await getCategoryList(page);
        if (response.data.code === 2000) {
            console.log('商品分类列表数据:', response.data.data);
            listData.value = response.data.data.list;
            // 分页数据的更新
            page.total = response.data.data.total
            page.pageSize = response.data.data.pageSize
            page.pageNum = response.data.data.pageNum
        } else {
            console.error('获取品牌列表失败:', response.data.message);
        }
        console.log('品牌列表数据:', response.data);
        // 在这里可以将获取到的数据赋值给组件的状态变量，以便在模板中使用
    } catch (error) {
        console.error('获取品牌列表失败:', error);
    }
};

// 删除处理函数
const deleteHanlder = async (row: any) => {
    ElMessageBox.confirm('确定要删除该品牌吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error',
    }).then(async () => {
        // 在这里可以调用删除品牌的API，并根据需要更新品牌列表数据
        const result = await deleteCategory(row.id)
        if (result.data.code === 2000) {
            console.log('删除商品分类成功:', result.data.message);
            ElMessage({
                message: result.data.message,
                type: 'success',
            })
            // 删除成功后，刷新商品分类列表数据
            fetchCategoryList();
        } else {
            // console.error('删除商品分类失败:', result.data.message);     
            ElMessage({
                message: result.data.message,
                type: 'error',
            })
        }

    })

    // console.log('删除商品分类:', row.id);

}

const createHandler = async () => {
    dialogFormVisible.value = true;
    dialogTitle.value = '新增商品分类';
    formData.category_code = ''
    formData.category_name = ''
    formData.remark = ''
    formData.status = 0

}
// 提交按钮
const addSubmitHandler = async () => {
    if (dialogTitle.value === '新增商品分类') {     
        // 调用新增的接口
        const res = await addCategory(formData)
        if (res.data.code === 2000) {
            ElMessage({
                message: res.data.message,
                type: 'success',
            })
        } else {
            ElMessage({
                message: res.data.message,
                type: 'error',
            })
        }

    } else {
        // 调用接口
        const res = await updateCategory(formData.id, formData)
        if (res.data.code === 2000) {
            ElMessage({
                message: res.data.message,
                type: 'success',
            })
        } else {
            ElMessage({
                message: res.data.message,
                type: 'error',
            })
        }
    }


    dialogFormVisible.value = false;
    // 重新获取列表的数据
    fetchCategoryList();
}

// 编辑处理函数
const editHandler = async (row: any) => {
    console.log('编辑商品分类:', row.id);
    dialogFormVisible.value = true;
    dialogTitle.value = '编辑商品分类';
    formData.id = row.id
    formData.category_code = row.category_code
    formData.category_name = row.category_name
    formData.remark = row.remark
    formData.status = row.status

    // 重新获取列表的数据
    // fetchCategoryList();
}

// 调用获取商品分类列表数据的方法
fetchCategoryList();


//列表数据
// const listData = [
//     {
//         id: 1,
//         name: '商品分类1',
//         logo: 'https://picx.zhimg.com/v2-d6f44389971daab7e688e5b37046e4e4_720w.jpg?source=172ae18b'
//     },
//     {
//         id: 2,
//         name: '商品分类2',           
//         logo: 'https://picx.zhimg.com/v2-d6f44389971daab7e688e5b37046e4e4_720w.jpg?source=172ae18b'
//     },
// ]

</script>



