
<template>
  <div v-if="loading">

    <div class="login-outer">

      <div class="login-inner">

        <div class="login-card">

          <div class="login-header">
            <h1 v-if="done">Пароль изменен!</h1>
            <h1 v-else>Ошибка смены пароля</h1>
          </div>

          <div class="login-text"> 
            <div v-if="done">Можете использовать новый пароль для <router-link :to="{ name: 'Login' }" class="link">входа</router-link> в аккаунт.</div>
            <div v-else>Возможно ссылка просрочена. Повторите запрос на <router-link :to="{ name: 'PasswordResetRequest' }" class="link">смену пароля</router-link> или обратитесь к администратору.</div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>
</template>
 
<script setup>

const loading = ref(false);

import { reactive, onMounted, onBeforeUnmount, ref, watch } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const done = ref(route.query.done === 'true');

onMounted(() => {
  loading.value = true;
});

</script>

<style scoped>
  /* Стили для главной страницы */
</style>
 