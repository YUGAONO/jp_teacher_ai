import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authService } from '@/services'
import type { User, LoginRequest, SignupRequest, UpdateProfileRequest } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  
  const isAuthenticated = computed(() => !!user.value && !!token.value)

  // Initialize from localStorage
  const initializeAuth = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
      } catch (error) {
        console.error('Failed to parse stored user:', error)
        clearAuth()
      }
    }
  }

  const saveToStorage = (authData: { access_token: string; user: User }) => {
    localStorage.setItem('access_token', authData.access_token)
    localStorage.setItem('user', JSON.stringify(authData.user))
  }

  const clearAuth = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  const login = async (credentials: LoginRequest) => {
    try {
      isLoading.value = true
      const response = await authService.login(credentials)
      
      user.value = response.user
      token.value = response.access_token
      saveToStorage(response)
      
      return { success: true, message: 'ログインしました！' }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'ログインに失敗しました' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const signup = async (userData: SignupRequest) => {
    try {
      isLoading.value = true
      const response = await authService.signup(userData)
      
      user.value = response.user
      token.value = response.access_token
      saveToStorage(response)
      
      return { success: true, message: 'アカウントが正常に作成されました！' }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '登録に失敗しました' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await authService.logout()
      }
      clearAuth()
      return { success: true, message: 'ログアウトしました' }
    } catch (error: any) {
      clearAuth() // Clear local state even if API call fails
      return { 
        success: false, 
        message: error.response?.data?.detail || 'ログアウト中にエラーが発生しました' 
      }
    }
  }

  const getProfile = async () => {
    try {
      const profile = await authService.getProfile()
      if (user.value) {
        user.value = {
          ...user.value,
          display_name: profile.display_name,
          locale: profile.locale,
          current_plan: profile.current_plan
        }
        localStorage.setItem('user', JSON.stringify(user.value))
      }
      return { success: true, data: profile }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'プロフィール取得に失敗しました' 
      }
    }
  }

  const updateProfile = async (updates: UpdateProfileRequest) => {
    try {
      const updatedProfile = await authService.updateProfile(updates)
      if (user.value) {
        user.value = {
          ...user.value,
          display_name: updatedProfile.display_name,
          locale: updatedProfile.locale,
          current_plan: updatedProfile.current_plan
        }
        localStorage.setItem('user', JSON.stringify(user.value))
      }
      return { success: true, message: 'プロフィールが更新されました！' }
    } catch (error: any) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'プロフィール更新に失敗しました' 
      }
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    initializeAuth,
    login,
    signup,
    logout,
    getProfile,
    updateProfile
  }
})
