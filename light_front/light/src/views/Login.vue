<template>
  <div v-if="loading">

    <div class="login-outer">

      <div class="login-inner">

        <div class="login-card">

          <!-- Заголовок страницы входа -->
          <div class="login-header">
              <h1>Авторизация</h1>
          </div>

          <!-- Форма для входа -->
          <form @submit.prevent="login" id="login-form" class="login-form">

            <div class="login-form-field">
              <label for="username" class="login-form-label">Имя пользователя:</label>
              <input v-model="username" class="form-input" id="username" type="text" required />
            </div>

            <div class="login-form-field">
              <label for="password" class="login-form-label">Пароль:</label>
              <div class="password-wrapper">
                <input
                  v-model="password"
                  class="form-input password-input"
                  id="password"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  required
                />
                <!-- Иконка для переключения видимости пароля -->
                <span @click="togglePasswordVisibility" class="toggle-password">
                  {{ isPasswordVisible ? '👁️' : '👁️‍🗨️' }}
                </span>
              </div>
            </div>

          </form>

          <div class="login-menu button-group">
            <button type="submit" form="login-form" class="button">Войти</button>
            <button type="button" @click="goToRegister" class="button">Регистрация</button>
            <button type="button" @click="goToPasswordResetRequest" class="button">Cмена пароля</button>
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
import { reactive, onMounted, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref(''); // Переменная для имени пользователя
const password = ref(''); // Переменная для пароля
const isPasswordVisible = ref(false); // Управление видимостью пароля
import { baseUrl, isTokenValid, setUserId, clearUserId } from '../utils/utils';

const loading = ref(false);

// Функция для выполнения входа
const login = async () => {
  try {
    console.log('Начало процесса входа');
    localStorage.removeItem('access_token');
    clearUserId();
    console.log('Токен и user_id очищены');

    console.log('Отправка POST-запроса для аутентификации');
    const response = await axios.post(`${baseUrl}/token/`, {
      username: username.value,
      password: password.value,
    });
    console.log('Ответ на запрос входа:', response.data);

    localStorage.setItem('access_token', response.data.access);
    console.log('Токен доступа сохранен в localStorage');

    const validToken = isTokenValid(response.data.access);
    if (validToken) {
      setUserId(validToken.user_id);
      console.log('ID пользователя установлен:', validToken.user_id);
    } else {
      console.warn('Токен недействителен');
    }

    // Проверка наличия параметра redirect и перенаправление
    const redirectPath = router.currentRoute.value.query.redirect || { name: 'HomePage' };
    console.log('Путь для перенаправления:', redirectPath);
    router.push(redirectPath); // Переход по сохраненному маршруту или на главную
    console.log('Пользователь перенаправлен');
  } catch (error) {
    console.error('Ошибка входа:', error);
    alert('Ошибка входа, проверьте учетные данные');
  }
};

// Переключение видимости пароля
const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};

const goToRegister = () => {
  router.push({ name: 'Register' });
};

const goToPasswordResetRequest = () => {
  router.push({ name: 'PasswordResetRequest' });
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Стили можно добавить по мере необходимости */
</style>
