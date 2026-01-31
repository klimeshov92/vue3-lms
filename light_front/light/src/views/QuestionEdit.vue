<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование вопрос</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label class="form-label">Тип вопроса:</label>
          <multiselect
            v-model="form.question_type"
            :options="question_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип вопроса"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.question_type" class="error">{{ errors.question_type }}</span>
        </div>
        
        <div class="form-field">
          <label for="manual" class="form-label">Инструкция:</label>
          <textarea v-model="form.manual" id="manual" class="form-input" rows="3" placeholder="Введите иструкцию" ></textarea>
          <span v-if="errors.manual" class="error">{{ errors.manual }}</span>
        </div>

        <div class="form-field">
          <label for="text" class="form-label">Текст вопроса:</label>
          <textarea v-model="form.text" id="text" class="form-input" rows="3" placeholder="Введите текст вопроса" ></textarea>
          <span v-if="errors.text" class="error">{{ errors.text }}</span>
        </div>

        <div class="form-field">
          <label for="picture" class="form-label">Картинка:</label>
          <input type="file" id="picture" @change="onFileChange" class="form-input" />
          <div v-if="picture_url" class="avatar-preview">
            <span class="avatar-preview-text">Текущий аватар:</span>
            <a :href="picture_url" target="_blank" class="link" >{{ picture_url }}</a>
          </div>
        </div>

        <div class="form-field">
          <label for="score" class="form-label">Баллы:</label>
          <input v-model="form.score" id="score" type="number" class="form-input" placeholder="Введите баллы" />
          <span v-if="errors.score" class="error">{{ errors.score }}</span>
        </div>

        <div class="form-field">
          <label for="feedback_for_correct" class="form-label">Обратная связь при правильном ответе:</label>
          <textarea v-model="form.feedback_for_correct" id="feedback_for_correct" class="form-input" rows="3" placeholder="Введите обратную связь при правильном ответе" ></textarea>
          <span v-if="errors.feedback_for_correct" class="error">{{ errors.feedback_for_correct }}</span>
        </div>

        <div class="form-field">
          <label for="feedback_for_incorrect" class="form-label">Обратная связь при неправильном ответе:</label>
          <textarea v-model="form.feedback_for_incorrect" id="feedback_for_incorrect" class="form-input" rows="3" placeholder="Введите обратную связь при неправильном ответе" ></textarea>
          <span v-if="errors.feedback_for_incorrect" class="error">{{ errors.feedback_for_incorrect }}</span>
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  question_type: '',
  manual: '',
  text: '',
  score: null,
  feedback_for_correct: '',
  feedback_for_incorrect: '',
  categories: [],
});

const loading = ref(false);

const question_types = [
  { label: 'Одиночный выбор', value: 'single_selection' },
  { label: 'Множественный выбор', value: 'multiple_choice' },
  { label: 'Сортировка', value: 'sorting' },
  { label: 'Соотвествие', value: 'compliance' },
  { label: 'Текстовый ввод', value: 'text_input' },
  { label: 'Числовой ввод', value: 'numeric_input' },
];

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
    const response = await axios.get(`${baseUrl}/questions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    object.value.question_type = question_types.find(option => option.value === object.value.question_type);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);
    picture_url.value = object.value.picture || '';

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const pictureFile = ref(null);
const picture_url = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    pictureFile.value = file;
    picture_url.value = URL.createObjectURL(file);
  }
};

const errors = reactive({});
const validateForm = () => {
  errors.question_type = form.question_type.value ? '' : 'Тип задачи обязателен!';
  errors.manual = form.manual ? '' : 'Инструкция обязательна!';
  errors.text = form.text ? '' : 'Текст вопроса обязателен!';
  errors.score = form.score != undefined ? '' : 'Баллы обязательны!';
  errors.feedback_for_correct = form.feedback_for_correct ? '' : 'Обратная связь при правильном ответе обязательна!';
  errors.feedback_for_incorrect = form.feedback_for_incorrect ? '' : 'Обратная связь при неправильном ответе обязательна!';
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
      question_type: form.question_type.value,
      manual: form.manual,
      text: form.text,
      score: form.score,
      feedback_for_correct: form.feedback_for_correct,
      feedback_for_incorrect: form.feedback_for_incorrect,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/questions/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    if (pictureFile.value) {
      const pictureFormData = new FormData();
      pictureFormData.append('picture', pictureFile.value);
      const picturePatchUrl = `${baseUrl}/questions/${id}/`;
      await axios.patch(picturePatchUrl, pictureFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Картинка успешно обновлена');
    }

    console.log('Изменения сохранены');
    router.push({ name: 'QuestionDetail', params: { id: id } });
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
  goBackSmart(router);
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
