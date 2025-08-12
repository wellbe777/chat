import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import { useCookies } from 'vue3-cookies';
import axios from "axios"
import i18n from './i18n'

axios.defaults.withCredentials = true

const app = createApp(App)

app.use(router)
app.use(useCookies)
app.use(i18n)

app.mount('#app')