import request from "../utils/request";

export const getOrderList = (params?: any) => {
    return request.get("/order/list/", { params });
}

export const getMyOrderList = (params?: any) => {
    return request.get("/order/my-list/", { params });
}

export const getOrderDetailList = (params?: any) => {
    return request.get("/order/detail/list/", { params });
}

export const createOrder = (data: any) => {
    return request.post("/order/create/", data);
}

export const payOrder = (data: any) => {
    return request.put("/order/pay/", data);
}

export const refundOrder = (data: any) => {
    return request.post("/order/refund/", data);
}
