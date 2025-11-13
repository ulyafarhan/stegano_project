<template>
  <div class="text-white max-w-5xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 mt-12 sm:mt-16 mb-12">
    <header class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-white mb-2">Enkripsi & Sisipkan Data</h1>
      <p class="text-slate-400 text-sm sm:text-base">Sembunyikan pesan rahasia Anda ke dalam media digital dengan aman.</p>
    </header>

    <div class="bg-slate-900 p-4 sm:p-6 md:p-8 rounded-2xl shadow-2xl border border-slate-800">
      <transition name="fade">
        <div v-if="isHostTooSmall" class="bg-red-500/10 border border-red-500/50 text-red-200 p-3 sm:p-4 rounded-xl mb-6 sm:mb-8 flex items-start gap-3">
          <i class="pi pi-exclamation-triangle text-lg sm:text-xl mt-0.5"></i>
          <div>
            <p class="font-bold text-sm sm:text-base">Media host terlalu kecil!</p>
            <p class="text-xs sm:text-sm opacity-90">Ukuran host ({{ formatBytes(hostFile?.size || 0) }}) harus lebih besar dari payload ({{ formatBytes(finalPayloadSize) }}).</p>
          </div>
        </div>
      </transition>

      <form @submit.prevent="handleEncode">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 md:gap-8">
          
          <div class="lg:col-span-7 space-y-6 sm:space-y-8">
            
            <div>
              <label class="font-semibold block mb-2 sm:mb-3 text-indigo-400 text-sm sm:text-base">1. Data Rahasia (Payload)</label>
              
              <div class="flex bg-slate-800 p-1 rounded-lg mb-3 sm:mb-4 w-fit border border-slate-700">
                <button 
                  type="button"
                  @click="inputMode = 'file'"
                  class="px-3 sm:px-4 py-2 rounded-md text-xs sm:text-sm font-medium transition-all"
                  :class="inputMode === 'file' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'"
                >
                  <i class="pi pi-file mr-1 sm:mr-2"></i>Upload File
                </button>
                <button 
                  type="button"
                  @click="inputMode = 'text'"
                  class="px-3 sm:px-4 py-2 rounded-md text-xs sm:text-sm font-medium transition-all"
                  :class="inputMode === 'text' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'"
                >
                  <i class="pi pi-align-left mr-1 sm:mr-2"></i>Ketik Pesan
                </button>
              </div>

              <div v-if="inputMode === 'file'">
                <FileDropZone
                  label=""
                  icon="pi pi-file"
                  v-model:file="uploadedPayload"
                  :required="true"
                />
              </div>

              <div v-else>
                <div class="relative group">
                  <textarea
                    v-model="textPayload"
                    rows="6"
                    class="w-full bg-slate-800 border-2 border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors resize-none"
                    placeholder="Ketik pesan rahasia Anda di sini..."
                  ></textarea>
                  <div class="absolute bottom-3 right-3 text-xs text-slate-500 bg-slate-800/80 px-2 py-1 rounded">
                    {{ textPayload.length }} karakter ({{ formatBytes(textPayload.length) }})
                  </div>
                </div>
                <p class="text-xs text-slate-500 mt-2">
                  <i class="pi pi-info-circle"></i> Teks ini akan otomatis dikonversi menjadi file <strong>pesan_rahasia.txt</strong>.
                </p>
              </div>
            </div>

            <div class="relative">
              <div class="absolute left-8 -top-6 bottom-4 w-0.5 bg-gradient-to-b from-slate-700/0 via-slate-700/50 to-slate-700/0 -z-10"></div>
              
              <FileDropZone
                label="2. Media Penampung (Host)"
                icon="pi pi-image"
                accept=".png,.jpg,.jpeg,.pdf,.wav,.mp3,.mp4,.docx"
                v-model:file="hostFile"
                :required="true"
              />
            </div>
          </div>

          <div class="lg:col-span-5">
            <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 sticky top-6">
              <h3 class="text-lg font-semibold mb-4 text-indigo-400 flex items-center gap-2">
                <i class="pi pi-cog"></i> Konfigurasi
              </h3>
              
              <div class="space-y-6">
                <div>
                  <label class="font-medium block mb-2 text-slate-300">Kunci Enkripsi (1-255)</label>
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
                </div>

                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-slate-400">Estimasi Payload:</span>
                    <span class="text-white font-mono">{{ formatBytes(finalPayloadSize) }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-slate-400">Kapasitas Host:</span>
                    <span class="text-white font-mono">{{ hostFile ? formatBytes(hostFile.size) : '-' }}</span>
                  </div>
                </div>

                <div class="pt-4 border-t border-slate-700">
                  <Button
                    type="submit"
                    label="Proses Enkripsi"
                    icon="pi pi-lock"
                    iconPos="right"
                    :loading="isLoading"
                    :disabled="!isValid"
                    class="w-full p-button-lg bg-indigo-600 hover:bg-indigo-500 border-none shadow-lg shadow-indigo-900/20 transition-all transform hover:-translate-y-0.5"
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

// State untuk Dual Mode
const inputMode = ref('file') // 'file' | 'text'
const uploadedPayload = ref(null)
const textPayload = ref('')
const hostFile = ref(null)

const API_URL = 'http://localhost:8000'

// Logic menghitung ukuran payload aktual
const finalPayloadSize = computed(() => {
  if (inputMode.value === 'file') {
    return uploadedPayload.value ? uploadedPayload.value.size : 0
  } else {
    // Hitung ukuran bytes dari string teks
    return new Blob([textPayload.value]).size
  }
})

const isHostTooSmall = computed(() => {
  if (!hostFile.value || finalPayloadSize.value === 0) return false
  return hostFile.value.size <= finalPayloadSize.value
})

const isValid = computed(() => {
  const hasPayload = inputMode.value === 'file' 
    ? !!uploadedPayload.value 
    : textPayload.value.length > 0
    
  return hasPayload && hostFile.value && key.value && !isHostTooSmall.value
})

const formatBytes = (bytes, decimals = 2) => {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

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

const handleEncode = async () => {
  isLoading.value = true
  const formData = new FormData()
  
  // LOGIC UTAMA: Tentukan apa yang dikirim ke Backend
  if (inputMode.value === 'file') {
    // 1. Kirim File Upload Biasa
    formData.append('payload_file', uploadedPayload.value)
  } else {
    // 2. Konversi Teks menjadi File .txt Virtual
    const textBlob = new Blob([textPayload.value], { type: 'text/plain' })
    // Kita beri nama file "pesan_rahasia.txt"
    const textFile = new File([textBlob], "pesan_rahasia.txt", { type: "text/plain" })
    formData.append('payload_file', textFile)
  }

  formData.append('host_file', hostFile.value)
  formData.append('key', key.value.toString())

  try {
    const response = await axios.post(`${API_URL}/encode`, formData, {
      responseType: 'blob'
    })

    if (response.status === 200) {
      const disposition = response.headers['content-disposition']
      let filename = `encoded_${hostFile.value.name}`
      if (disposition) {
        const match = /filename="([^"]*)"/.exec(disposition)
        if (match) filename = match[1]
      }

      downloadBlob(response.data, filename)
      toast.add({ severity: 'success', summary: 'Sukses', detail: 'Pesan berhasil disembunyikan & diunduh!', life: 3000 })
      
      // Reset form text agar tidak ganda
      if(inputMode.value === 'text') textPayload.value = ''
      else uploadedPayload.value = null
    }
  } catch (error) {
    let message = 'Gagal menghubungi server.'
    if (error.response && error.response.data) {
      try {
        const text = await error.response.data.text()
        const json = JSON.parse(text)
        message = json.detail || message
      } catch (e) { /* ignore */ }
    }
    toast.add({ severity: 'error', summary: 'Gagal', detail: message, life: 5000 })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>