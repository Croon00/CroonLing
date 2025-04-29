import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080", // 기본 주소
  timeout: 10000,
});

export default axiosInstance;
