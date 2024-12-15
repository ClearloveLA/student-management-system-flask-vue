import { api } from './base'

export const getLogs = (params) => {
  return api.get('/system/logs', { params })
}

export const getSettings = () => {
  return api.get('/system/settings')
}

export const generateMockData = () => {
  return api.post('/system/mock/generate')
} 