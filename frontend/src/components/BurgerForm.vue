<template>
  <div>
    <form id="burger-form" method="POST" @submit="createBurger">
      <div class="input-container">
        <label for="nome">Nome do cliente:</label>
        <input type="text" id="nome" name="nome" v-model="nome" placeholder="Digite o seu nome">
      </div>
      <div class="input-container">
        <label for="pao">Escolha o pão:</label>
        <select name="pao" id="pao" v-model="pao">
          <option value="">Selecione o seu pão</option>
          <option v-for="pao in paes" :key="pao.id" :value="pao.id">{{ pao.descricao }}</option>
        </select>
      </div>
      <div class="input-container">
        <label for="carne">Escolha a carne do seu Burger:</label>
        <select name="carne" id="carne" v-model="carne">
          <option value="">Selecione o tipo de carne</option>
          <option v-for="carne in carnes" :key="carne.id" :value="carne.id">{{ carne.descricao }}</option>
        </select>
      </div>
      <div id="opcionais-container" class="input-container">
        <label id="opcionais-title" for="opcionais">Selecione os opcionais:</label>
        <div class="checkbox-container" v-for="opcional in opcionaisdata" :key="opcional.id">
          <input type="checkbox" name="opcionais" v-model="opcionais" :value="opcional.id">
          <span>{{ opcional.descricao }}</span>
        </div>
      </div>
      <div class="input-container">
        <input class="submit-btn" type="submit" value="Criar meu Burger!">
      </div>
    </form>
  </div>
</template>

<script>
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'
import { burgerService }  from '@/services/burgers.js'
import { opcionalService }  from '@/services/opcionais.js'
import { ingredienteService }  from '@/services/ingredientes.js'


export default {
    name: "BurgerForm",
    data(){
        return {
            paes: null,
            carnes: null,
            opcionaisdata: null,
            nome: null,
            pao: null,
            carne: null,
            opcionais: [],
            msg: null,

        }
    },
    methods: {
        async getCarnes(){
          ingredienteService.getCarnesAll()
          .then((response) => {
            this.carnes = response.data
          })
          .catch(()=>{
            createToast("Erro ao buscar carnes", {type: 'danger'})
          });

        },
        async getPaes(){
          ingredienteService.getPaesAll()
          .then((response) => {
            this.paes = response.data
          })
          .catch(()=>{
            createToast("Erro ao buscar paes", {type: 'danger'})
          });

        },
        async getOpcionais(){
          opcionalService.getAll()
          .then((response) => {
            this.opcionaisdata = response.data
          })
          .catch(()=>{
            createToast("Erro ao buscar opcionais", {type: 'danger'})
          });

        },
        async createBurger(e){
            e.preventDefault();

          const data = {
              nome: this.nome,
              carne: this.carne,
              pao: this.pao,
              opcionais: Array.from(this.opcionais),
              preco: 29.99,
              status: 1
          }

          burgerService.create(data)
          .then((res) => {

              createToast(
               `Pedido #${res.data.id} realizado com sucesso!`,
                {type: 'success'}
              )
              this.nome = "";
              this.carne = "";
              this.pao = "";
              this.opcionais = "";
            })
            .catch(()=>{
              createToast("Erro ao realizar pedido", {type: 'danger'})
            });


        }
    },
    mounted(){
        this.getCarnes()
        this.getPaes()
        this.getOpcionais()
    }
}
</script>

<style scoped>
  #burger-form {
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
  .checkbox-container {
    display: flex;
    align-items: flex-start;
    width: 50%;
    margin-bottom: 20px;
  }
  .checkbox-container span,
  .checkbox-container input {
    width: auto;
  }
  .checkbox-container span {
    margin-left: 6px;
    font-weight: bold;
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