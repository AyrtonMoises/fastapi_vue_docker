<template>
    <div id="nav">
        <head><title>Site</title></head>

        <router-link to="/" id="logo-url">
            <img :src="logo" :alt="alt" id="logo">
        </router-link>
        <router-link to="/">Home</router-link>
        <router-link to="/pedidos">Pedidos</router-link>
        <a v-if="username" href="#" @click="logout()" class="nav-item nav-link">Logout</a>
        <p v-else><router-link to="/login">Login</router-link></p>

    </div>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'


export default {
    name: "Navbar",
    props: ["logo", "alt"],
    setup() {

        const userStore = useUserStore();

        const { username } = storeToRefs(userStore);
        const { logout } = userStore;

        return {
          username,
          logout
        }
    },
}
</script>

<style scoped>
  #nav {
    background-color: #222;
    border-bottom: 4px solid #111;
    padding: 15px 50px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
  #nav #logo-url{
    margin: auto;
    margin-left: 0;
  }
  #logo {
    width: 40px;
    height: 40px;
  }
  #nav a{
    color: #FCBA03;
    text-decoration: none;
    margin: 12px;
    transition: .5s;
  }
  #nav a:hover {
    color: #FFF;
  }
</style>