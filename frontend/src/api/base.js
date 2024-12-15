import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      console.log('Sending request with token:', token)
      // 确保token格式正确
      const finalToken = token.startsWith('Bearer ') ? token : `Bearer ${token}`
      config.headers.Authorization = finalToken
      
      // 移除URL末尾的斜杠
      if (config.url.endsWith('/')) {
        config.url = config.url.slice(0, -1)
      }
      
      // 打印完整的请求配置
      console.log('Final request config:', {
        url: config.url,
        method: config.method,
        headers: config.headers,
        baseURL: config.baseURL
      })
    } else {
      console.log('No token found in localStorage')
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('Response error:', error)
    console.error('Response error config:', error.config)
    console.error('Response error response:', error.response)

    let message = '请求失败'
    if (error.response) {
      message = error.response.data?.message || message
      
      if (error.response.status === 401) {
        // 只在非登录请求时处理401
        if (!error.config.url.includes('/auth/login')) {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          ElMessage.error('认证失败，3秒后跳转到登录页')
          setTimeout(() => {
            router.push('/login')
          }, 3000)
        }
      }
    } else if (error.request) {
      message = '服务器无响应，请检查后端服务���否启动'
    } else {
      message = error.message
    }
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export { api } 