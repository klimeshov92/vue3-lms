<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание аккаунта</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        <div class="form-field">
          <label for="username" class="form-label">Имя пользователя:</label>
          <input v-model="form.username" id="username" type="text" class="form-input" placeholder="Введите имя пользоваетля" required />
          <span v-if="errors.username" class="error">{{ errors.username }}</span>
        </div>

        <div class="form-field">
          <label for="email" class="form-label">Электронная почта:</label>
          <input v-model="form.email" id="email" type="email" class="form-input" placeholder="Введите электронную почту" required />
          <span v-if="errors.email" class="error">{{ errors.email }}</span>
        </div>

        <div class="form-field">
          <label for="password" class="form-label">Пароль:</label>
          <div class="password-wrapper">
            <input 
              v-model="form.password" 
              :type="isPasswordVisible.password ? 'text' : 'password'"
              id="password" 
              class="form-input password-input"
              placeholder="Введите пароль"
              required 
            />
            <span class="toggle-password" @click="togglePasswordVisibility('password')">
              {{ isPasswordVisible.password ? '👁️' : '👁️‍🗨️' }}
            </span>
          </div>
          <span v-if="errors.password" class="error">{{ errors.password }}</span>
        </div>

        <div class="form-field">
          <label for="password_confirm" class="form-label">Повторите пароль:</label>
          <div class="password-wrapper">
            <input 
              v-model="form.password_confirm" 
              :type="isPasswordVisible.password_confirm ? 'text' : 'password'"
              id="password_confirm" 
              class="form-input password-input"
              placeholder="Повторите пароль"
              required 
            />
            <span class="toggle-password" @click="togglePasswordVisibility('password_confirm')">
              {{ isPasswordVisible.password_confirm ? '👁️' : '👁️‍🗨️' }}
            </span>
          </div>
          <span v-if="errors.password_confirm" class="error">{{ errors.password_confirm }}</span>
        </div>

        <div class="form-field">
          <label for="legal_agree" class="form-label">

              <span>
                Я согласен с
                <RouterLink
                  :to="{ name: 'LegalPage' }"
                  target="_blank"
                  class="link"
                  @click.stop
                >
                  пользовательским соглашением
                </RouterLink>
              </span>

          </label>
          <input v-model="form.legal_agree" id="legal_agree" type="checkbox" class="form-input" />
          <span v-if="errors.legal_agree" class="error">{{ errors.legal_agree }}</span>
        </div>

        <div class="form-field">
          <label for="policy_agree" class="form-label">

            <span>
              Я согласен с
              <RouterLink
                :to="{ name: 'PolicyPage' }"
                target="_blank"
                class="link"
                @click.stop
              >
                политикой конфиденциальности
              </RouterLink>
            </span>


          </label>
          <input v-model="form.policy_agree" id="policy_agree" type="checkbox" class="form-input" />
          <span v-if="errors.policy_agree" class="error">{{ errors.policy_agree }}</span>
        </div>

        <div class="form-field form-recaptcha">
          <div
            class="g-recaptcha"
            :data-sitekey="siteKey"
            data-callback="onCaptchaVerified"
            data-expired-callback="onCaptchaExpired"
          ></div>

          <span v-if="errors.captcha" class="error">
            {{ errors.captcha }}
          </span>
        </div>


      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Создать пользователя</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
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
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, frontendUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  legal_agree:false,
  policy_agree:false,
});

const loading = ref(false);


const isPasswordVisible = reactive({
  password: false,
  password_confirm: false,
});

const togglePasswordVisibility = (field) => {
  isPasswordVisible[field] = !isPasswordVisible[field];
};

const cancelEdit = () => {
  router.back();
};

const siteKey = '6Lcd_j8sAAAAAOIfvcsO1dE010MxFpBjmuSpazva'
let captchaRendered = false
const captchaToken = ref(null)

const onCaptchaVerified = (token) => {
  captchaToken.value = token
}

const onCaptchaExpired = () => {
  captchaToken.value = null
}


const errors = reactive({});
const validateForm = () => {
  errors.username = form.username ? '' : 'Имя пользователя обязательно!';
  errors.email = form.email ? '' : 'Электронная почта обязательна!';
  errors.password = form.password ? '' : 'Пароль обязателен!';
  errors.password_confirm = form.password_confirm ? '' : 'Повтор пароля обязателен!';
  if (form.password && form.password_confirm && form.password !== form.password_confirm) {
    errors.password_confirm = 'Пароли не совпадают!';
  }
  errors.legal_agree = form.legal_agree == true ? '' : 'Согласие с пользовательским соглашением обязательно!';
  errors.policy_agree = form.policy_agree == true ? '' : 'Согласие с политикой конфиденциальности обязательно!';
  errors.captcha = captchaToken.value ? '' : 'Подтвердите, что вы не робот'
  return Object.values(errors).every((error) => !error);
};

const createObject = async () => {

  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    console.log('Отправляем данные для создания объекта:', form);

    const jsonData = {
      username: form.username,
      email: form.email,
      password: form.password,
      legal_agree: form.legal_agree,
      policy_agree: form.policy_agree,
      frontend_url: frontendUrl,
      captcha: captchaToken.value, 
    };

    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.post(`${baseUrl}/register/`, jsonData, {
      headers: { Authorization: '' },
    });

    console.log('Объект создан:', jsonResponse.data);

    router.push({ 
      name: 'PostRegister',
      query: { username: form.username, email: form.email } 
    });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
    if (window.grecaptcha) {
      window.grecaptcha.reset()
      captchaToken.value = null
    }
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    window.onCaptchaVerified = onCaptchaVerified
    window.onCaptchaExpired = onCaptchaExpired

    setTimeout(() => {
      if (window.grecaptcha && !captchaRendered) {
        window.grecaptcha.render(
          document.querySelector('.g-recaptcha'),
          {
            sitekey: siteKey,
            callback: onCaptchaVerified,
            'expired-callback': onCaptchaExpired,
          }
        )
        captchaRendered = true
      }
    }, 0)

    loading.value = true
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
