<template>
  <div class="container">
    <!-- 搜索和筛选区域 -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <div class="input-group">
              <span class="input-group-text">
                <i class="bi bi-search"></i>
              </span>
              <input 
                type="text" 
                class="form-control" 
                v-model="searchQuery"
                @input="handleFilterChange"
                placeholder="搜索姓名/学号/电话/班级"
              >
            </div>
          </div>
          <div class="col-md-2">
            <select class="form-select" v-model="selectedMajor" @change="handleMajorChange">
              <option value="">所有专业</option>
              <option v-for="major in majors" :key="major" :value="major">
                {{ major }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select" v-model="selectedClass" @change="handleFilterChange">
              <option value="">所有班级</option>
              <option v-for="className in availableClasses" :key="className" :value="className">
                {{ className }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select" v-model="selectedGender" @change="handleFilterChange">
              <option value="">所有性别</option>
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="col-md-3">
            <button class="btn btn-primary me-2" @click="showAddDialog">
              <i class="bi bi-plus-lg"></i> 添加学生
            </button>
            <button 
              class="btn btn-success" 
              @click="handleGenerateMock"
              :loading="generating"
            >
              <i class="bi bi-database-fill"></i> 生成模拟数据
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- 学生列表表格 -->
    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>学号</th>
                <th>姓名</th>
                <th>性别</th>
                <th>年龄</th>
                <th>班级</th>
                <th>联系电话</th>
                <th>邮箱</th>
                <th>入学日期</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in tableData.data" :key="student.id">
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>
                  <span :class="student.gender === '男' ? 'text-primary' : 'text-danger'">
                    <i :class="student.gender === '男' ? 'bi bi-gender-male' : 'bi bi-gender-female'"></i>
                    {{ student.gender }}
                  </span>
                </td>
                <td>{{ student.age }}</td>
                <td>{{ student.class_name }}</td>
                <td>{{ student.phone }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.enrollment_date }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="handleEdit(student)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="handleDelete(student)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- 添加分页器 -->
          <div class="d-flex justify-content-between align-items-center mt-4">
            <div class="text-muted">
              共 {{ tableData.total }} 条记录
            </div>
            <div class="d-flex align-items-center">
              <select class="form-select me-3" style="width: auto;" v-model="pageSize" @change="handlePageSizeChange">
                <option :value="10">10条/页</option>
                <option :value="20">20条/页</option>
                <option :value="50">50条/页</option>
                <option :value="100">100条/页</option>
              </select>
              <div class="d-flex align-items-center me-3">
                <span class="me-2">跳转到</span>
                <input 
                  type="number" 
                  class="form-control" 
                  style="width: 70px;"
                  v-model="jumpToPage"
                  min="1"
                  :max="tableData.totalPages"
                >
                <button 
                  class="btn btn-outline-primary ms-2"
                  @click="handleJumpToPage"
                >
                  跳转
                </button>
              </div>
              <nav aria-label="Page navigation">
                <ul class="pagination mb-0">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <a class="page-link" href="#" @click.prevent="handlePageChange(1)">
                      <i class="bi bi-chevron-double-left"></i>
                    </a>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <a class="page-link" href="#" @click.prevent="handlePageChange(currentPage - 1)">
                      <i class="bi bi-chevron-left"></i>
                    </a>
                  </li>
                  <li class="page-item" v-for="page in displayPages" :key="page"
                      :class="{ active: currentPage === page }">
                    <a class="page-link" href="#" @click.prevent="handlePageChange(page)">{{ page }}</a>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === tableData.totalPages }">
                    <a class="page-link" href="#" @click.prevent="handlePageChange(currentPage + 1)">
                      <i class="bi bi-chevron-right"></i>
                    </a>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === tableData.totalPages }">
                    <a class="page-link" href="#" @click.prevent="handlePageChange(tableData.totalPages)">
                      <i class="bi bi-chevron-double-right"></i>
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑学生对话框 -->
    <div class="modal fade" id="studentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ dialogTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleSubmit" id="studentForm" class="needs-validation" novalidate>
              <div class="mb-3">
                <label class="form-label">姓名 <span class="text-danger">*</span></label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="form.name" 
                  required
                  pattern="^[\u4e00-\u9fa5]{2,10}$"
                  :class="{ 'is-invalid': formErrors.name }"
                >
                <div class="invalid-feedback">
                  请输入2-10个汉字的姓名
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">性别 <span class="text-danger">*</span></label>
                <select 
                  class="form-select" 
                  v-model="form.gender" 
                  required
                  :class="{ 'is-invalid': formErrors.gender }"
                >
                  <option value="">请选择性别</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
                <div class="invalid-feedback">请选择性别</div>
              </div>

              <div class="mb-3">
                <label class="form-label">年龄 <span class="text-danger">*</span></label>
                <input 
                  type="number" 
                  class="form-control" 
                  v-model="form.age" 
                  min="16" 
                  max="30" 
                  required
                  :class="{ 'is-invalid': formErrors.age }"
                >
                <div class="invalid-feedback">年龄必须在16-30岁之间</div>
              </div>

              <div class="mb-3">
                <label class="form-label">专业 <span class="text-danger">*</span></label>
                <select 
                  class="form-select" 
                  v-model="form.major" 
                  required
                  :class="{ 'is-invalid': formErrors.major }"
                  @change="handleFormMajorChange"
                >
                  <option value="">请选择专业</option>
                  <option v-for="major in majors" :key="major" :value="major">
                    {{ major }}
                  </option>
                </select>
                <div class="invalid-feedback">请选择专业</div>
              </div>

              <div class="mb-3">
                <label class="form-label">班级 <span class="text-danger">*</span></label>
                <select 
                  class="form-select" 
                  v-model="form.class_name" 
                  required
                  :class="{ 'is-invalid': formErrors.class_name }"
                  :disabled="!form.major"
                >
                  <option value="">请选择班级</option>
                  <option v-for="className in formAvailableClasses" :key="className" :value="className">
                    {{ className }}
                  </option>
                </select>
                <div class="invalid-feedback">请选择班级</div>
              </div>

              <div class="mb-3">
                <label class="form-label">联系电话 <span class="text-danger">*</span></label>
                <input 
                  type="tel" 
                  class="form-control" 
                  v-model="form.phone" 
                  required
                  pattern="^1[3-9]\d{9}$"
                  :class="{ 'is-invalid': formErrors.phone }"
                >
                <div class="invalid-feedback">请输入正确的11位手机号码</div>
              </div>

              <div class="mb-3">
                <label class="form-label">邮箱 <span class="text-danger">*</span></label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="form.email" 
                  required
                  pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
                  :class="{ 'is-invalid': formErrors.email }"
                >
                <div class="invalid-feedback">请输入正确的邮箱地址</div>
              </div>

              <div class="mb-3">
                <label class="form-label">地址</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="form.address"
                  maxlength="100"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">入学日期 <span class="text-danger">*</span></label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="form.enrollment_date" 
                  required
                  :class="{ 'is-invalid': formErrors.enrollment_date }"
                >
                <div class="invalid-feedback">请选择入学日期</div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="handleSubmit">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStudents, addStudent, updateStudent, deleteStudent, generateMockData } from '@/api/student'

// 从 mockDataGenerator 导入班级列表
const CLASS_LIST = {
  '应用': ['应用22301班', '应用22302班', '应用22303班', '应用22304班', '应用22305班'],
  '安全': ['安全22301班', '安全22302班', '安全22303班', '安全22304班'],
  '工软': ['工软22301班', '工软22302班'],
  '公网': ['工网22301班']
}

// 搜索和筛选
const searchQuery = ref('')
const selectedClass = ref('')
const selectedGender = ref('')
const selectedMajor = ref('')

// 可用班级列表（��据选择的专业动态变化）
const availableClasses = computed(() => {
  if (!selectedMajor.value) {
    return Object.values(CLASS_LIST).flat()
  }
  return CLASS_LIST[selectedMajor.value] || []
})

// 专业列表
const majors = Object.keys(CLASS_LIST)

// 分页和筛选状态
const currentPage = ref(1)
const pageSize = ref(10)
const jumpToPage = ref(1)

// 表格数据
const tableData = ref({
  data: [],
  total: 0,
  loading: false
})

// 表单相关
const modal = ref(null)
const dialogTitle = ref('添加学生')
const form = ref({
  name: '',
  gender: '',
  age: 18,
  major: '',
  class_name: '',
  phone: '',
  email: '',
  address: '',
  enrollment_date: ''
})

// 表单错误状态
const formErrors = ref({
  name: false,
  gender: false,
  age: false,
  major: false,
  class_name: false,
  phone: false,
  email: false,
  enrollment_date: false
})

// 表单可用班级列表
const formAvailableClasses = computed(() => {
  if (!form.value.major) {
    return []
  }
  return CLASS_LIST[form.value.major] || []
})

// 处理表单中专业变化
const handleFormMajorChange = () => {
  form.value.class_name = '' // 清空班级选择
}

// 监听筛选条件变化
const handleFilterChange = () => {
  currentPage.value = 1 // 重置到第一页
  loadTableData()
}

// 处理专���变化
const handleMajorChange = () => {
  selectedClass.value = '' // 清空班级选择
  handleFilterChange()
}

// 加载表格数据
const loadTableData = async () => {
  tableData.value.loading = true
  try {
    // 打印当前token
    console.log('Current token:', localStorage.getItem('token'))
    
    const result = await getStudents({
      page: currentPage.value,
      per_page: pageSize.value,
      keyword: searchQuery.value,
      major: selectedMajor.value,
      class_name: selectedClass.value,
      gender: selectedGender.value
    })
    
    console.log('Students response:', result)  // 添加调试日志
    
    tableData.value = {
      data: result.items,
      total: result.total,
      totalPages: result.pages,
      loading: false
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
    tableData.value.loading = false
  }
}

// 初始化
onMounted(() => {
  modal.value = new Modal(document.getElementById('studentModal'))
  loadTableData()
})

// 显示添加对话框
const showAddDialog = () => {
  dialogTitle.value = '添加学生'
  form.value = {
    name: '',
    gender: '',
    age: 18,
    major: '',
    class_name: '',
    phone: '',
    email: '',
    address: '',
    enrollment_date: new Date().toISOString().split('T')[0]
  }
  // 重置错误状态
  Object.keys(formErrors.value).forEach(key => {
    formErrors.value[key] = false
  })
  modal.value.show()
}

// 显示编辑对话框
const handleEdit = (student) => {
  dialogTitle.value = '编辑学生'
  // 从班级名称中提取专业
  const major = Object.keys(CLASS_LIST).find(key => 
    CLASS_LIST[key].includes(student.class_name)
  )
  form.value = { 
    ...student,
    major
  }
  // 重置错误状态
  Object.keys(formErrors.value).forEach(key => {
    formErrors.value[key] = false
  })
  modal.value.show()
}

// 处理删除
const handleDelete = async (student) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除学生 ${student.name} 的信息吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await deleteStudent(student.id)
    ElMessage.success('删除成功')
    loadTableData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 验证表单
const validateForm = () => {
  let isValid = true
  const errors = {
    name: false,
    gender: false,
    age: false,
    major: false,
    class_name: false,
    phone: false,
    email: false,
    enrollment_date: false
  }

  // 姓名验证：2-10个汉字
  if (!/^[\u4e00-\u9fa5]{2,10}$/.test(form.value.name)) {
    errors.name = true
    isValid = false
  }

  // 性别验证
  if (!form.value.gender) {
    errors.gender = true
    isValid = false
  }

  // 年龄验证：16-30岁
  const age = parseInt(form.value.age)
  if (isNaN(age) || age < 16 || age > 30) {
    errors.age = true
    isValid = false
  }

  // 专业和班级验证
  if (!form.value.major) {
    errors.major = true
    isValid = false
  }
  if (!form.value.class_name) {
    errors.class_name = true
    isValid = false
  }

  // 手机号验证：11位数字，以1开头
  if (!/^1[3-9]\d{9}$/.test(form.value.phone)) {
    errors.phone = true
    isValid = false
  }

  // 邮箱验证
  if (!/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(form.value.email)) {
    errors.email = true
    isValid = false
  }

  // 入学日期验证
  if (!form.value.enrollment_date) {
    errors.enrollment_date = true
    isValid = false
  }

  formErrors.value = errors
  return isValid
}

// 处理表单提交
const handleSubmit = async () => {
  if (!validateForm()) {
    ElMessage.warning('请检查表单填写是否正确')
    return
  }

  try {
    const submitData = {
      ...form.value,
      // 移除表单中的 major 字段，因为后端不需要
      major: undefined,
      // 确保日期格式正确
      enrollment_date: form.value.enrollment_date
    }

    if (dialogTitle.value === '添加学生') {
      await addStudent(submitData)
      ElMessage.success('添加成功')
    } else {
      await updateStudent(submitData.id, submitData)
      ElMessage.success('编辑成功')
    }
    
    modal.value.hide()
    loadTableData()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error(error.response?.data?.message || '操作失败')
  }
}

// 添加计算属性：显示的页码范围
const displayPages = computed(() => {
  const totalPages = tableData.value.totalPages || 1
  const current = currentPage.value
  const delta = 2 // 当前页前后显示页码数
  
  let start = Math.max(1, current - delta)
  let end = Math.min(totalPages, current + delta)
  
  // 调整起始页码，确保始终显示 2*delta+1 个页码（如果有足够的页数）
  if (end - start < 2 * delta) {
    if (start === 1) {
      end = Math.min(start + 2 * delta, totalPages)
    } else {
      start = Math.max(1, end - 2 * delta)
    }
  }
  
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

// 添加分页处理函数
const handlePageChange = (page) => {
  if (page < 1 || page > tableData.value.totalPages) return
  currentPage.value = page
  loadTableData()
}

// 添加每页显示数量变化处理函数
const handlePageSizeChange = () => {
  currentPage.value = 1 // 重置到第一页
  loadTableData()
}

// 添加页码跳转处理函数
const handleJumpToPage = () => {
  if (jumpToPage.value < 1 || jumpToPage.value > tableData.value.totalPages) return
  currentPage.value = jumpToPage.value
  loadTableData()
}

// 生成模拟数据
const generating = ref(false)
const handleGenerateMock = async () => {
  try {
    generating.value = true
    await ElMessageBox.confirm(
      '这将清空现有数据并生成新的模拟数据，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await generateMockData()
    ElMessage.success(res.message)
    loadTableData()  // 重新加载数据
  } catch (error) {
    if (error !== 'cancel') {
      console.error('生成数据失败:', error)
      ElMessage.error('生成数据失败')
    }
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.table th {
  white-space: nowrap;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
}

.bi {
  font-size: 1rem;
}

/* 添加分页相关样式 */
.pagination {
  margin-bottom: 0;
}

.page-link {
  padding: 0.375rem 0.75rem;
}

.page-item.active .page-link {
  background-color: var(--primary-color, #0d6efd);
  border-color: var(--primary-color, #0d6efd);
}

.page-link:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-select:focus {
  border-color: var(--primary-color, #0d6efd);
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* 禁用状态样式 */
.page-item.disabled .page-link {
  pointer-events: none;
  background-color: #e9ecef;
  border-color: #dee2e6;
}
</style>