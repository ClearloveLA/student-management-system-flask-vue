import { api } from './base'

// 获取学生列表
export const getStudents = (params) => {
  return api.get('students', { params })
}

// 添加学生
export const addStudent = (data) => {
  return api.post('students', data)
}

// 更新学生信息
export const updateStudent = (id, data) => {
  return api.put(`students/${id}`, data)
}

// 删除学生
export const deleteStudent = (id) => {
  return api.delete(`students/${id}`)
}

// 获取学生统计数据
export const getStudentStats = () => {
  return api.get('students/stats')
}

// 添加生成数据的方法
export const generateMockData = () => {
  return api.post('students/generate')
} 