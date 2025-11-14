import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. TAILWIND & KUSTOMISASI KITA (HARUS DIIMPOR PERTAMA)
// Ini akan memuat @tailwind base terlebih dahulu
import './assets/main.css' 

// 2. TEMA PRIME VUE (DIIMPOR SETELAH TAILWIND)
// Tema PrimeVue sekarang akan menimpa @tailwind base, bukan sebaliknya
import 'primevue/resources/themes/lara-dark-indigo/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

// --- Sisa Konfigurasi ---
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'

// Impor Komponen
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputNumber from 'primevue/inputnumber'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import Menubar from 'primevue/menubar'
import Password from 'primevue/password' // Pastikan ini ada dari langkah sebelumnya

const app = createApp(App)

app.use(router)
app.use(PrimeVue)
app.use(ToastService)

// Registrasi Komponen
app.component('Button', Button)
app.component('Card', Card)
app.component('InputNumber', InputNumber)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('Menubar', Menubar)
app.component('Password', Password) // Pastikan ini ada

app.mount('#app')