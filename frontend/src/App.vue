<template>
  <div class="flex h-screen bg-slate-800">
    <Toast position="bottom-right" />

    <aside class="w-64 bg-slate-900 text-white shadow-lg z-10 border-r border-slate-700">
      <div class="p-5">
        <h1 class="text-2xl font-bold text-indigo-400 mb-8">VertexGuard</h1>
        <Sidebar />
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto p-8 bg-slate-800">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style>
@import './assets/main.css';
</style>