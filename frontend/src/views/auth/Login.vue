<template>
  <div class="auth-container">
    <div class="auth-wrapper">
      <div class="auth-card">
        <!-- 左侧装饰区域 -->
        <div class="auth-decoration">
          <div class="decoration-content">
            <i class="bi bi-mortarboard-fill"></i>
            <h2>学生管理系统</h2>
            <p>高效 · 便捷 · 智能</p>
          </div>
        </div>
        
        <!-- 右侧表单区域 -->
        <div class="auth-form">
          <div class="form-header">
            <h3>{{ isLogin ? '欢迎回来' : '创建账号' }}</h3>
            <p class="text-muted">
              {{ isLogin ? '很高兴再次见到您' : '请填写以下信息完成注册' }}
            </p>
          </div>
          
          <form @submit.prevent="handleSubmit">
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="form.username"
                placeholder="用户名"
                required
              >
              <label for="username">用户名</label>
            </div>
            
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="form.password"
                placeholder="密码"
                required
              >
              <label for="password">密码</label>
            </div>
            
            <template v-if="!isLogin">
              <div class="form-floating mb-3">
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  placeholder="确认密码"
                  required
                >
                <label for="confirmPassword">确认密码</label>
              </div>
              
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  placeholder="邮箱"
                  required
                >
                <label for="email">邮箱</label>
              </div>
            </template>
            
            <button 
              type="submit" 
              class="btn btn-primary w-100"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ isLogin ? '登录' : '注册' }}
            </button>
            
            <div class="form-footer">
              <p>
                {{ isLogin ? '还没有账号？' : '已有账号？' }}
                <router-link 
                  :to="isLogin ? '/register' : '/login'"
                  class="link-primary"
                >
                  {{ isLogin ? '立即注册' : '立即登录' }}
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, register } from '@/api/auth'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isLogin = computed(() => route.path === '/login')
const loading = ref(false)

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: ''
})

const handleSubmit = async () => {
  if (!isLogin.value && form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  try {
    loading.value = true
    if (isLogin.value) {
      const res = await login(form.value.username, form.value.password)
      if (res.access_token) {
        const userData = res.user || {
          id: res.id,
          username: form.value.username,
          email: res.email
        }
        userStore.login(res.access_token, userData)
        ElMessage.success('登录成功')
        router.push('/')
      }
    } else {
      await register({
        username: form.value.username,
        password: form.value.password,
        email: form.value.email
      })
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-wrapper {
  width: 100%;
  max-width: 900px;
}

.auth-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
}

.auth-decoration {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.decoration-content i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.decoration-content h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.decoration-content p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.auth-form {
  flex: 1;
  padding: 3rem;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h3 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.form-floating {
  margin-bottom: 1.5rem;
}

.form-control {
  border-radius: 10px;
  border: 1px solid #e1e8f0;
  padding: 0.75rem 1rem;
  height: auto;
  font-size: 1rem;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  background: #a5b4fc;
  transform: none;
}

.form-footer {
  text-align: center;
  margin-top: 2rem;
}

.link-primary {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.link-primary:hover {
  color: #764ba2;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .auth-card {
    flex-direction: column;
  }
  
  .auth-decoration {
    padding: 2rem;
  }
  
  .auth-form {
    padding: 2rem;
  }
  
  .decoration-content i {
    font-size: 3rem;
  }
  
  .decoration-content h2 {
    font-size: 1.5rem;
  }
}
</style> 