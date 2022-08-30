import { createRouter, createWebHistory } from 'vue-router'
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'

import HomeView from '../views/HomeView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import { useUserStore } from '@/stores/user';


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/pedidos',
    name: 'pedidos',
    component: () => import('../views/PedidosView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  { path: '/:pathMatch(.*)*', name: 'notfound', component: NotFoundView }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to) => {

  const publicPages = ['/login', '/',];
  const authRequired = !publicPages.includes(to.path);
  const userStore = useUserStore();

  if (authRequired && !userStore.username) {
      createToast('Usuário sem permissão', {type: 'danger'})
      userStore.returnUrl = to.fullPath;
      return '/login';
  }
});



export default router
