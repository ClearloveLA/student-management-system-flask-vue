<template>
  <div class="wrapper">
    <!-- 侧边栏 -->
    <nav id="sidebar" :class="{ active: !sidebarOpen }" v-if="userStore.isAuthenticated">
      <div class="sidebar-header">
        <h3><i class="bi bi-mortarboard-fill"></i> 学生管理</h3>
      </div>

      <ul class="list-unstyled components">
        <li :class="{ active: $route.path === '/' }">
          <router-link to="/">
            <i class="bi bi-people-fill"></i> 学生列表
          </router-link>
        </li>
        <li :class="{ active: $route.path === '/statistics' }">
          <router-link to="/statistics">
            <i class="bi bi-bar-chart-fill"></i> 数据统计
          </router-link>
        </li>
        <li :class="{ active: $route.path === '/logs' }">
          <router-link to="/logs">
            <i class="bi bi-clock-history"></i> 操作日志
          </router-link>
        </li>
        <li :class="{ active: $route.path === '/settings' }">
          <router-link to="/settings">
            <i class="bi bi-gear-fill"></i> 系统设置
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- 页面内容 -->
    <div id="content">
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary" v-if="userStore.isAuthenticated">
        <div class="container-fluid">
          <button type="button" class="btn btn-primary" @click="toggleSidebar">
            <i class="bi bi-list"></i>
          </button>
          <span class="navbar-brand ms-3">学生信息管理系统</span>
          
          <!-- 用户信息下拉菜单 -->
          <div class="ms-auto">
            <div class="dropdown">
              <div class="user-profile" 
                   data-bs-toggle="dropdown" 
                   data-bs-auto-close="outside"
                   role="button"
                   aria-expanded="false">
                <img :src="userStore.avatarUrl" 
                     :alt="userStore.userInfo?.username"
                     class="avatar">
                <span class="username ms-2">{{ userStore.userInfo?.username }}</span>
                <i class="bi bi-chevron-down ms-2"></i>
              </div>
              <ul class="dropdown-menu dropdown-menu-end animate slideIn">
                <li class="dropdown-header">
                  <div class="d-flex align-items-center">
                    <img :src="userStore.avatarUrl" 
                         :alt="userStore.userInfo?.username"
                         class="avatar-sm">
                    <div class="ms-2">
                      <div class="fw-bold">{{ userStore.userInfo?.username }}</div>
                      <small class="text-muted">{{ userStore.userInfo?.email }}</small>
                    </div>
                  </div>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <router-link class="dropdown-item" to="/profile">
                    <i class="bi bi-person-circle"></i> 个人信息
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/settings">
                    <i class="bi bi-gear"></i> 系统设置
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
                    <i class="bi bi-box-arrow-right"></i> 退出登录
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </nav>

      <div class="content-body">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './store/user'

const router = useRouter()
const userStore = useUserStore()
const sidebarOpen = ref(true)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const handleLogout = async () => {
  try {
    // TODO: 调用登出API
    userStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('登出失败:', error)
  }
}
</script>

<style>
.wrapper {
  display: flex;
  width: 100%;
  min-height: 100vh;
}

#sidebar {
  width: 250px;
  background: #343a40;
  color: #fff;
  transition: all 0.3s;
}

#sidebar.active {
  margin-left: -250px;
}

.sidebar-header {
  padding: 20px;
  background: #2c3136;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

#sidebar ul li a {
  padding: 15px 20px;
  display: block;
  color: #fff;
  text-decoration: none;
}

#sidebar ul li a:hover {
  background: #2c3136;
}

#sidebar ul li.active > a {
  background: #2c3136;
}

#content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-body {
  padding: 20px;
  flex: 1;
  background: #f8f9fa;
}

.navbar .btn-primary {
  padding: 0.25rem 0.5rem;
}

.bi {
  margin-right: 8px;
}

.dropdown-item .bi {
  width: 16px;
  text-align: center;
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  cursor: pointer;
  color: white;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.avatar-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-weight: 500;
}

.dropdown-header {
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.dropdown-menu {
  min-width: 280px;
  padding: 0;
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  border-radius: 0.5rem;
}

.dropdown-item {
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dropdown-item i {
  font-size: 1.1rem;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.text-danger:hover {
  background-color: #dc3545;
  color: white !important;
}

/* 下拉菜单动画 */
.animate {
  animation-duration: 0.3s;
  animation-fill-mode: both;
}

@keyframes slideIn {
  from {
    transform: translateY(1rem);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slideIn {
  animation-name: slideIn;
}

/* 确保下拉菜单在悬停时保持显示 */
.dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown {
  margin-right: 55px;
}
</style>