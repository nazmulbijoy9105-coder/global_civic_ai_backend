import axios from "axios";

const API_BASE = "https://global-civic-ai-backend.onrender.com";

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach token to every request
apiClient.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle global errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
    }
    return Promise.reject(
      error.response?.data?.detail
        ? new Error(error.response.data.detail)
        : new Error("Something went wrong")
    );
  }
);

export const api = {
  signup: async (userData) => {
    const res = await apiClient.post("/auth/register", userData);
    return res.data;
  },

  login: async ({ username, password }) => {
    const res = await apiClient.post("/auth/login", { username, password });
    localStorage.setItem("token", res.data.access_token);
    return res.data;
  },

  getCurrentUser: async () => {
    const res = await apiClient.get("/users/me");
    return res.data;
  },

  logout: () => {
    localStorage.removeItem("token");
  },
};