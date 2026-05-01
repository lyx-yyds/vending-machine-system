import request from "../utils/request";

export const getUnitList = (params?: any) => {
    return request.get("/unit/list/", { params });
}

export const getUnitSimple = () => {
    return request.get("/unit/simple/");
}

export const addUnit = (data: any) => {
    return request.post("/unit/add/", data);
}

export const updateUnit = (data: any) => {
    return request.put("/unit/update/", data);
}

export const deleteUnit = (id: number) => {
    return request.delete(`/unit/${id}/`);
}