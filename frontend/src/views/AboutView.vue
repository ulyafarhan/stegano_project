<template>
  <div class="text-white max-w-5xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 mt-12 sm:mt-16 mb-12">
    <header class="text-center mb-12 sm:mb-16">
      <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
        <span class="bg-gradient-to-r from-indigo-400 to-purple-500 text-transparent bg-clip-text">
          Tentang VertexGuard
        </span>
      </h1>
      <p class="text-base sm:text-lg text-slate-400 max-w-3xl mx-auto">
        Aplikasi steganografi modern yang menggabungkan keamanan enkripsi kelas industri dengan kepraktisan penyembunyian data.
      </p>
    </header>

    <div class="bg-slate-900 p-6 sm:p-8 rounded-2xl shadow-2xl border border-slate-800 space-y-12">
      
      <div>
        <h2 class="text-2xl sm:text-3xl font-bold text-indigo-400 mb-4">Misi Kami</h2>
        <p class="text-slate-300/90 leading-relaxed text-base">
          Misi kami adalah menyediakan alat yang mudah digunakan namun kuat untuk melindungi privasi dan kerahasiaan informasi. Di era digital saat ini, VertexGuard hadir sebagai solusi untuk komunikasi yang aman melalui media sehari-hari.
        </p>
      </div>

      <div>
        <h2 class="text-2xl sm:text-3xl font-bold text-indigo-400 mb-6">Fitur Utama</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Feature Card 1 -->
          <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/80 h-full flex flex-col">
            <div class="mb-4 p-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 w-fit">
              <i class="pi pi-shield text-2xl text-emerald-400"></i>
            </div>
            <h3 class="font-bold text-lg text-white mb-2">Enkripsi AES-256</h3>
            <p class="text-sm text-slate-400 leading-relaxed">
              Payload diamankan menggunakan AES-256 (CBC), standar emas dalam kriptografi, dengan kunci dari password Anda.
            </p>
          </div>
          <!-- Feature Card 2 -->
          <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/80 h-full flex flex-col">
            <div class="mb-4 p-3 rounded-full bg-sky-500/10 border border-sky-500/20 w-fit">
              <i class="pi pi-box text-2xl text-sky-400"></i>
            </div>
            <h3 class="font-bold text-lg text-white mb-2">Steganografi Universal</h3>
            <p class="text-sm text-slate-400 leading-relaxed">
              Menyisipkan data ke hampir semua jenis file (PNG, JPG, PDF, dll.) tanpa merusak file asli menggunakan metode EOF.
            </p>
          </div>
          <!-- Feature Card 3 -->
          <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/80 h-full flex flex-col">
            <div class="mb-4 p-3 rounded-full bg-purple-500/10 border border-purple-500/20 w-fit">
              <i class="pi pi-desktop text-2xl text-purple-400"></i>
            </div>
            <h3 class="font-bold text-lg text-white mb-2">Antarmuka Modern</h3>
            <p class="text-sm text-slate-400 leading-relaxed">
              Dibangun dengan Vue 3, Vite, dan Tailwind CSS. Dirancang agar responsif, intuitif, dan mudah digunakan.
            </p>
          </div>
        </div>
      </div>

      <div>
        <h2 class="text-2xl sm:text-3xl font-bold text-indigo-400 mb-6">Teknologi yang Digunakan</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/80">
            <h3 class="font-bold text-lg mb-4 text-slate-200">Frontend</h3>
            <ul class="space-y-3 text-sm">
              <li class="flex items-center gap-3"><i class="pi pi-code text-slate-500"></i><span class="text-slate-300">Vue.js 3 (Composition API)</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-code text-slate-500"></i><span class="text-slate-300">Vite (Build Tool)</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-code text-slate-500"></i><span class="text-slate-300">Tailwind CSS</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-code text-slate-500"></i><span class="text-slate-300">PrimeVue (Komponen UI)</span></li>
            </ul>
          </div>
          <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/80">
            <h3 class="font-bold text-lg mb-4 text-slate-200">Backend</h3>
            <ul class="space-y-3 text-sm">
              <li class="flex items-center gap-3"><i class="pi pi-server text-slate-500"></i><span class="text-slate-300">FastAPI (Python)</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-server text-slate-500"></i><span class="text-slate-300">PyCryptodome (Kriptografi)</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-server text-slate-500"></i><span class="text-slate-300">Metode EOF Steganography</span></li>
              <li class="flex items-center gap-3"><i class="pi pi-server text-slate-500"></i><span class="text-slate-300">Uvicorn (ASGI Server)</span></li>
            </ul>
          </div>
        </div>
      </div>

      <div>
        <h2 class="text-2xl sm:text-3xl font-bold text-indigo-400 mb-4">Peringatan & Praktik Terbaik</h2>
        <div class="bg-yellow-500/10 border border-yellow-500/30 text-yellow-200 p-5 sm:p-6 rounded-xl flex items-start gap-4">
          <i class="pi pi-exclamation-triangle text-2xl text-yellow-400 mt-1 flex-shrink-0"></i>
          <div>
            <h3 class="font-bold text-white mb-2">Risiko Metode EOF (End-of-File)</h3>
            <p class="text-sm text-yellow-200/90 leading-relaxed">
              Metode ini menyisipkan data di akhir file host. Meskipun universal, data tersembunyi akan <strong>HILANG</strong> jika file host dibuka dan disimpan ulang oleh editor media (misalnya, Photoshop, editor metadata audio, dll.).
            </p>
            <h4 class="font-semibold text-white mt-4 mb-2">Praktik Terbaik:</h4>
            <ul class="list-disc list-inside text-sm text-yellow-200/90 leading-relaxed space-y-1">
              <li>Selalu gunakan file host yang sudah final dan <strong>jangan mengeditnya kembali</strong> setelah data disisipkan.</li>
              <li>Perlakukan file yang sudah terisi data sebagai <strong>read-only</strong> (hanya-baca).</li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
// No script needed for this view
</script>