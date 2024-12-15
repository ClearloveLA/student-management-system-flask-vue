<template>
  <div class="container-fluid mt-4">
    <!-- 标题和筛选区域 -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="mb-0">
            <i class="bi bi-clock-history"></i> 操作日志
          </h4>
          <div class="d-flex gap-2">
            <select class="form-select" v-model="filterType">
              <option value="">所有操作类型</option>
              <option value="LOGIN">登录</option>
              <option value="LOGOUT">登出</option>
              <option value="ADD_STUDENT">添加学生</option>
              <option value="DELETE_STUDENT">删除学生</option>
              <option value="GENERATE_DATA">生成数据</option>
            </select>
            <button class="btn btn-outline-secondary" @click="refreshLogs">
              <i class="bi bi-arrow-clockwise"></i> 刷新
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 日志列表 -->
    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>时间</th>
              <th>用户</th>
              <th>操作类型</th>
              <th>操作描述</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="logs.length">
              <tr v-for="log in logs" :key="log.id">
                <td class="text-nowrap">{{ formatDate(log.created_at) }}</td>
                <td>
                  <span class="badge bg-primary">{{ log.username }}</span>
                </td>
                <td>
                  <span :class="getOperationTypeClass(log.operation_type)">
                    {{ getOperationTypeText(log.operation_type) }}
                  </span>
                </td>
                <td>{{ log.operation_desc }}</td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="4" class="text-center py-4">
                <div class="text-muted">
                  <i class="bi bi-inbox fs-2"></i>
                  <p class="mt-2">暂无操作日志</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="card-footer d-flex justify-content-between align-items-center">
        <div class="text-muted">
          共 {{ total }} 条记录
        </div>
        <nav v-if="totalPages > 1">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="handlePageChange(currentPage - 1)">
                上一页
              </a>
            </li>
            <li 
              v-for="page in displayPages" 
              :key="page"
              class="page-item"
              :class="{ active: currentPage === page }"
            >
              <a class="page-link" href="#" @click.prevent="handlePageChange(page)">
                {{ page }}
              </a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="handlePageChange(currentPage + 1)">
                下一页
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getLogs } from '@/api/log'

// 状态
const logs = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const filterType = ref('')
const loading = ref(false)

// 操作类型映射
const operationTypes = {
  LOGIN: { text: '登录', class: 'badge bg-success' },
  LOGOUT: { text: '登出', class: 'badge bg-secondary' },
  ADD_STUDENT: { text: '添加学生', class: 'badge bg-primary' },
  DELETE_STUDENT: { text: '删除学生', class: 'badge bg-danger' },
  GENERATE_DATA: { text: '生成数据', class: 'badge bg-info' }
}

// 获取操作类型显示文本
const getOperationTypeText = (type) => {
  return operationTypes[type]?.text || type
}

// 获取操作类型样式
const getOperationTypeClass = (type) => {
  return operationTypes[type]?.class || 'badge bg-secondary'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})

// 计算显示的页码范围
const displayPages = computed(() => {
  const delta = 2 // 当前页前后显示的��码数
  let start = Math.max(1, currentPage.value - delta)
  let end = Math.min(totalPages.value, currentPage.value + delta)
  
  if (end - start < 2 * delta) {
    if (start === 1) {
      end = Math.min(start + 2 * delta, totalPages.value)
    } else {
      start = Math.max(1, end - 2 * delta)
    }
  }
  
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

// 加载日志数据
const loadLogs = async () => {
  try {
    loading.value = true
    const data = await getLogs({
      page: currentPage.value,
      per_page: pageSize.value,
      operation_type: filterType.value
    })
    logs.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('加载日志失败:', error)
    ElMessage.error('加载日志失败')
  } finally {
    loading.value = false
  }
}

// 刷新日志
const refreshLogs = () => {
  currentPage.value = 1
  loadLogs()
}

// 处理页码变化
const handlePageChange = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadLogs()
}

// 监听筛选条件变化
watch(filterType, () => {
  currentPage.value = 1
  loadLogs()
})

// 初始化
onMounted(() => {
  loadLogs()
})
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table th {
  font-weight: 600;
  white-space: nowrap;
}

.table td {
  vertical-align: middle;
}

.badge {
  font-weight: 500;
  padding: 0.5em 0.75em;
}

.form-select {
  min-width: 150px;
}

.pagination {
  margin-bottom: 0;
}

.page-link {
  padding: 0.375rem 0.75rem;
}

.page-item.active .page-link {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}
</style> 