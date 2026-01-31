
<template>
  <div v-if="loading">

    <div class="login-outer">

      <div class="login-inner">

        <div class="login-card">

          <div class="login-header">
            <h1>Письмо отправлено!</h1>
          </div>

          <div class="login-text"> 
            <div>Для смены пароля откройте письмо на {{ email }} и перейдите по ссылке.</div>
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const username = ref(route.query.username || '');
const email = ref(route.query.email || '');

onMounted(() => {
  loading.value = true;
});

</script>

<style scoped>
  /* Стили для главной страницы */
</style>
 