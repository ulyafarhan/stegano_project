<template>
  <nav class="flex flex-col space-y-2">
    <router-link
      v-for="item in navigation"
      :key="item.label"
      :to="item.to"
      class="flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-slate-700 hover:text-white"
      active-class="bg-indigo-500 text-white font-bold shadow-lg"
    >
      <i :class="item.icon" class="mr-3 text-lg"></i>
      <span>{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const navigation = ref([
  {
    label: 'Beranda',
    icon: 'pi pi-home',
    to: '/'
  },
  {
    label: 'Enkripsi & Sisipkan',
    icon: 'pi pi-lock',
    to: '/encode'
  },
  {
    label: 'Ekstrak & Dekripsi',
    icon: 'pi pi-key',
    to: '/decode'
  },
  {
    label: 'Tentang',
    icon: 'pi pi-info-circle',
    to: '/about'
  }
])
</script>