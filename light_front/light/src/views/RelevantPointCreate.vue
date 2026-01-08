<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание соотвествующего пункта</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label class="form-label">Ответ:</label>
          <multiselect
            v-model="form.answer"
            :options="answers"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите ответ"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!answerId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.answer" class="error">{{ errors.answer }}</span>
        </div>

        <div class="form-field">
          <label for="text" class="form-label">Текст соотвествующего пункта:</label>
          <textarea v-model="form.text" id="text" class="form-input" rows="3" placeholder="Введите текст вопроса" ></textarea>
          <span v-if="errors.text" class="error">{{ errors.text }}</span>
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
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  answer: null,
  text: '',
});

const loading = ref(false);

const answers = ref([]);
const loadAnswers = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/answers/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    answers.value = response.data.results || [];
    console.log('Разделы тестов загружены:', answers.value);
  } catch (error) {
    console.error('Ошибка при загрузке разделов тестов:', error.response ? error.response.data : error.message);
  }
};

const answerId = route.query.answerId || '';
const loadAnswerById = () => {
  if (answerId) {
    console.log('Answer ID:', answerId);
    const answer = answers.value.find(answer => answer.id === parseInt(answerId, 10));
    if (answer) {
      form.answer = answer;
    } else {
      console.error('Answer не найден.');
    }
  } else {
    console.log('Answer ID не найден.');
  }
};

const cancelEdit = () => {
  router.back();
};

const errors = reactive({});
const validateForm = () => {
  errors.answer = form.answer ? '' : 'Выбор ответа обязателен!';
  errors.text = form.text ? '' : 'Текст обязателен!';
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
      answer: form.answer?.id,
      text: form.text,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/relevant_points/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    const questionId = route.query.questionId || '';
    router.push({ name: 'QuestionDetail', params: { id: questionId }  });
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
    await loadAnswers();
    await loadAnswerById();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
