<template>
  <div class="text-white max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mt-16 sm:mt-20 mb-20">
    <header class="mb-12 sm:mb-16 text-center">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold mb-4 tracking-tight">
        <span class="bg-gradient-to-r from-indigo-400 to-purple-500 text-transparent bg-clip-text">
          PrivaSel Steganography
        </span>
      </h1>
      <p class="text-base sm:text-lg text-slate-400 max-w-3xl mx-auto">
        Platform steganografi modern untuk menyembunyikan dan mengekstrak data rahasia Anda dengan aman menggunakan enkripsi AES-256 yang kuat.
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
      <!-- Encode Card -->
      <router-link
        to="/encode"
        class="group relative bg-slate-900 p-6 sm:p-8 rounded-2xl shadow-2xl border border-slate-800 hover:border-indigo-500/50 transition-all duration-300 transform hover:-translate-y-1 flex flex-col overflow-hidden"
      >
        <div class="absolute -top-1 -right-1 w-24 h-24 bg-indigo-600/20 blur-3xl group-hover:w-32 group-hover:h-32 transition-all duration-300"></div>
        <div class="flex-grow z-10">
          <div class="mb-4 p-3 rounded-full bg-indigo-500/10 border border-indigo-500/20 w-fit">
            <i class="pi pi-lock text-2xl text-indigo-400"></i>
          </div>
          <h2 class="text-2xl sm:text-3xl font-bold text-slate-100 mb-3">
            Enkripsi & Sisipkan
          </h2>
          <p class="text-slate-400 mb-6 text-sm sm:text-base leading-relaxed">
            Amankan file atau pesan teks Anda, lalu sembunyikan di dalam file media apa pun (gambar, audio, PDF, dll).
          </p>
        </div>
        <div class="mt-auto z-10">
          <span class="font-semibold text-indigo-400 flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
            Mulai Enkripsi
            <i class="pi pi-arrow-right"></i>
          </span>
        </div>
      </router-link>

      <!-- Decode Card -->
      <router-link
        to="/decode"
        class="group relative bg-slate-900 p-6 sm:p-8 rounded-2xl shadow-2xl border border-slate-800 hover:border-emerald-500/50 transition-all duration-300 transform hover:-translate-y-1 flex flex-col overflow-hidden"
      >
        <div class="absolute -top-1 -right-1 w-24 h-24 bg-emerald-600/20 blur-3xl group-hover:w-32 group-hover:h-32 transition-all duration-300"></div>
        <div class="flex-grow z-10">
          <div class="mb-4 p-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 w-fit">
            <i class="pi pi-key text-2xl text-emerald-400"></i>
          </div>
          <h2 class="text-2xl sm:text-3xl font-bold text-slate-100 mb-3">
            Ekstrak & Dekripsi
          </h2>
          <p class="text-slate-400 mb-6 text-sm sm:text-base leading-relaxed">
            Buka kembali file media yang telah dimodifikasi untuk mengekstrak dan mendekripsi data rahasia Anda.
          </p>
        </div>
        <div class="mt-auto z-10">
          <span class="font-semibold text-emerald-400 flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
            Mulai Dekripsi
            <i class="pi pi-arrow-right"></i>
          </span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No script needed for this view
</script>

<style scoped>
/* Styles are handled by Tailwind CSS classes */
</style>