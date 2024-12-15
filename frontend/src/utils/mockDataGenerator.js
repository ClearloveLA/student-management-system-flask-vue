// 更新班级列表
const CLASS_LIST = {
  '应用': ['应用22301班', '应用22302班', '应用22303班', '应用22304班', '应用22305班'],
  '安全': ['安全22301班', '安全22302班', '安全22303班', '安全22304班'],
  '工软': ['工软22301班', '工软22302班'],
  '公网': ['工网22301班']
}

// 扩展姓名库
const surnames = [
  '张', '李', '王', '赵', '刘', '陈', '杨', '黄', '周', '吴',
  '郑', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗',
  '郝', '邓', '冯', '陆', '梁', '崔', '谢', '徐', '曹', '叶',
  '韩', '许', '傅', '沈', '曾', '彭', '吕', '苏', '卢', '蒋'
]

const names = [
  '伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '洋',
  '艳', '勇', '军', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
  '平', '刚', '桂英', '文', '辉', '建华', '玲', '红', '晶', '华',
  '玉兰', '萍', '志强', '建国', '建军', '建平', '建华', '国强', '国平', '国华',
  '建', '国', '华', '玉', '明', '红', '英', '志', '春', '秀',
  '杰', '涛', '莉', '桂', '文', '峰', '军', '燕', '冰', '玲',
  '凯', '浩', '楠', '婷', '琳', '雪', '璐', '宇', '晨', '瑞'
]

// 生成随机数据的工具函数
const generateRandomStudent = (id) => {
  const gender = Math.random() > 0.5 ? '男' : '女'
  const name = surnames[Math.floor(Math.random() * surnames.length)] + 
               names[Math.floor(Math.random() * names.length)]
  const age = Math.floor(Math.random() * 4) + 18  // 18-21岁

  const cities = ['北京市', '上海市', '广州市', '深圳市', '成都市', '杭州市', '武汉市', '南京市', '西安市', '重庆市']
  const districts = ['海淀区', '朝阳区', '浦东新区', '天河区', '南山区', '武侯区', '江干区', '洪山区', '玄武区', '雁塔区']

  const city = cities[Math.floor(Math.random() * cities.length)]
  const district = districts[Math.floor(Math.random() * districts.length)]

  return {
    id: `2024${String(id).padStart(4, '0')}`,
    name,
    gender,
    age,
    class_name: '', // 这里先留空，在生成过程中分配
    phone: `138${String(Math.floor(Math.random() * 52000000)).padStart(8, '0')}`,
    email: `student${id}@example.com`,
    address: `${city}${district}`,
    enrollment_date: '2024-03-01'
  }
}

// 生成指定数量的学生数据
export const generateStudents = (count = 520) => {
  // 计算每个班级的基础人数
  const classList = Object.values(CLASS_LIST).flat()
  const baseStudentsPerClass = Math.floor(count / classList.length)
  const remainder = count % classList.length
  
  // 为每个班级分配学生数量
  const classAllocation = classList.reduce((acc, className, index) => {
    // 将余数分配给前几个班级
    acc[className] = baseStudentsPerClass + (index < remainder ? 1 : 0)
    return acc
  }, {})

  // 生成学生数据
  let students = []
  let currentId = 1

  // 按照分配的数量生成每个班级的学生
  Object.entries(classAllocation).forEach(([className, studentCount]) => {
    for (let i = 0; i < studentCount; i++) {
      const student = generateRandomStudent(currentId)
      student.class_name = className // 确保学生被分配到正确的班级
      students.push(student)
      currentId++
    }
  })

  // 随机打乱学生顺序
  return students.sort(() => Math.random() - 0.5)
}

// 统计数据
export const getStatistics = (students) => {
  const total = students.length
  const genderCount = {
    male: students.filter(s => s.gender === '男').length,
    female: students.filter(s => s.gender === '女').length
  }
  
  // 按班级统计
  const classCount = students.reduce((acc, student) => {
    acc[student.class_name] = (acc[student.class_name] || 0) + 1
    return acc
  }, {})

  // 按年龄统计
  const ageCount = students.reduce((acc, student) => {
    acc[student.age] = (acc[student.age] || 0) + 1
    return acc
  }, {})

  // 按地区统计（取城市）
  const cityCount = students.reduce((acc, student) => {
    const city = student.address.substring(0, 3)
    acc[city] = (acc[city] || 0) + 1
    return acc
  }, {})

  return {
    total,
    genderCount,
    classCount,
    ageCount,
    cityCount
  }
}

// 获取或生成学生数据
export const getOrGenerateStudents = (count = 520) => {
  // 尝试从 localStorage 获取数据
  const savedStudents = localStorage.getItem('mockStudents')
  if (savedStudents) {
    return JSON.parse(savedStudents)
  }

  // 如果没有保存的数据，生成新数据并保存
  const students = generateStudents(count)
  localStorage.setItem('mockStudents', JSON.stringify(students))
  return students
}

// 添加、更新、删除学生数据的辅助函数
export const mockStudentAPI = {
  // 获取分页数据
  getStudents: (page = 1, pageSize = 10, filters = {}) => {
    const students = JSON.parse(localStorage.getItem('mockStudents') || '[]')
    
    // 增强的筛选逻辑
    let filteredStudents = students.filter(student => {
      let match = true
      
      // 搜索关键词匹配多个字段
      if (filters.keyword) {
        const keyword = filters.keyword.toLowerCase()
        const searchFields = [
          student.name,
          student.id,
          student.phone,
          student.email,
          student.class_name,
          student.address
        ]
        match = searchFields.some(field => 
          String(field).toLowerCase().includes(keyword)
        )
      }

      // 专业筛选
      if (filters.major) {
        match = match && student.class_name.startsWith(filters.major)
      }

      // 班级筛选
      if (filters.class_name) {
        match = match && student.class_name === filters.class_name
      }

      // 性别筛选
      if (filters.gender) {
        match = match && student.gender === filters.gender
      }

      return match
    })

    // 排序
    if (filters.sortBy) {
      filteredStudents.sort((a, b) => {
        const direction = filters.sortOrder === 'desc' ? -1 : 1
        return direction * String(a[filters.sortBy]).localeCompare(String(b[filters.sortBy]))
      })
    }

    // 计算分页
    const total = filteredStudents.length
    const start = (page - 1) * pageSize
    const end = start + pageSize
    const data = filteredStudents.slice(start, end)

    return {
      data,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize)
    }
  },

  // 添加学生
  addStudent: (student) => {
    const students = JSON.parse(localStorage.getItem('mockStudents') || '[]')
    const newId = `2024${String(students.length + 1).padStart(4, '0')}`
    const newStudent = {
      ...student,
      id: newId,
      enrollment_date: new Date().toISOString().split('T')[0]
    }
    students.push(newStudent)
    localStorage.setItem('mockStudents', JSON.stringify(students))
    return newStudent
  },

  // 更新学生
  updateStudent: (id, data) => {
    const students = JSON.parse(localStorage.getItem('mockStudents') || '[]')
    const index = students.findIndex(s => s.id === id)
    if (index !== -1) {
      students[index] = { ...students[index], ...data }
      localStorage.setItem('mockStudents', JSON.stringify(students))
      return students[index]
    }
    throw new Error('Student not found')
  },

  // 删除学生
  deleteStudent: (id) => {
    const students = JSON.parse(localStorage.getItem('mockStudents') || '[]')
    const newStudents = students.filter(s => s.id !== id)
    localStorage.setItem('mockStudents', JSON.stringify(newStudents))
    return true
  },

  // 批量删除
  batchDelete: (ids) => {
    const students = JSON.parse(localStorage.getItem('mockStudents') || '[]')
    const newStudents = students.filter(s => !ids.includes(s.id))
    localStorage.setItem('mockStudents', JSON.stringify(newStudents))
    return true
  }
} 