import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 主题模式
  const theme = ref(localStorage.getItem('theme') || 'light')
  // 主题色
  const primaryColor = ref(localStorage.getItem('primaryColor') || '#0d6efd')

  // 监听系统主题变化
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
  const handleSystemThemeChange = () => {
    if (theme.value === 'auto') {
      document.documentElement.setAttribute('data-theme', prefersDark.matches ? 'dark' : 'light')
    }
  }
  prefersDark.addEventListener('change', handleSystemThemeChange)

  // 监听主题变化
  watch(theme, (newTheme) => {
    localStorage.setItem('theme', newTheme)
    if (newTheme === 'auto') {
      handleSystemThemeChange()
    } else {
      document.documentElement.setAttribute('data-theme', newTheme)
    }
  })

  // 监听主题色变化
  watch(primaryColor, (newColor) => {
    localStorage.setItem('primaryColor', newColor)
    document.documentElement.style.setProperty('--primary-color', newColor)
    // 生成不同深浅的主题色
    const color = newColor.substring(1) // 移除#
    const r = parseInt(color.substring(0, 2), 16)
    const g = parseInt(color.substring(2, 4), 16)
    const b = parseInt(color.substring(4, 6), 16)
    
    // 生成浅色变体
    document.documentElement.style.setProperty(
      '--primary-light',
      `rgba(${r}, ${g}, ${b}, 0.1)`
    )
    // 生成深色变体
    document.documentElement.style.setProperty(
      '--primary-dark',
      `rgb(${Math.max(0, r - 30)}, ${Math.max(0, g - 30)}, ${Math.max(0, b - 30)})`
    )
  })

  return {
    theme,
    primaryColor
  }
}) 