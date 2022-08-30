import { defineStore } from 'pinia'
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'

import router from '@/router'
import { loginJWT } from '@/services/auth';



export const useUserStore = defineStore('user', {
    state: () => {
        return {
            username: localStorage.getItem('username'),
            returnUrl: null
        }
    },
    actions: {
        login(loginData) {

            loginJWT(loginData)
            .then((response) => {
              this.username = response.data.username
              localStorage.setItem('username', response.data.username);
              localStorage.setItem('access_token', response.data.access_token);
              localStorage.setItem('refresh_token', response.data.refresh_token);
              router.push(this.returnUrl || '/');
            })
            .catch(error => {
              createToast("Usuário/Senha incorretos", {type: 'danger'})
              }
            )
          },
          logout() {
            this.username = null;
            localStorage.removeItem('username');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            router.push('/login');
          }
    },})
