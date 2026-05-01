import request from "../utils/request";

export const getStockList = (params?: any) => {
    return request.get("/stock/list/", { params });
}
