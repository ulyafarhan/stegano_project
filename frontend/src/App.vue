<template>
  <div class="flex h-screen bg-slate-800 overflow-hidden">
    <Toast position="top-center" />

    <div class="lg:hidden fixed top-0 left-0 right-0 bg-slate-900 border-b border-slate-700 z-30 px-4 py-3 flex items-center justify-between shadow-md">
      <div class="flex items-center gap-3">
        <button @click="isSidebarOpen = !isSidebarOpen" class="text-slate-300 hover:text-white focus:outline-none">
          <i class="pi pi-bars text-2xl"></i>
        </button>
        <h1 class="text-xl font-bold text-indigo-400">VertexGuard</h1>
      </div>
    </div>

    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/50 z-20 lg:hidden backdrop-blur-sm transition-opacity"
    ></div>

    <aside 
      class="fixed lg:static inset-y-0 left-0 z-30 w-64 bg-slate-900 text-white shadow-xl border-r border-slate-700 transform transition-transform duration-300 ease-in-out lg:translate-x-0"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-5 h-full overflow-y-auto">
        <h1 class="text-2xl font-bold text-indigo-400 mb-8 hidden lg:block">VertexGuard</h1>
        
        <div class="lg:hidden flex justify-end mb-4">
          <button @click="isSidebarOpen = false" class="text-slate-400 hover:text-white">
            <i class="pi pi-times text-xl"></i>
          </button>
        </div>

        <Sidebar @click="closeSidebarOnMobile" />
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto bg-slate-800 relative w-full">
      <div class="p-4 pt-20 lg:p-8 lg:pt-8 min-h-full">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'

const isSidebarOpen = ref(false)

// Helper agar sidebar menutup otomatis saat menu diklik di mobile
const closeSidebarOnMobile = () => {
  if (window.innerWidth < 1024) { // 1024px adalah breakpoint 'lg' tailwind
    isSidebarOpen.value = false
  }
}
</script>

<style>
@import './assets/main.css';
</style>