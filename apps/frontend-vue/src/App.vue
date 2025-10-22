<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/counter'
import AppSidebar from '@/components/common/AppSidebar.vue'

const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)

// Initialize auth on app startup
onMounted(() => {
  authStore.initializeAuth()
})
</script>

<template>
  <div id="app" class="app-container">
    <AppSidebar />
    
    <main class="main-content">
      <div class="content-wrapper">
        <header class="page-header">
          <div v-if="isAuthenticated" class="user-greeting">
            こんにちは、{{ user?.display_name || 'ユーザー' }}さん！
          </div>
          
          <div v-else class="login-prompt">
            サイドバーからログインまたは新規登録を行ってください。
          </div>
        </header>
        
        <!-- ルータービューで画面を切り替え -->
        <div v-if="isAuthenticated" class="router-view-container">
          <RouterView />
        </div>
        
        <div v-else class="login-required">
          <div class="login-card">
            <h3>ログインが必要です</h3>
            <p>PDF生成機能を使用するには、サイドバーからログインしてください。</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.user-greeting {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.login-prompt {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #2196f3;
}

.router-view-container {
  margin-bottom: 3rem;
}

.login-required {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.login-card {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
}

.login-card h3 {
  color: #333;
  margin-bottom: 1rem;
}

.login-card p {
  color: #666;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .content-wrapper {
    max-width: 100%;
  }
}
</style>
