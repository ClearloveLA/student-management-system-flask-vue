<template>
  <div class="container-fluid mt-4">
    <div class="row justify-content-center">
      <!-- 左侧个人信息卡片 -->
      <div class="col-md-4 mb-4">
        <div class="profile-card">
          <div class="profile-header">
            <div class="avatar-wrapper">
              <div class="avatar">
                <span>{{ profile.username?.[0]?.toUpperCase() || 'U' }}</span>
              </div>
            </div>
            <h4 class="mt-3">{{ profile.username }}</h4>
            <p class="text-muted">{{ profile.role }}</p>
          </div>
          <div class="profile-info">
            <div class="info-item">
              <i class="bi bi-envelope"></i>
              <span>{{ profile.email }}</span>
            </div>
            <div class="info-item">
              <i class="bi bi-calendar"></i>
              <span>注册于 {{ formatDate(profile.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧表单区域 -->
      <div class="col-md-6">
        <!-- 修改邮箱表单 -->
        <div class="form-card mb-4">
          <div class="form-card-header">
            <h5><i class="bi bi-person-gear"></i> 修改个人信息</h5>
          </div>
          <div class="form-card-body">
            <form @submit.prevent="handleUpdateProfile">
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="profile.email"
                  required
                >
                <label for="email">邮箱地址</label>
              </div>
              <button type="submit" class="btn btn-primary w-100">
                <i class="bi bi-check-lg"></i> 保存修改
              </button>
            </form>
          </div>
        </div>

        <!-- 修改密码表单 -->
        <div class="form-card">
          <div class="form-card-header">
            <h5><i class="bi bi-shield-lock"></i> 修改密码</h5>
          </div>
          <div class="form-card-body">
            <form @submit.prevent="handleChangePassword">
              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  id="oldPassword"
                  v-model="passwordForm.old_password"
                  required
                >
                <label for="oldPassword">当前密码</label>
              </div>
              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  id="newPassword"
                  v-model="passwordForm.new_password"
                  required
                >
                <label for="newPassword">新密码</label>
              </div>
              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="passwordForm.confirm_password"
                  required
                >
                <label for="confirmPassword">确认新密码</label>
              </div>
              <button type="submit" class="btn btn-warning w-100">
                <i class="bi bi-key"></i> 修改密码
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserProfile, updateUserProfile, changePassword } from '@/api/user'

const profile = ref({
  username: '',
  email: '',
  role: '',
  created_at: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 加载用户信息
const loadProfile = async () => {
  try {
    const data = await getUserProfile()
    profile.value = data
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  }
}

// 更新个人信息
const handleUpdateProfile = async () => {
  try {
    await updateUserProfile({
      email: profile.value.email
    })
    ElMessage.success('更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.message || '更新失败')
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  try {
    await changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    ElMessage.success('密码修改成功')
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error(error.response?.data?.message || '密码修改失败')
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.profile-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, #4a90e2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.avatar-wrapper {
  margin: 0 auto;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  padding: 3px;
  background: rgba(255, 255, 255, 0.2);
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar span {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--primary-color);
}

.profile-info {
  padding: 1.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.info-item i {
  width: 24px;
  margin-right: 0.5rem;
  color: var(--primary-color);
}

.form-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.form-card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  background: #f8f9fa;
}

.form-card-header h5 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #495057;
}

.form-card-body {
  padding: 1.5rem;
}

.form-floating > .form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.25rem rgba(var(--primary-color-rgb), 0.25);
}

.btn {
  padding: 0.75rem 1.5rem;
  font-weight: 500;
}

.btn i {
  margin-right: 0.5rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .profile-card {
    margin-bottom: 1.5rem;
  }
}
</style> 