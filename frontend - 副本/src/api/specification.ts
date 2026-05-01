import request from "../utils/request";

export const getSpecificationList = (params?: any) => {
    return request.get("/specifications/list/", { params });
}

export const addSpecification = (data: any) => {
    return request.post("/specifications/add/", data);
}

export const updateSpecification = (data: any) => {
    return request.put("/specifications/update/", data);
}

export const deleteSpecification = (id: number) => {
    return request.delete(`/specifications/${id}/`);
}
