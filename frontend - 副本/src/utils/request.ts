import axios from 'axios';

const instance = axios.create({
    baseURL: '/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.request.use(
    (config) => {
        // 在发送请求之前做些什么
        // config.headers.Authorization = localStorage.getItem('token');
        //  添加白名单，不需要token的接口 [‘’, ‘’]-数组
        const whiteList = ['/user/login', '/user/register'];
        if (!whiteList.includes(config.url || '')) {
            config.headers.Authorization = "Bearer " + sessionStorage.getItem('token');
        }
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);

// 响应拦截器
instance.interceptors.response.use(
    (response) => {
        // 对响应数据做些什么
        return response;
    },
    (error) => {
        // 对响应错误做些什么
        return Promise.reject(error);
    }
);

export default instance;