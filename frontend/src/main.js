import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import titleMixin from './mixins/titleMixin'


const pinia = createPinia();
const app = createApp(App)


app.use(pinia);
app.use(router);
app.mixin(titleMixin);

app.mount('#app');
