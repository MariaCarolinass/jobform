import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const instance = axios.create({
    baseURL: API_URL,
    timeout: 15000,
})

export default instance