<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h1 class="text-xl font-bold text-white">JP Teacher AI</h1>
    </div>
    
    <!-- ナビゲーションメニュー -->
    <div v-if="isAuthenticated" class="navigation-section">
      <h3 class="text-lg font-semibold text-white mb-3">メニュー</h3>
      <nav class="nav-menu">
        <router-link to="/words" class="nav-link" active-class="nav-link-active">
          📚 単語PDF生成
        </router-link>
        <router-link to="/examples" class="nav-link" active-class="nav-link-active">
          📝 例文生成
        </router-link>
      </nav>
    </div>
    
    <!-- 未ログイン時 -->
    <div v-if="!isAuthenticated" class="auth-section">
      <h2 class="text-lg font-semibold text-white mb-4">ログイン・新規登録</h2>
      
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
    
    <!-- ログイン済み時 -->
    <div v-else class="user-section">
      <h2 class="text-lg font-semibold text-white mb-4">ユーザー情報</h2>
      
      <div class="user-profile-tabs">
        <button
          :class="['tab-button', { active: activeProfileTab === 'profile' }]"
          @click="activeProfileTab = 'profile'"
        >
          プロフィール
        </button>
        <button
          :class="['tab-button', { active: activeProfileTab === 'settings' }]"
          @click="activeProfileTab = 'settings'"
        >
          設定
        </button>
      </div>
      
      <div class="tab-content">
        <div v-if="activeProfileTab === 'profile'" class="profile-info">
          <div class="user-info-card">
            <p><strong>👤 {{ user?.display_name || 'ユーザー' }}</strong></p>
            <p>📧 {{ user?.email || '' }}</p>
            <p>🌐 言語: {{ user?.locale || 'ja' }}</p>
            <p>📋 プラン: {{ user?.current_plan || 'free' }}</p>
          </div>
          
          <button
            @click="refreshProfile"
            :disabled="isLoading"
            class="refresh-button"
          >
            <span v-if="isLoading">更新中...</span>
            <span v-else">最新の情報を取得</span>
          </button>
        </div>
        
        <div v-if="activeProfileTab === 'settings'" class="profile-settings">
          <ProfileSettings />
        </div>
      </div>
      
      <div class="logout-section">
        <button
          @click="handleLogout"
          :disabled="isLoading"
          class="logout-button"
        >
          <span v-if="isLoading">ログアウト中...</span>
          <span v-else">ログアウト</span>
        </button>
      </div>
    </div>
    
    <div class="footer">
      <p class="text-sm text-gray-300">© 2024 JP Teacher AI</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/counter'
import LoginForm from '@/components/auth/LoginForm.vue'
import SignupForm from '@/components/auth/SignupForm.vue'
import ProfileSettings from '@/components/auth/ProfileSettings.vue'

const authStore = useAuthStore()
const { user, isAuthenticated, isLoading } = storeToRefs(authStore)

const activeTab = ref<'login' | 'signup'>('login')
const activeProfileTab = ref<'profile' | 'settings'>('profile')

const refreshProfile = async () => {
  const result = await authStore.getProfile()
  if (!result.success) {
    alert(result.message)
  }
}

const handleLogout = async () => {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.navigation-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-link {
  display: block;
  padding: 0.75rem 1rem;
  color: white;
  text-decoration: none;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-link-active {
  background-color: rgba(255, 255, 255, 0.3) !important;
  font-weight: 600;
}

.auth-section,
.user-section {
  flex: 1;
  margin-bottom: 2rem;
}

.auth-tabs,
.user-profile-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-button {
  flex: 1;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.tab-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.tab-button.active {
  background-color: rgba(255, 255, 255, 0.3);
}

.tab-content {
  margin-top: 1rem;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-info-card {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.user-info-card p {
  color: white;
  margin-bottom: 0.5rem;
}

.refresh-button,
.logout-button {
  width: 100%;
  padding: 0.75rem;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.refresh-button:hover,
.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.refresh-button:disabled,
.logout-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.logout-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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