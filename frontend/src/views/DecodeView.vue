<template>
  <div class="text-white">
    <h1 class="text-3xl font-bold mb-6">Ekstrak & Dekripsi Data</h1>

    <div class="bg-slate-900 p-8 rounded-lg shadow-lg">
      <form @submit.prevent="handleDecode">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <label class="font-semibold block mb-2 text-indigo-400">
              Langkah 1: Media Host (File Terenkripsi)
            </label>
            <div
              class="flex items-center justify-center w-full h-48 bg-slate-800 border-2 border-dashed border-slate-600 rounded-lg cursor-pointer hover:bg-slate-700 transition-colors"
              @dragover.prevent
              @drop.prevent="onHostDrop"
              @click="triggerHostInput"
            >
              <div class="text-center">
                <i class="pi pi-cloud-upload text-4xl text-slate-500"></i>
                <p class="mt-2 text-slate-400">
                  Drag & drop atau <span class="text-indigo-400">klik untuk memilih</span> file
                  terenkripsi.
                </p>
                <p v-if="hostFile" class="mt-2 text-green-400">
                  {{ hostFile.name }} ({{ formatBytes(hostFile.size) }})
                </p>
              </div>
              <input type="file" ref="hostInput" class="hidden" @change="onHostSelect" />
            </div>
          </div>

          <div class="bg-slate-800 p-6 rounded-lg">
            <h3 class="text-lg font-semibold mb-4 text-indigo-400">Opsi & Aksi</h3>
            <div class="field">
              <label for="key" class="font-semibold block mb-2">
                Langkah 2: Kunci Dekripsi (1-255)
              </label>
              <InputNumber
                v-model="key"
                inputId="key"
                :min="1"
                :max="255"
                class="w-full"
                :inputStyle="{ 'background-color': '#1e293b', color: 'white' }"
              />
              <small class="text-slate-400 mt-1">Gunakan kunci yang sama saat enkripsi.</small>
            </div>

            <div class="mt-8 border-t border-slate-700 pt-6">
              <Button
                type="submit"
                label="Proses Ekstraksi"
                icon="pi pi-key"
                iconPos="right"
                :loading="isLoading"
                :disabled="isLoading || !hostFile"
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
import { ref } from 'vue'
import axios from 'axios'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const isLoading = ref(false)
const key = ref(10)
const hostFile = ref(null)
const hostInput = ref(null)
const API_URL = 'http://localhost:8000'

const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const onHostSelect = (event) => {
  hostFile.value = event.target.files[0]
}

const onHostDrop = (event) => {
  hostFile.value = event.dataTransfer.files[0]
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

const handleDecode = async () => {
  if (!hostFile.value || !key.value) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'File host dan Kunci wajib diisi.',
      life: 3000
    })
    return
  }

  isLoading.value = true
  const formData = new FormData()
  formData.append('host_file', hostFile.value)
  formData.append('key', key.value.toString())

  try {
    const response = await axios.post(`${API_URL}/decode`, formData, {
      responseType: 'blob'
    })

    if (response.status === 200) {
      const disposition = response.headers['content-disposition']
      let filename = 'rahasia.dat'
      if (disposition) {
        const match = /filename="([^"]*)"/.exec(disposition)
        if (match) filename = match[1]
      }

      downloadBlob(response.data, filename)
      toast.add({
        severity: 'success',
        summary: 'Sukses',
        detail: 'File rahasia berhasil diekstrak.',
        life: 3000
      })
    }
  } catch (error) {
    let message = 'Terjadi error tidak diketahui.'
    if (error.response && error.response.data) {
      try {
        const errorJson = JSON.parse(await error.response.data.text())
        message = errorJson.detail || message
      } catch {
        message = 'Gagal memproses file. Kunci mungkin salah atau file rusak.'
      }
    }
    toast.add({ severity: 'error', summary: 'Error', detail: message, life: 5000 })
  } finally {
    isLoading.value = false
  }
}
</script>