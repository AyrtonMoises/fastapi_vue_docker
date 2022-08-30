<template>
  <div id="burger-table" v-if="burgers">

    <div>
      <div id="burger-table-heading">
        <div class="order-id">#</div>
        <div>Cliente</div>
        <div>Pão</div>
        <div>Carne</div>
        <div>Opcionais</div>
        <div>Ações</div>
      </div>
    </div>
    <div id="burger-table-rows">
      <div class="burger-table-row" v-for="burger in burgers" :key="burger.id">
        <div class="order-number">{{ burger.id }}</div>
        <div>{{ burger.nome }}</div>
        <div>{{ burger.pao }}</div>
        <div>{{ burger.carne }}</div>
        <div>
          <ul v-for="(opcional, index) in burger.opcionais" :key="index">
            <li>{{ opcional }}</li>
          </ul>
        </div>
        <div>
          <select name="status" class="status" @change="updateBurger($event, burger.id)">
            <option :value="s.id" v-for="s in status" :key="s.id" :selected="burger.status == s.descricao">
              {{ s.descricao }}
            </option>
          </select>
          <button class="delete-btn" @click="deleteBurger(burger.id)">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <h2>Não há pedidos no momento!</h2>
  </div>
</template>
<script>
import { burgerService }  from '@/services/burgers.js'
import { statusService }  from '@/services/status.js'
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'

  export default {
    name: "Pedidos",
    data() {
      return {
        burgers: null,
        burger_id: null,
        status: [],
      }
    },
    methods: {
      async getPedidos() {

        burgerService.getAll()
        .then((response) => {
          this.burgers = response.data
           this.getStatus();
        })
        .catch(()=>{
          createToast("Erro ao buscar", {type: 'danger'})
        });
       

      },
      async getStatus() {

        statusService.getAll()
        .then((response) => {
          this.status = response.data
        })
        .catch(()=>{
          createToast("Erro ao buscar", {type: 'danger'})
        });

      },
      async deleteBurger(id) {

        burgerService.remove(id)
        .then(() => {
          createToast(
            `Pedido deletado com sucesso!`,
            {type: 'success'}
          )
          this.getPedidos();
        })
        .catch(()=>{
          createToast("Erro ao deletar", {type: 'danger'})
        });

        

      },
      async updateBurger(event, id) {

        const option = event.target.value;

        burgerService.update(id, {status_id: option})
        .then((res) => {
            createToast(
              `Pedido #${res.data.id} alterado para ${res.data.status.descricao} com sucesso!`,
              {type: 'success'}
            )
          })
          .catch(()=>{
            createToast("Erro ao alterar", {type: 'danger'})
          });

      }
    },
    mounted () {
    this.getPedidos()
    }
  }
</script>

<style scoped>
  #burger-table {
    max-width: 1200px;
    margin: 0 auto;
  }

  #burger-table-heading,
  #burger-table-rows,
  .burger-table-row {
    display: flex;
    flex-wrap: wrap;
  }

  #burger-table-heading {
    font-weight: bold;
    padding: 12px;
    border-bottom: 3px solid #333;
  }

  .burger-table-row {
    width: 100%;
    padding: 12px;
    border-bottom: 1px solid #CCC;
  }

  #burger-table-heading div,
  .burger-table-row div {
    width: 19%;
  }

  #burger-table-heading .order-id,
  .burger-table-row .order-number {
    width: 5%;
  }

  select {
    padding: 12px 6px;
    margin-right: 12px;
  }

  .delete-btn {
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
  
  .delete-btn:hover {
    background-color: transparent;
    color: #222;
  }
  
</style>