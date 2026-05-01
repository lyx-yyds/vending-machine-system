import request from "../utils/request";

export const login = (data: any) => {
    return request.post("/user/login", data);
}

export const getUserList = (params?: any) => {
    return request.get("/user/list/", { params });
}

export const updateUserStatus = (data: any) => {
    return request.put("/user/status/", data);
}

export const resetUserPassword = (data: any) => {
    return request.put("/user/password/", data);
}

export const getUserProfile = (params?: any) => {
    return request.get("/user/profile/", { params });
}

export const updateUserProfile = (data: any) => {
    return request.put("/user/profile/", data);
}

export const changePassword = (data: any) => {
    return request.put("/user/change-password/", data);
}
