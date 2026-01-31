<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание раздела теста</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Тест:</label>
          <multiselect
            v-model="form.test"
            :options="tests"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите тест"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!testId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.test" class="error">{{ errors.test }}</span>
        </div>

        <div class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div class="form-field">
          <label for="desc" class="form-label">Описание:</label>
          <textarea v-model="form.desc" id="desc" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
        </div>

        <div class="form-field">
          <label for="sample_size" class="form-label">Размер выборки:</label>
          <input v-model="form.sample_size" id="sample_size" type="number" class="form-input" placeholder="Введите размер выборки" />
          <span v-if="errors.sample_size" class="error">{{ errors.sample_size }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>

</template>

<script setup>
import { reactive, onMounted, ref, watch, computed } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  test: null,
  item: null,
  name: '',
  desc: '',
  sample_size: null,
});

const loading = ref(false);

const tests = ref([]);
const loadTests = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/tests/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    tests.value = response.data.results || [];
    console.log('Тесты задач загружены:', tests.value);
  } catch (error) {
    console.error('Ошибка при загрузке тестов:', error.response ? error.response.data : error.message);
  }
};

const testId = route.query.testId || '';
const loadTestById = () => {
  if (testId) {
    console.log('Test ID:', testId);
    const test = tests.value.find(test => test.id === parseInt(testId, 10));
    if (test) {
      form.test = test;
    } else {
      console.error('Test не найден.');
    }
  } else {
    console.log('Test ID не найден.');
  }
};

const cancelEdit = () => {
  const testId = route.query.testId || '';
  router.push({ name: 'TestDetail', params: { id: testId }  });
};

const errors = reactive({});
const validateForm = () => {
  errors.test = form.test ? '' : 'Выбор шаблона задачи обязателен!';
  errors.item = form.item && form.item > 0 ? '' : 'Пункт обязателен и должен быть больше 0!';
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
      test: form.test?.id,
      item: form.item,
      name: form.name,
      desc: form.desc,
      sample_size: form.sample_size,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/test_sections/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    const testId = route.query.testId || '';
    router.push({ name: 'TestDetail', params: { id: testId }  });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadTests();
    await loadTestById();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
