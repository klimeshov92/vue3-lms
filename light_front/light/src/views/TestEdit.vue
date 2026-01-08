<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование теста</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label for="avatar" class="form-label">Аватар:</label>
          <input type="file" id="avatar" @change="onFileChange" class="form-input" />
          <div v-if="avatar_url" class="avatar-preview">
            <span class="avatar-preview-text">Текущий аватар:</span>
            <a :href="avatar_url" target="_blank" class="link" >{{ avatar_url }}</a>
          </div>
        </div>

        <div class="form-field">
          <label class="form-label">Категории:</label>
          <multiselect
            v-model="form.categories"
            :options="categories"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите категории"
            label="name"
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
        </div>

        <div class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div class="form-field">
          <label for="passing_score" class="form-label">Проходной балл:</label>
          <input v-model="form.passing_score" id="passing_score" type="number" class="form-input" placeholder="Введите проходной балл" />
          <span v-if="errors.passing_score" class="error">{{ errors.passing_score }}</span>
        </div>

        <div class="form-field">
          <label for="time_to_complete" class="form-label">Время на выполнение (минут):</label>
          <input v-model="form.time_to_complete" id="time_to_complete" type="number" class="form-input" placeholder="Введите время в минутах" />
          <span v-if="errors.time_to_complete" class="error">{{ errors.time_to_complete }}</span>
        </div>

        <div class="form-field">
          <label for="attempts" class="form-label">Попытки:</label>
          <input v-model="form.attempts" id="attempts" type="number" class="form-input" placeholder="Введите проходной балл" />
          <span v-if="errors.attempts" class="error">{{ errors.attempts }}</span>
        </div>

        <div class="form-field">
          <label for="random_questions" class="form-label">Случайный порядок вопросов:</label>
          <input v-model="form.random_questions" id="random_questions" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="random_answers" class="form-label">Случайный порядок ответов:</label>
          <input v-model="form.random_answers" id="random_answers" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="show_questions_results" class="form-label">Показывать результаты вопросов:</label>
          <input v-model="form.show_questions_results" id="show_questions_results" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="show_answers_results" class="form-label">Показывать результаты ответов:</label>
          <input v-model="form.show_answers_results" id="show_answers_results" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="desc" class="form-label">Описание:</label>
          <textarea v-model="form.desc" id="desc" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="edit-form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

    <div v-else class="none-card">
      <div>Объект не найден</div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>

</template>

<script setup>

import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  name: '',
  desc: '',
  categories: [],
  passing_score: null,
  time_to_complete: null,
  attempts: null,
  random_questions: true,
  random_answers: true,
  show_questions_results: true,
  show_answers_results: true,
});

const loading = ref(false);

const categories = ref([]);
const loadCategories = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/categories/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    categories.value = response.data.results || [];
    console.log('Категории загружены:', categories.value);
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error.response ? error.response.data : error.message);
  }
};

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/tests/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    Object.assign(form, object.value);
    avatar_url.value = object.value.avatar || '';

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const avatarFile = ref(null);
const avatar_url = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
    avatar_url.value = URL.createObjectURL(file);
  }
};

const errors = reactive({});
const validateForm = () => {
  errors.name = form.name ? '' : 'Название обязательно!';
  errors.passing_score = form.passing_score && form.passing_score > 0 ? '' : 'Задержка обязательна и должна быть больше 0!';
  errors.time_to_complete = form.time_to_complete && form.time_to_complete > 0 ? '' : 'Задержка обязательна и должна быть больше 0!';
  errors.attempts = form.attempts && form.attempts > 0 ? '' : 'Задержка обязательна и должна быть больше 0!';
  return Object.values(errors).every((err) => !err);
};

const saveChanges = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    const id = route.params.id;
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonData = {
      name: form.name,
      desc: form.desc,
      categories: form.categories.map(item => item.id),
      passing_score: form.passing_score,
      attempts: form.attempts,
      time_to_complete: form.time_to_complete,
      random_questions: form.random_questions,
      random_answers: form.random_answers,
      show_questions_results: form.show_questions_results,
      show_answers_results: form.show_answers_results,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/tests/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    if (avatarFile.value) {
      const avatarFormData = new FormData();
      avatarFormData.append('avatar', avatarFile.value);
      const avatarPatchUrl = `${baseUrl}/tests/${id}/`;
      await axios.patch(avatarPatchUrl, avatarFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Аватар успешно обновлен');
    }

    console.log('Изменения сохранены');
    router.push({ name: 'TestDetail', params: { id: id } });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при сохранении изменений:', error.response.data);
    } else {
      console.error('Ошибка при сохранении изменений:', error.message);
    }
  }
};

const cancelEdit = () => {
  router.back();
};


onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadCategories();
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>
