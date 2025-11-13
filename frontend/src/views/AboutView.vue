<template>
  <div class="text-white">
    <h1 class="text-4xl font-bold mb-4">Tentang VertexGuard</h1>
    <p class="text-lg text-slate-300 mb-8">
      Aplikasi steganografi modern yang menggabungkan keamanan enkripsi dan kepraktisan
      penyembunyian data.
    </p>

    <div class="bg-slate-900 p-8 rounded-lg shadow-lg space-y-6">
      <div>
        <h2 class="text-2xl font-bold text-indigo-400 mb-3">Misi Kami</h2>
        <p class="text-slate-300">
          Misi kami adalah menyediakan alat yang mudah digunakan namun kuat untuk melindungi privasi
          dan kerahasiaan informasi. Di era digital saat ini, VertexGuard hadir sebagai solusi
          untuk komunikasi yang aman melalui media sehari-hari.
        </p>
      </div>

      <div>
        <h2 class="text-2xl font-bold text-indigo-400 mb-3">Teknologi yang Digunakan</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="bg-slate-800 p-4 rounded-lg">
            <h3 class="font-bold text-lg mb-2">Frontend</h3>
            <ul class="list-disc list-inside text-slate-300 space-y-1">
              <li>Vue.js 3 (Composition API)</li>
              <li>Vite</li>
              <li>Tailwind CSS</li>
              <li>PrimeVue</li>
            </ul>
          </div>
          <div class="bg-slate-800 p-4 rounded-lg">
            <h3 class="font-bold text-lg mb-2">Backend</h3>
            <ul class="list-disc list-inside text-slate-300 space-y-1">
              <li>FastAPI (Python)</li>
              <li>Caesar Cipher (mod 256)</li>
              <li>Berbagai Pustaka Steganografi</li>
            </ul>
          </div>
        </div>
      </div>

      <div>
        <h2 class="text-2xl font-bold text-indigo-400 mb-3">Kontak</h2>
        <p class="text-slate-300">
          Proyek ini dikembangkan oleh [Nama Anda/Tim Anda]. Untuk pertanyaan atau kolaborasi,
          silakan hubungi kami di [email protected]
        </p>
      </div>
    </div>
  </div>
</template>