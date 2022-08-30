<template>
  <div>
    <div class="main-container">
      <h1>Login</h1>
      <LoginForm />
    </div>
  </div>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'

export default {
  name: 'Login',
  title: 'Login',
  components: {
    LoginForm
  }
}
</script>