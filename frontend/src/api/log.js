import { api } from './base'

// 获取操作日志
export const getLogs = (params) => {
  return api.get('system/logs', { params })
} 