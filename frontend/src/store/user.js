import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))
  const token = ref(localStorage.getItem('token') || '')

  const isAuthenticated = computed(() => !!token.value)
  const avatarUrl = computed(() => 
    `https://ui-avatars.com/api/?name=${userInfo.value?.username || 'U'}&background=random`
  )

  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const login = (newToken, info) => {
    setToken(newToken)
    setUserInfo(info)
  }

  const logout = () => {
    userInfo.value = {}
    token.value = ''
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
  }

  return {
    userInfo,
    token,
    isAuthenticated,
    avatarUrl,
    setUserInfo,
    setToken,
    login,
    logout
  }
}) 