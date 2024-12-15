import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/styles/themes.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')

const theme = localStorage.getItem('theme') || 'light'
if (theme === 'auto') {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
  document.documentElement.setAttribute('data-theme', prefersDark.matches ? 'dark' : 'light')
} else {
  document.documentElement.setAttribute('data-theme', theme)
}

const primaryColor = localStorage.getItem('primaryColor') || '#0d6efd'
document.documentElement.style.setProperty('--primary-color', primaryColor)