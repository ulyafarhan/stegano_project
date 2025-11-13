<template>
  <div class="text-white">
    <h1 class="text-3xl font-bold mb-6">Enkripsi & Sisipkan Data</h1>

    <div class="bg-slate-900 p-8 rounded-lg shadow-lg">
      <div v-if="isHostTooSmall" class="bg-red-500 text-white p-4 rounded-lg mb-6">
        <p class="font-bold">Peringatan: Media host terlalu kecil!</p>
        <p>Ukuran media host harus lebih besar dari file rahasia.</p>
      </div>

      <form @submit.prevent="handleEncode">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="space-y-8">
            <div>
              <label class="font-semibold block mb-2 text-indigo-400">
                Langkah 1: File Rahasia (Payload)
              </label>
              <div
                class="flex items-center justify-center w-full h-48 bg-slate-800 border-2 border-dashed border-slate-600 rounded-lg cursor-pointer hover:bg-slate-700 transition-colors"
                @dragover.prevent
                @drop.prevent="onPayloadDrop"
                @click="triggerPayloadInput"
              >
                <div class="text-center">
                  <i class="pi pi-file text-4xl text-slate-500"></i>
                  <p class="mt-2 text-slate-400">
                    Drag & drop atau <span class="text-indigo-400">klik untuk memilih</span> file
                    rahasia.
                  </p>
                  <p v-if="payloadFile" class="mt-2 text-green-400 font-mono text-sm">
                    {{ payloadFile.name }} ({{ formatBytes(payloadFile.size) }})
                  </p>
                </div>
                <input
                  type="file"
                  ref="payloadInput"
                  class="hidden"
                  @change="onPayloadSelect"
                />
              </div>
            </div>

            <div>
              <label class="font-semibold block mb-2 text-indigo-400">
                Langkah 2: Media Penampung (Host)
              </label>
              <div
                class="flex items-center justify-center w-full h-48 bg-slate-800 border-2 border-dashed border-slate-600 rounded-lg cursor-pointer hover:bg-slate-700 transition-colors"
                @dragover.prevent
                @drop.prevent="onHostDrop"
                @click="triggerHostInput"
              >
                <div class="text-center">
                  <i class="pi pi-image text-4xl text-slate-500"></i>
                  <p class="mt-2 text-slate-400">
                    Drag & drop atau <span class="text-indigo-400">klik untuk memilih</span> media
                    penampung.
                  </p>
                  <p v-if="hostFile" class="mt-2 text-green-400 font-mono text-sm">
                    {{ hostFile.name }} ({{ formatBytes(hostFile.size) }})
                  </p>
                </div>
                <input 
                  type="file" 
                  ref="hostInput" 
                  class="hidden" 
                  accept=".png,.jpg,.jpeg,.wav,.mp3,.mp4,.m4a,.pdf,.docx,.xlsx"
                  @change="onHostSelect" 
                />
              </div>
            </div>
          </div>

          <div class="bg-slate-800 p-6 rounded-lg">
            <h3 class="text-lg font-semibold mb-4 text-indigo-400">Opsi & Aksi</h3>
            <div class="field">
              <label for="key" class="font-semibold block mb-2">
                Langkah 3: Kunci Enkripsi (1-255)
              </label>
              <InputNumber
                v-model="key"
                inputId="key"
                :min="1"
                :max="255"
                class="w-full"
                :inputStyle="{ 'background-color': '#1e293b', color: 'white' }"
              />
              <small class="text-slate-400 mt-1">Angka ini wajib diingat untuk dekripsi.</small>
            </div>

            <div class="mt-8 border-t border-slate-700 pt-6">
              <Button
                type="submit"
                label="Proses Sekarang"
                icon="pi pi-lock"
                iconPos="right"
                :loading="isLoading"
                :disabled="isLoading || !hostFile || !payloadFile || isHostTooSmall"
                class="w-full p-button-lg bg-indigo-500 hover:bg-indigo-600 border-indigo-500"
              />
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

const toast = useToast()
const isLoading = ref(false)

const key = ref(10)
const payloadFile = ref(null)
const hostFile = ref(null)
const payloadInput = ref(null)
const hostInput = ref(null)

const API_URL = 'http://localhost:8000'

const isHostTooSmall = computed(() => {
  if (!payloadFile.value || !hostFile.value) return false
  // Peringatan dasar: Host sebaiknya lebih besar dari payload
  return hostFile.value.size <= payloadFile.value.size
})

const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const onPayloadSelect = (event) => {
  payloadFile.value = event.target.files[0]
}
const onHostSelect = (event) => {
  hostFile.value = event.target.files[0]
}

const onPayloadDrop = (event) => {
  payloadFile.value = event.dataTransfer.files[0]
}

const onHostDrop = (event) => {
  hostFile.value = event.dataTransfer.files[0]
}

const triggerPayloadInput = () => {
  payloadInput.value.click()
}

const triggerHostInput = () => {
  hostInput.value.click()
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
  if (!payloadFile.value || !hostFile.value || !key.value) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Semua file dan kunci wajib diisi.',
      life: 3000
    })
    return
  }

  isLoading.value = true
  const formData = new FormData()
  formData.append('payload_file', payloadFile.value)
  formData.append('host_file', hostFile.value)
  formData.append('key', key.value.toString())

  try {
    const response = await axios.post(`${API_URL}/encode`, formData, {
      responseType: 'blob'
    })

    if (response.status === 200) {
      const disposition = response.headers['content-disposition']
      let filename = 'encoded_file'
      if (disposition) {
        const match = /filename="([^"]*)"/.exec(disposition)
        if (match) filename = match[1]
      }

      downloadBlob(response.data, filename)
      toast.add({
        severity: 'success',
        summary: 'Sukses',
        detail: 'File berhasil dienkripsi dan diunduh.',
        life: 3000
      })
      
      // Reset form
      payloadFile.value = null
      hostFile.value = null
    }
  } catch (error) {
    let message = 'Terjadi error tidak diketahui.'
    if (error.response && error.response.data) {
      // Jika response blob, kita perlu konversi ke text untuk baca error JSON
      try {
        const errorText = await error.response.data.text()
        const errorJson = JSON.parse(errorText)
        message = errorJson.detail || message
      } catch {
        message = 'Gagal memproses file di server.'
      }
    }
    toast.add({ severity: 'error', summary: 'Gagal', detail: message, life: 5000 })
  } finally {
    isLoading.value = false
  }
}
</script>