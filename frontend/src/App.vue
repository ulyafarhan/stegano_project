<template>
  <div class="flex h-screen bg-slate-800 overflow-hidden">
    <Toast position="top-center" />

    <!-- Mobile Header dengan responsivitas lebih baik -->
    <div class="lg:hidden fixed top-0 left-0 right-0 bg-slate-900 border-b border-slate-700 z-30 px-3 sm:px-4 py-2 sm:py-3 flex items-center justify-between shadow-md">
      <div class="flex items-center gap-2 sm:gap-3">
        <button @click="isSidebarOpen = !isSidebarOpen" class="text-slate-300 hover:text-white focus:outline-none transition-colors p-2 rounded-lg hover:bg-slate-800">
          <i class="pi pi-bars text-lg sm:text-xl"></i>
        </button>
        <h1 class="text-base sm:text-lg md:text-xl font-bold text-indigo-400">VertexGuard</h1>
      </div>
    </div>

    <!-- Overlay untuk mobile dengan transisi -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/50 z-20 lg:hidden backdrop-blur-sm transition-opacity duration-300"
    ></div>

    <!-- Sidebar dengan ukuran responsif -->
    <aside 
      class="fixed lg:static inset-y-0 left-0 z-30 w-72 sm:w-64 bg-slate-900 text-white shadow-xl border-r border-slate-700 transform transition-transform duration-300 ease-in-out lg:translate-x-0"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-4 sm:p-5 h-full overflow-y-auto">
        <h1 class="text-xl sm:text-2xl font-bold text-indigo-400 mb-6 sm:mb-8 hidden lg:block">VertexGuard</h1>
        
        <div class="lg:hidden flex justify-end mb-3 sm:mb-4">
          <button @click="isSidebarOpen = false" class="text-slate-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-slate-800">
            <i class="pi pi-times text-lg sm:text-xl"></i>
          </button>
        </div>

        <Sidebar @click="closeSidebarOnMobile" />
      </div>
    </aside>

    <!-- Main Content dengan padding responsif -->
    <main class="flex-1 overflow-y-auto bg-slate-800 relative w-full">
      <div class="p-3 sm:p-4 md:p-6 lg:p-8 min-h-full" :class="{ 'pt-12 sm:pt-16 md:pt-20 lg:pt-8': true }">
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