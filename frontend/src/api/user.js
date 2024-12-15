import { api } from './base'

// 获取用户信息
export const getUserProfile = () => {
  return api.get('users/profile')
}

// 更新用户信息
export const updateUserProfile = (data) => {
  return api.put('users/profile', data)
}

// 修改密码
export const changePassword = (data) => {
  return api.put('users/password', data)
} 