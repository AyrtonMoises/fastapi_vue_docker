<template>
  <div>

    <form id="login-form" method="POST" @submit="loginSubmit">
      <div class="input-container">
        <label for="nome">Usuário</label>
        <input type="text" id="usuario" name="usuario" v-model="usuario" placeholder="Usuário">
      </div>
      <div class="input-container">
        <label for="nome">Senha</label>
        <input type="password" id="senha" name="senha" v-model="senha" placeholder="Senha" autocomplete="on">
      </div>
      <div class="input-container">
        <input class="submit-btn" type="submit" value="Login">
      </div>
    </form>
  </div>
</template>

<script>

import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

export default {
    name: "LoginForm",
    setup() {

        const userStore = useUserStore();

        const { username } = storeToRefs(userStore);
        const { login } = userStore;

        return {
            username,
            login,
        }
    },
    data(){
        return {
            usuario: null,
            senha: null
        }
    },
    methods: {

      loginSubmit(e) {
        e.preventDefault();
        this.login({
          username: this.usuario,
          password: this.senha          
        })

      }

    }

}
</script>

<style scoped>
  #login-form {
    max-width: 400px;
    margin: 0 auto;
  }
  .input-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  label {
    font-weight: bold;
    margin-bottom: 15px;
    color: #222;;
    padding: 5px 10px;
    border-left: 4px solid #fcba03;
  }
  input, select {
    padding: 5px 10px;
    width: 300px;
  }
  #opcionais-container {
    flex-direction: row;
    flex-wrap: wrap;
  }
  #opcionais-title {
    width: 100%;
  }

  .submit-btn {
    background-color: #222;
    color:#fcba03;
    font-weight: bold;
    border: 2px solid #222;
    padding: 10px;
    font-size: 16px;
    margin: 0 auto;
    cursor: pointer;
    transition: .5s;
  }
  .submit-btn:hover {
    background-color: transparent;
    color: #222;
  }
</style>