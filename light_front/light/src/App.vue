<template>
  <Header v-if="!isScormPage" />
  <div v-if="!isScormPage" class="main">
    <div class="content-outer">
      <div class="content-inner">
        <router-view />
      </div>
    </div>
    <footer v-if="!isScormPage" class="footer-outer">
      <div class="footer-inner">

        <router-link :to="{ name: 'HomePage' }" 
          @click="toggleMenu" 
          class="list-settings-button">
          <div>
            Главная страница
          </div>
        </router-link>

        <router-link :to="{ name: 'LegalPage' }" 
          @click="toggleMenu" 
          class="list-settings-button">
          <div>
            Пользовательское соглашение
          </div>
        </router-link>

        <router-link :to="{ name: 'PolicyPage' }" 
          @click="toggleMenu" 
          class="list-settings-button">
          <div>
            Политика конфиденциальности
          </div>
        </router-link>
       </div>

    </footer>
  </div>
  <div v-if="isScormPage">
    <router-view />
  </div>
  
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import Header from './components/Header.vue';

const route = useRoute();

const isScormPage = computed(() => route.name === 'ScormContent');
</script>

<style scoped>
/* Добавь свои стили для главного компонента здесь */
</style>
