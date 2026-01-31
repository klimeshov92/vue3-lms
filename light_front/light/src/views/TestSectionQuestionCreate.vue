<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание вопроса раздела теста</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Раздел теста:</label>
          <multiselect
            v-model="form.test_section"
            :options="test_sections"
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
            :disabled="!!testSectionId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.test_section" class="error">{{ errors.test_section }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Вопрос:</label>
          <multiselect
            v-model="form.question"
            :options="questions"
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
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.question" class="error">{{ errors.question }}</span>
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
  test_section: null,
  question: null,
  item: null,
});

const loading = ref(false);

const test_sections = ref([]);
const loadTestSections = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/test_sections/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    test_sections.value = response.data.results || [];
    console.log('Разделы тестов загружены:', test_sections.value);
  } catch (error) {
    console.error('Ошибка при загрузке разделов тестов:', error.response ? error.response.data : error.message);
  }
};

const testSectionId = route.query.testSectionId || '';
const loadTestSectionById = () => {
  if (testSectionId) {
    console.log('TestSection ID:', testSectionId);
    const test_section = test_sections.value.find(test_section => test_section.id === parseInt(testSectionId, 10));
    if (test_section) {
      form.test_section = test_section;
    } else {
      console.error('TestSection не найден.');
    }
  } else {
    console.log('TestSection ID не найден.');
  }
};

const questions = ref([]);
const loadQuestions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/questions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    questions.value = response.data.results || [];
    console.log('Вопросы загружены:', questions.value);
  } catch (error) {
    console.error('Ошибка при загрузке вопросов:', error.response ? error.response.data : error.message);
  }
};

const cancelEdit = () => {
  const testId = route.query.testId || '';
  router.push({ name: 'TestDetail', params: { id: testId }  });
};

const errors = reactive({});
const validateForm = () => {
  errors.test_section = form.test_section ? '' : 'Выбор раздела теста обязателен!';
  errors.question = form.question ? '' : 'Выбор вопроса обязателен!';
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
      test_section: form.test_section?.id,
      question: form.question?.id,
      item: form.item,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/test_section_questions/`, jsonData, {
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
    await loadTestSections();
    await loadTestSectionById();
    await loadQuestions();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
