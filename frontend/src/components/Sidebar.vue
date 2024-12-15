<template>
  <div class="sidebar bg-dark">
    <div class="sidebar-header">
      <h3 class="text-light mb-0">学生管理系统</h3>
    </div>
    <ul class="nav flex-column">
      <li class="nav-item" v-for="item in menuItems" :key="item.path">
        <router-link 
          :to="item.path" 
          class="nav-link"
          :class="{ active: $route.path === item.path }"
        >
          <i :class="`bi ${item.icon}`"></i>
          <span>{{ item.text }}</span>
        </router-link>
      </li>
    </ul>
    <div class="sidebar-footer">
      <div class="nav flex-column">
        <router-link to="/profile" class="nav-link">
          <i class="bi bi-person-circle"></i>
          <span>个人信息</span>
        </router-link>
        <a href="#" class="nav-link" @click.prevent="handleLogout">
          <i class="bi bi-box-arrow-right"></i>
          <span>退出登录</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { logout } from '@/api/auth'

const router = useRouter()

// 菜单配置
const menuItems = [
  {
    path: '/',
    icon: 'bi-people',
    text: '学生管理'
  },
  {
    path: '/statistics',
    icon: 'bi-bar-chart',
    text: '数据统计'
  },
  {
    path: '/logs',
    icon: 'bi-clock-history',
    text: '操作日志'
  },
  {
    path: '/settings',
    icon: 'bi-gear',
    text: '系统设置'
  }
]

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await logout()
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
      ElMessage.error('退出登录失败')
    }
  }
}
</script>

<style scoped>
.sidebar {
  height: 100vh;
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.8rem 1rem;
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  color: #fff;
  background: var(--primary-color);
}

.nav-link i {
  font-size: 1.2rem;
  margin-right: 0.5rem;
  width: 1.5rem;
  text-align: center;
}

.sidebar-footer {
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-footer .nav-link {
  padding: 0.5rem 1rem;
}
</style> 