<template>
  <div class="text-white max-w-5xl mx-auto">
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-white mb-2">Ekstrak & Dekripsi Data</h1>
      <p class="text-slate-400">Ambil kembali pesan rahasia Anda dari media digital.</p>
    </header>

    <div class="bg-slate-900 p-8 rounded-2xl shadow-2xl border border-slate-800">
      <form @submit.prevent="handleDecode">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <div class="lg:col-span-7 space-y-6">
            <div class="bg-indigo-500/10 border border-indigo-500/20 p-4 rounded-xl mb-6">
              <div class="flex items-start gap-3">
                <i class="pi pi-info-circle text-indigo-400 text-xl mt-0.5"></i>
                <div class="text-sm text-slate-300">
                  <p class="font-semibold text-indigo-300 mb-1">Bagaimana cara kerjanya?</p>
                  <p>Upload file media (Gambar, PDF, Audio) yang sudah disisipi pesan. Sistem akan mengekstrak isinya dan memberikannya kepada Anda sebagai file download.</p>
                </div>
              </div>
            </div>

            <FileDropZone
              label="File Media Terenkripsi (Host)"
              icon="pi pi-lock-open"
              v-model:file="hostFile"
              :required="true"
            />
          </div>

          <div class="lg:col-span-5">
            <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 sticky top-6">
              <h3 class="text-lg font-semibold mb-4 text-indigo-400 flex items-center gap-2">
                <i class="pi pi-key"></i> Kunci Keamanan
              </h3>
              
              <div class="space-y-6">
                <div>
                  <label class="font-medium block mb-2 text-slate-300">Masukkan Kunci (1-255)</label>
                  <InputNumber
                    v-model="key"
                    :min="1"
                    :max="255"
                    showButtons
                    buttonLayout="horizontal"
                    class="w-full"
                    inputClass="text-center bg-slate-900 border-slate-600 text-white font-mono"
                  >
                    <template #incrementbuttonicon><span class="pi pi-plus" /></template>
                    <template #decrementbuttonicon><span class="pi pi-minus" /></template>
                  </InputNumber>
                  <small class="text-slate-500 mt-2 block leading-tight">
                    <i class="pi pi-exclamation-triangle text-yellow-600 mr-1"></i>
                    Kunci harus <strong>sama persis</strong> dengan yang digunakan saat enkripsi. Jika salah, hasil ekstraksi akan rusak/gagal.
                  </small>
                </div>

                <div class="pt-4 border-t border-slate-700">
                  <Button
                    type="submit"
                    label="Proses Dekripsi"
                    icon="pi pi-unlock"
                    iconPos="right"
                    :loading="isLoading"
                    :disabled="!isValid"
                    class="w-full p-button-lg bg-emerald-600 hover:bg-emerald-500 border-none shadow-lg shadow-emerald-900/20 transition-all transform hover:-translate-y-0.5"
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
const key = ref(50)
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
      } catch (e) { 
        message = "Kunci salah atau file tidak mengandung pesan rahasia."
      }
    }
    toast.add({ severity: 'error', summary: 'Gagal', detail: message, life: 5000 })
  } finally {
    isLoading.value = false
  }
}
</script>