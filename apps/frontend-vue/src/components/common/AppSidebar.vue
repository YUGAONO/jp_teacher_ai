<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h1 class="text-2xl font-bold text-gray-800">Teachify</h1>
      
      <!-- User Profile Button (when authenticated) -->
      <div v-if="isAuthenticated" class="user-profile-button">
        <button 
          @click="showUserPopup = !showUserPopup"
          class="profile-trigger"
        >
          <span class="user-icon">👤</span>
          <span class="user-name">{{ user?.display_name || 'ユーザー' }}</span>
          <span class="dropdown-arrow">▼</span>
        </button>
        
        <!-- User Info Popup -->
        <div v-if="showUserPopup" class="user-popup" @click.stop>
          <div class="popup-header">
            <h3>{{ user?.display_name || 'ユーザー' }}</h3>
          </div>
          
          <div class="popup-section">
            <div class="popup-item">
              <span class="label">プラン設定</span>
            </div>
          </div>
          
          <div class="popup-divider"></div>
          
          <div class="popup-section">
            <div class="popup-item">
              <span class="label">{{ user?.email || '' }}</span>
            </div>
          </div>
          
          <div class="popup-divider"></div>
          
          <div class="popup-section">
            <button @click="handleLogout" class="logout-popup-button">
              ログアウト
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- ナビゲーションメニュー -->
    <div v-if="isAuthenticated" class="navigation-section">
      <h3 class="text-lg font-semibold text-gray-700 mb-3">メニュー</h3>
      <nav class="nav-menu">
        <router-link to="/words" class="nav-link" active-class="nav-link-active">
          📚 新規作成
        </router-link>
      </nav>
    </div>
    
    <!-- 未ログイン時 -->
    <div v-if="!isAuthenticated" class="auth-section">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">ログイン・新規登録</h2>
      
      <div class="auth-tabs">
        <button
          :class="['tab-button', { active: activeTab === 'login' }]"
          @click="activeTab = 'login'"
        >
          ログイン
        </button>
        <button
          :class="['tab-button', { active: activeTab === 'signup' }]"
          @click="activeTab = 'signup'"
        >
          新規登録
        </button>
      </div>
      
      <div class="tab-content">
        <LoginForm v-if="activeTab === 'login'" />
        <SignupForm v-if="activeTab === 'signup'" />
      </div>
    </div>
    
    <div class="footer">
      <p class="text-sm text-gray-500">© 2024 JP Teacher AI</p>
    </div>
  </div>
  
  <!-- Backdrop for popup -->
  <div v-if="showUserPopup" class="popup-backdrop" @click="showUserPopup = false"></div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/counter'
import LoginForm from '@/components/auth/LoginForm.vue'
import SignupForm from '@/components/auth/SignupForm.vue'

const authStore = useAuthStore()
const { user, isAuthenticated, isLoading } = storeToRefs(authStore)

const activeTab = ref<'login' | 'signup'>('login')
const showUserPopup = ref(false)

const handleLogout = async () => {
  showUserPopup.value = false
  const result = await authStore.logout()
  if (!result.success) {
    alert(result.message)
  }
}
</script>

<style scoped>
.sidebar {
  width: 350px;
  height: 100vh;
  background: #f8f9fa;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e9ecef;
}

.sidebar-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
  position: relative;
}

.user-profile-button {
  position: relative;
  margin-top: 1rem;
}

.profile-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.profile-trigger:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.user-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.user-name {
  flex: 1;
  text-align: left;
  color: #495057;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 0.8rem;
  color: #6c757d;
}

.user-popup {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow: hidden;
  margin-top: 0.25rem;
}

.popup-header {
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.popup-header h3 {
  margin: 0;
  color: #495057;
  font-size: 1rem;
  font-weight: 600;
}

.popup-section {
  padding: 0.5rem 0;
}

.popup-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.popup-item:hover {
  background: #f8f9fa;
}

.popup-item .label {
  color: #495057;
  font-size: 0.9rem;
}

.popup-divider {
  height: 1px;
  background: #e9ecef;
}

.logout-popup-button {
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  color: #dc3545;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: left;
}

.logout-popup-button:hover {
  background: #f8f9fa;
}

.popup-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
}

.navigation-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-link {
  display: block;
  padding: 0.75rem 1rem;
  color: #495057;
  text-decoration: none;
  border-radius: 0.5rem;
  transition: all 0.2s;
  background-color: white;
  border: 1px solid #dee2e6;
  font-weight: 500;
}

.nav-link:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
}

.nav-link-active {
  background-color: #e3f2fd !important;
  border-color: #2196f3 !important;
  color: #1976d2 !important;
  font-weight: 600;
}

.auth-section {
  flex: 1;
  margin-bottom: 2rem;
}

.auth-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-button {
  flex: 1;
  padding: 0.5rem;
  background-color: white;
  color: #495057;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-button:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
}

.tab-button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.tab-content {
  margin-top: 1rem;
}

.footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
  text-align: center;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    max-height: 80vh;
  }
}
</style>