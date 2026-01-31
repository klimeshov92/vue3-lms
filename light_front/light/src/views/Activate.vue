
<template>
  <div v-if="loading">

    <div class="login-outer">

      <div class="login-inner">

        <div class="login-card">

          <div class="login-header">
            <h1 v-if="activation">Активация завершена</h1>
            <h1 v-else>Ошибка активации</h1>
          </div>

          <div class="login-text"> 
            <div v-if="activation">Используйте логин и пароль для <router-link :to="{ name: 'Login' }" class="link">входа</router-link> в аккаунт.</div>
            <div v-else>Возможно ссылка просрочена. Попробуйте <router-link :to="{ name: 'Register' }" class="link">зарегистрироваться</router-link> снова или обратитесь к администратору.</div>
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

import { reactive, onMounted, ref, watch } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const uid = route.params.uid;
const token = route.params.token;

const activation = ref(false);
const fetchActivate = async () => {
  try {
    const response = await axios.get(`${baseUrl}/activate/${uid}/${token}/`, {
      headers: { Authorization: '' },
    });
    console.log(`Ответ по активации:`, response.data);
    activation.value = response.data.activation;
    console.log(`Активация:`, activation.value);

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await fetchActivate();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});


</script>

<style scoped>
  /* Стили для главной страницы */
</style>
 