import axios from 'axios';
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'

import { useUserStore } from '@/stores/user'


export default () => {
    let headers = {};
    let accessToken = localStorage.getItem('access_token');

    if (accessToken && accessToken !== '') {
        headers.Authorization = 'Bearer' + ' ' + accessToken;
    };
    const instance = axios.create({
        baseURL: process.env.VUE_APP_API,
        headers: headers
    });

    instance.interceptors.response.use((response) => {
        return response;
    }, (error) => {
        if(error.response.status === 401 && error.response.config.url !== '/api/token') {
            createToast('Usuário não autorizado', {type: 'danger'})
            const userStore = useUserStore();
            const { logout } = userStore;
            logout()
        }
        else if (error.response.status >= 500) {
            createToast('Erro no servidor', {type: 'danger'})
            return Promise.reject(error.response.data);
        }
        return Promise.reject(error.message);
    });

    return instance;
}