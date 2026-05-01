import request from "../utils/request";

export const getDashboard = () => {
    return request.get("/dashboard/");
}