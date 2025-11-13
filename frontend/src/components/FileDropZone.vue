<template>
  <div>
    <label class="font-semibold block mb-1 sm:mb-2 text-indigo-400 text-sm sm:text-base">
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div
      class="relative group w-full h-32 sm:h-40 md:h-48 rounded-xl border-2 border-dashed transition-all duration-300 ease-in-out cursor-pointer overflow-hidden"
      :class="[
        isDragging 
          ? 'border-indigo-400 bg-indigo-500/10 scale-[1.02]' 
          : 'border-slate-600 bg-slate-800 hover:bg-slate-750 hover:border-slate-500',
        file ? 'border-solid border-emerald-500/50 bg-emerald-500/5' : ''
      ]"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="triggerInput"
    >
      <div v-if="!file" class="absolute inset-0 flex flex-col items-center justify-center text-center p-2 sm:p-4">
        <div class="p-2 sm:p-3 rounded-full bg-slate-700/50 mb-2 sm:mb-3 group-hover:scale-110 transition-transform">
          <i :class="icon" class="text-xl sm:text-2xl md:text-3xl text-slate-400 group-hover:text-indigo-400 transition-colors"></i>
        </div>
        <p class="text-xs sm:text-sm text-slate-300 font-medium">
          Klik untuk upload <span v-if="accept">({{ acceptExtensions }})</span>
        </p>
        <p class="text-xs text-slate-500 mt-0.5 sm:mt-1">atau drag & drop file ke sini</p>
      </div>

      <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-800 z-10">
        <i class="pi pi-check-circle text-2xl sm:text-3xl md:text-4xl text-emerald-400 mb-1 sm:mb-2 animate-bounce"></i>
        <p class="font-bold text-white truncate max-w-[90%] px-2 sm:px-4 text-sm sm:text-base">{{ file.name }}</p>
        <p class="text-xs text-emerald-400 font-mono mt-0.5 sm:mt-1">{{ formatBytes(file.size) }}</p>
        
        <button 
          @click.stop="removeFile"
          class="mt-2 sm:mt-4 px-2 sm:px-3 py-1 rounded-md bg-red-500/10 text-red-400 text-xs sm:text-sm hover:bg-red-500 hover:text-white transition-colors flex items-center gap-1 sm:gap-2"
        >
          <i class="pi pi-trash"></i> Hapus
        </button>
      </div>

      <input
        type="file"
        ref="fileInput"
        class="hidden"
        :accept="accept"
        @change="handleSelect"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  label: { type: String, default: 'Upload File' },
  icon: { type: String, default: 'pi pi-upload' },
  accept: { type: String, default: '' }, // e.g., ".jpg,.png,.pdf"
  required: { type: Boolean, default: false }
})

const emit = defineEmits(['update:file'])

const fileInput = ref(null)
const isDragging = ref(false)
const file = ref(null)

// Helper untuk tampilan ekstensi
const acceptExtensions = computed(() => {
  if (!props.accept) return 'Semua Format'
  return props.accept.split(',').map(ext => ext.trim().replace('.', '').toUpperCase()).join('/')
})

const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const triggerInput = () => {
  fileInput.value.click()
}

const handleFile = (selectedFile) => {
  if (selectedFile) {
    file.value = selectedFile
    emit('update:file', selectedFile)
  }
}

const handleSelect = (event) => {
  handleFile(event.target.files[0])
}

const handleDrop = (event) => {
  isDragging.value = false
  handleFile(event.dataTransfer.files[0])
}

const removeFile = () => {
  file.value = null
  if (fileInput.value) fileInput.value.value = '' // Reset input
  emit('update:file', null)
}
</script>