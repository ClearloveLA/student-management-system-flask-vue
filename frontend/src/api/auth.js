import { ElMessage } from 'element-plus'
import { api } from './base'

// API函数
export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', { username, password })
    // 确保返回的数据包含必要的字段
    if (response.access_token && response.user) {
      return response
    } else {
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('登录失败:', error)
    throw error
  }
}

export const register = async (userData) => {
  try {
    const response = await api.post('/auth/register', userData)
    ElMessage.success('注册成功')
    return response
  } catch (error) {
    console.error('注册失败:', error)
    throw error
  }
}

export const logout = async () => {
  try {
    const response = await api.post('/auth/logout')
    ElMessage.success('登出成功')
    return response
  } catch (error) {
    console.error('登出失败:', error)
    throw error
  }
} 