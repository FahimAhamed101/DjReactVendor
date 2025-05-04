import axios from 'axios'


const apiInstance = axios.create({
    baseURL: 'https://dj-react-vendor.vercel.app/api/v1/',
    timeout: 20000,

    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
    }
})
export default apiInstance 