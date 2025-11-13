import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. TEMA PRIME VUE (HARUS DIIMPOR PERTAMA)
// Kita impor tema gelapnya di sini
import 'primevue/resources/themes/lara-dark-indigo/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

// 2. TAILWIND & KUSTOMISASI KITA (HARUS DIIMPOR TERAKHIR)
// Ini akan menimpa bagian dari lara-dark-indigo yang kita tidak suka
import './assets/main.css' 

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

app.mount('#app')