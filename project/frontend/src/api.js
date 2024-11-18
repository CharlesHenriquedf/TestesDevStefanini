import axios from "axios";

// Base URL do backend
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Configuração da instância do Axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para adicionar o token JWT às requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // Obter o token do localStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Adicionar o token ao cabeçalho
  }
  return config;
});

export default api;
