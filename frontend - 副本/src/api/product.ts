import request from "../utils/request";

export const getCategoryList = (params?: any) => {
    return request.get("/product/category/list/", params);
}

export const getCategorySimple = () => {
    return request.get("/product/category/simple/");
}

export const deleteCategory = (id: number) => {
    return request.delete(`/product/category/${id}/`);
}

export const addCategory = (data: any) => {
    return request.post("/product/category/add/", data);
}

export const updateCategory = (data: any) => {
    return request.put("/product/category/update/", data);
}

export const getProductList = (params?: any) => {
    return request.get("/product/list/", params);
}

export const deleteProduct = (id: number) => {
    return request.delete(`/product/${id}/`);
}

export const addProduct = (data: any) => {
    return request.post("/product/add/", data);
}

export const updateProduct = (data: any) => {
    return request.put("/product/update/", data);
}

export const getSupplierList = (params?: any) => {
    return request.get("/product/supplier/list/", params);
}

export const deleteSupplier = (id: number) => {
    return request.delete(`/product/supplier/${id}/`);
}

export const addSupplier = (data: any) => {
    return request.post("/product/supplier/add/", data);
}

export const updateSupplier = (data: any) => {
    return request.put("/product/supplier/update/", data);
}