<template>
  <div class="text-white">
    <h1 class="text-4xl font-bold mb-4">Selamat Datang di VertexGuard</h1>
    <p class="text-lg text-slate-300 mb-8">
      Platform steganografi modern untuk menyembunyikan dan mengekstrak data rahasia Anda dengan
      aman.
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-slate-900 p-6 rounded-lg">
        <h2 class="text-2xl font-bold text-indigo-400 mb-4">Enkripsi & Sisipkan</h2>
        <p class="text-slate-300 mb-4">
          Sembunyikan pesan atau file rahasia Anda di dalam file media seperti gambar, audio, atau
          video.
        </p>
        <router-link
          to="/encode"
          class="inline-block bg-indigo-500 text-white px-6 py-2 rounded-md hover:bg-indigo-600 transition-colors"
          >Mulai Enkripsi</router-link
        >
      </div>

      <div class="bg-slate-900 p-6 rounded-lg">
        <h2 class="text-2xl font-bold text-indigo-400 mb-4">Ekstrak & Dekripsi</h2>
        <p class="text-slate-300 mb-4">
          Ekstrak dan dekripsi pesan atau file rahasia dari file media yang telah dimodifikasi.
        </p>
        <router-link
          to="/decode"
          class="inline-block bg-indigo-500 text-white px-6 py-2 rounded-md hover:bg-indigo-600 transition-colors"
          >Mulai Dekripsi</router-link
        >
      </div>
    </div>
  </div>
</template>