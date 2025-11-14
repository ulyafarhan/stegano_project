<template>
  <div class="text-white max-w-5xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 mt-12 sm:mt-16 mb-12">
    <header class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-white mb-2">Ekstrak & Dekripsi Data</h1>
      <p class="text-slate-400 text-sm sm:text-base">Ambil kembali pesan rahasia Anda dari media digital.</p>
    </header>

    <div class="bg-slate-900 p-4 sm:p-6 md:p-8 rounded-2xl shadow-2xl border border-slate-800">
      <form @submit.prevent="handleDecode">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <!-- Left side: Instructions and Host File Dropzone -->
          <div class="lg:col-span-7 space-y-8">
            <div class="bg-indigo-500/10 border border-indigo-500/20 p-4 rounded-xl">
              <div class="flex items-start gap-3">
                <i class="pi pi-info-circle text-indigo-400 text-xl mt-0.5"></i>
                <div class="text-sm text-slate-300">
                  <p class="font-semibold text-indigo-300 mb-1">Bagaimana cara kerjanya?</p>
                  <p class="opacity-90">Upload file media (Gambar, PDF, Audio, dll.) yang sudah disisipi pesan. Sistem akan mengekstrak isinya dan memberikannya kepada Anda sebagai file unduhan.</p>
                </div>
              </div>
            </div>

            <FileDropZone
              label="1. File Media Terenkripsi (Host)"
              icon="pi pi-lock-open"
              v-model:file="hostFile"
              :required="true"
            />
          </div>

          <!-- Right side: Security Key and Decryption -->
          <div class="lg:col-span-5">
            <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-md sticky top-24">
              <h3 class="text-lg font-semibold mb-6 text-indigo-400 flex items-center gap-3">
                <i class="pi pi-key"></i>
                <span>2. Kunci Keamanan & Proses</span>
              </h3>
              
              <div class="space-y-6">
                <div>
                  <label class="font-medium block mb-2 text-slate-300">Password Dekripsi</label>
                  <Password
                    v-model="key"
                    placeholder="Masukkan password rahasia"
                    :feedback="false"
                    toggleMask
                    class="w-full"
                    inputClass="w-full p-3 bg-slate-900 border-2 border-slate-700 rounded-lg text-white font-mono focus:border-indigo-500 focus:outline-none transition-colors"
                  />
                  <p class="text-xs text-slate-500 mt-2 leading-tight flex items-start gap-2">
                    <i class="pi pi-exclamation-triangle text-yellow-500/80 mt-0.5"></i>
                    <span>Password harus <strong>sama persis</strong> dengan yang digunakan saat enkripsi.</span>
                  </p>
                </div>

                <div class="pt-4 border-t border-slate-700">
                  <Button
                    type="submit"
                    label="Dekripsi & Ekstrak File"
                    icon="pi pi-unlock"
                    iconPos="right"
                    :loading="isLoading"
                    :disabled="!isValid"
                    class="w-full font-bold py-4 px-6 text-lg rounded-lg bg-emerald-600 hover:bg-emerald-700 border-emerald-600 shadow-lg shadow-emerald-600/20 transition-all duration-200 transform hover:-translate-y-0.5"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'primevue/usetoast'
import FileDropZone from '../components/FileDropZone.vue'

const toast = useToast()
const isLoading = ref(false)
const key = ref ('')
const hostFile = ref(null)

const API_URL = 'http://localhost:8000'

const isValid = computed(() => {
  return hostFile.value && key.value
})

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  window.URL.revokeObjectURL(url)
}

const handleDecode = async () => {
  isLoading.value = true
  const formData = new FormData()
  formData.append('host_file', hostFile.value)
  formData.append('key', key.value.toString())

  try {
    const response = await axios.post(`${API_URL}/decode`, formData, {
      responseType: 'blob'
    })

    if (response.status === 200) {
      // Ambil nama file asli dari header backend
      const disposition = response.headers['content-disposition']
      let filename = 'rahasia_terekstrak.dat' // Default fallback
      
      if (disposition) {
        const match = /filename="([^"]*)"/.exec(disposition)
        if (match) filename = match[1]
      }

      downloadBlob(response.data, filename)
      
      toast.add({ 
        severity: 'success', 
        summary: 'Berhasil!', 
        detail: `File "${filename}" berhasil diekstrak.`, 
        life: 4000 
      })
    }
  } catch (error) {
    let message = 'Gagal memproses file.'
    
    if (error.response && error.response.data) {
      try {
        // Blob error response harus dibaca sebagai text dulu
        const text = await error.response.data.text()
        const json = JSON.parse(text)
        message = json.detail || message
      } catch { 
        message = "Kunci salah atau file tidak mengandung pesan rahasia."
      }
    }
    toast.add({ severity: 'error', summary: 'Gagal', detail: message, life: 5000 })
  } finally {
    isLoading.value = false
  }
}
</script>