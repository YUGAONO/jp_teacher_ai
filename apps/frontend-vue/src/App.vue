<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/counter'
import AppSidebar from '@/components/common/AppSidebar.vue'
import ExampleForm from '@/components/example/ExampleForm.vue'
import ExampleList from '@/components/example/ExampleList.vue'

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
            <br>
            単語とJLPTレベルを入力すると、例文を生成します。
          </div>
          
          <div v-else class="login-prompt">
            サイドバーからログインまたは新規登録を行ってください。
          </div>
        </header>
        
        <!-- 例文生成機能（ログイン済みの場合のみ表示） -->
        <div v-if="isAuthenticated" class="example-section">
          <ExampleForm />
          <ExampleList />
        </div>
        
        <!-- フッター情報 -->
        <!-- <footer v-if="isAuthenticated" class="page-footer">
          <div class="usage-info">
            <h3 class="usage-title">使用方法:</h3>
            <ol class="usage-list">
              <li>学習したい日本語の単語を入力</li>
              <li>目標のJLPTレベルを選択</li>
              <li>「例文を生成」ボタンをクリック</li>
            </ol>
          </div> -->
        <!-- </footer> -->
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
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
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

.example-section {
  margin-bottom: 3rem;
}

.page-footer {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #e0e0e0;
}

.usage-info {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.usage-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.usage-list {
  list-style: decimal;
  margin-left: 1.5rem;
  line-height: 1.6;
  color: #666;
}

.usage-list li {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
}
</style>
