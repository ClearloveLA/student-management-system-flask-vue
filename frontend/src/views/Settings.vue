<template>
  <div class="container py-4">
    <!-- 页面标题 -->
    <div class="header-section mb-4">
      <h2 class="text-primary mb-3">
        <i class="bi bi-gear-fill"></i> 系统设置
      </h2>
      <p class="text-muted">自定义您的系统偏好设置</p>
    </div>

    <div class="row g-4">
      <!-- 主题设置 -->
      <div class="col-md-6">
        <div class="settings-card">
          <div class="settings-card-header">
            <div class="icon-wrapper bg-primary">
              <i class="bi bi-palette"></i>
            </div>
            <h5>主题设置</h5>
          </div>
          <div class="settings-card-body">
            <div class="mb-4">
              <label class="form-label d-block">主题模式</label>
              <div class="theme-selector">
                <div class="theme-option" :class="{ active: theme === 'light' }" @click="theme = 'light'">
                  <div class="theme-preview light"></div>
                  <span>浅色</span>
                </div>
                <div class="theme-option position-relative" @click="showDarkModeToast">
                  <div class="theme-preview dark opacity-50"></div>
                  <span class="text-muted">深色</span>
                  <div class="coming-soon-badge">开发中</div>
                </div>
                <div class="theme-option position-relative" @click="showDarkModeToast">
                  <div class="theme-preview auto opacity-50"></div>
                  <span class="text-muted">跟随系统</span>
                  <div class="coming-soon-badge">开发中</div>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label">主题色</label>
              <div class="color-selector">
                <div class="color-option" 
                     v-for="color in themeColors" 
                     :key="color.value"
                     :class="{ active: primaryColor === color.value }"
                     :style="{ '--color': color.value }"
                     @click="primaryColor = color.value">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知设置 -->
      <div class="col-md-6">
        <div class="settings-card">
          <div class="settings-card-header">
            <div class="icon-wrapper bg-info">
              <i class="bi bi-bell"></i>
            </div>
            <h5>通知设置</h5>
          </div>
          <div class="settings-card-body">
            <div class="notification-setting">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 class="mb-1">邮件通知</h6>
                  <p class="text-muted mb-0 small">接收重要更新提醒的邮件</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" v-model="notifications.email">
                </div>
              </div>
            </div>
            <div class="notification-setting">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 class="mb-1">浏览器通知</h6>
                  <p class="text-muted mb-0 small">在浏览器中显示桌面通知</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" v-model="notifications.browser">
                </div>
              </div>
            </div>
            <div class="notification-setting">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">声音提醒</h6>
                  <p class="text-muted mb-0 small">收到通知时播放提示音</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" v-model="notifications.sound">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 安全设置 -->
      <div class="col-md-6">
        <div class="settings-card">
          <div class="settings-card-header">
            <div class="icon-wrapper bg-warning">
              <i class="bi bi-shield-lock"></i>
            </div>
            <h5>安全设置</h5>
          </div>
          <div class="settings-card-body">
            <div class="mb-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 class="mb-1">两步验证</h6>
                  <p class="text-muted mb-0 small">使用手机验证码进行双重认证</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" v-model="security.twoFactor">
                </div>
              </div>
            </div>
            <div class="mb-4">
              <h6 class="mb-3">登录设备</h6>
              <div class="device-list">
                <div class="device-item" v-for="device in loginDevices" :key="device.id">
                  <div class="device-info">
                    <i :class="device.icon"></i>
                    <div>
                      <div class="device-name">{{ device.name }}</div>
                      <small class="text-muted">{{ device.lastLogin }}</small>
                    </div>
                  </div>
                  <button class="btn btn-sm btn-outline-danger" @click="removeDevice(device.id)">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据设置 -->
      <div class="col-md-6">
        <div class="settings-card">
          <div class="settings-card-header">
            <div class="icon-wrapper bg-success">
              <i class="bi bi-database"></i>
            </div>
            <h5>数据设置</h5>
          </div>
          <div class="settings-card-body">
            <div class="mb-4">
              <h6 class="mb-3">数据备份</h6>
              <div class="backup-options">
                <div class="form-check mb-2">
                  <input class="form-check-input" type="radio" v-model="backup.frequency" value="daily">
                  <label class="form-check-label">每日备份</label>
                </div>
                <div class="form-check mb-2">
                  <input class="form-check-input" type="radio" v-model="backup.frequency" value="weekly">
                  <label class="form-check-label">每周备份</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" v-model="backup.frequency" value="monthly">
                  <label class="form-check-label">每月备份</label>
                </div>
              </div>
            </div>
            <div class="mb-3">
              <h6 class="mb-3">存储位置</h6>
              <select class="form-select" v-model="backup.location">
                <option value="local">本地存储</option>
                <option value="cloud">云端存储</option>
                <option value="both">本地+云端</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存按钮 -->
    <div class="save-settings">
      <button class="btn btn-primary" @click="saveSettings">
        <i class="bi bi-save"></i> 保存设置
      </button>
    </div>

    <!-- 添加 Toast 组件 -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div id="darkModeToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <i class="bi bi-info-circle me-2"></i>
          <strong class="me-auto">提示</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          深色模式正在开发中，敬请期待！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useThemeStore } from '../store/theme'

const themeStore = useThemeStore()

// 使用 store 中的值
const theme = computed({
  get: () => themeStore.theme,
  set: (value) => themeStore.theme = value
})

const primaryColor = computed({
  get: () => themeStore.primaryColor,
  set: (value) => themeStore.primaryColor = value
})

// 主题设置
const themeColors = [
  { name: '默认蓝', value: '#0d6efd' },
  { name: '翡翠绿', value: '#198754' },
  { name: '珊瑚红', value: '#dc3545' },
  { name: '琥珀黄', value: '#ffc107' },
  { name: '天空蓝', value: '#0dcaf0' },
  { name: '深紫色', value: '#6f42c1' }
]

// 通知设置
const notifications = ref({
  email: true,
  browser: false,
  sound: true
})

// 安全设置
const security = ref({
  twoFactor: false
})

// 登录设备列表
const loginDevices = ref([
  {
    id: 1,
    name: 'Chrome - Windows 10',
    icon: 'bi bi-windows',
    lastLogin: '今天 10:30'
  },
  {
    id: 2,
    name: 'Safari - iPhone 13',
    icon: 'bi bi-phone',
    lastLogin: '昨天 15:45'
  },
  {
    id: 3,
    name: 'Firefox - MacBook Pro',
    icon: 'bi bi-laptop',
    lastLogin: '2024-03-10 09:15'
  }
])

// 备份设置
const backup = ref({
  frequency: 'weekly',
  location: 'cloud'
})

// 移除设备
const removeDevice = (deviceId) => {
  if (confirm('确定要移除此设备吗？')) {
    loginDevices.value = loginDevices.value.filter(device => device.id !== deviceId)
  }
}

// 保存设置
const saveSettings = () => {
  // TODO: 调用保存API
  alert('设置已保存')
}

// 显示深色模式提示
const showDarkModeToast = () => {
  const toast = new bootstrap.Toast(document.getElementById('darkModeToast'))
  toast.show()
}
</script>

<style scoped>
.settings-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 100%;
}

.settings-card-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.icon-wrapper i {
  font-size: 1.5rem;
  margin: 0;
}

.settings-card-body {
  padding: 1.5rem;
}

.theme-selector {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.theme-option {
  text-align: center;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s;
}

.theme-option:hover {
  background: #f8f9fa;
}

.theme-option.active {
  background: #e9ecef;
}

.theme-preview {
  width: 80px;
  height: 50px;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  border: 2px solid #dee2e6;
}

.theme-preview.light {
  background: #ffffff;
}

.theme-preview.dark {
  background: #212529;
}

.theme-preview.auto {
  background: linear-gradient(to right, #ffffff 50%, #212529 50%);
}

.color-selector {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.color-option {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  background-color: var(--color);
  border: 2px solid transparent;
  transition: all 0.3s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #000;
}

.device-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.device-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.device-info i {
  font-size: 1.25rem;
  color: #6c757d;
}

.device-name {
  font-weight: 500;
}

.save-settings {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
}

.save-settings .btn {
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.notification-setting {
  padding: 1rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.notification-setting:hover {
  background-color: #f8f9fa;
}

.form-check-input {
  cursor: pointer;
}

@media (max-width: 768px) {
  .save-settings {
    position: static;
    margin-top: 2rem;
    text-align: center;
  }
}
</style> 