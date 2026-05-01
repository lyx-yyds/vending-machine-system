import request from "../utils/request";

export const getPaymentList = (params?: any) => {
    return request.get("/payment/list/", { params });
}

export const getRefundList = (params?: any) => {
    return request.get("/payment/refund/list/", { params });
}

export const processRefund = (data: any) => {
    return request.put("/payment/refund/process/", data);
}
