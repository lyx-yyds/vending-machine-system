import request from "../utils/request";

export const getInboundRecordList = (params?: any) => {
    return request.get("/inbound/record/list/", params);
}

export const addInboundRecord = (data: any) => {
    return request.post("/inbound/record/add/", data);
}

export const updateInboundRecord = (data: any) => {
    return request.put("/inbound/record/update/", data);
}

export const deleteInboundRecord = (id: number) => {
    return request.delete(`/inbound/record/${id}/`);
}

export const confirmInboundRecord = (data: any) => {
    return request.put("/inbound/record/confirm/", data);
}

export const getInboundDetailList = (params?: any) => {
    return request.get("/inbound/detail/list/", { params });
}

export const addInboundDetail = (data: any) => {
    return request.post("/inbound/detail/add/", data);
}

export const updateInboundDetail = (data: any) => {
    return request.put("/inbound/detail/update/", data);
}

export const deleteInboundDetail = (id: number) => {
    return request.delete(`/inbound/detail/${id}/`);
}