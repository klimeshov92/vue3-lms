<template>

  <div v-if="loading">

    <div class="form-page">

      <div class="form-header">
        <h1>Создание ответа</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        
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
            :disabled="!!questionId"
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

        <div class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label for="text" class="form-label">Текст ответа:</label>
          <textarea v-model="form.text" id="text" class="form-input" rows="3" placeholder="Введите текст ответа" ></textarea>
          <span v-if="errors.text" class="error">{{ errors.text }}</span>
        </div>

        <div class="form-field">
          <label for="picture" class="form-label">Картинка:</label>
          <input type="file" id="picture" @change="onFileChange" class="form-input" />
        </div>

        <div class="form-field">
          <label for="score" class="form-label">Баллы:</label>
          <input v-model="form.score" id="score" type="number" class="form-input" placeholder="Введите баллы" />
          <span v-if="errors.score" class="error">{{ errors.score }}</span>
        </div>

        <div v-if="form.question?.question_type == 'single_selection' || form.question?.question_type == 'multiple_choice'" class="form-field">
          <label for="correct_answer" class="form-label">Правильный ответ:</label>
          <input v-model="form.correct_answer" id="correct_answer" type="checkbox" class="form-input" />
        </div>

        <div v-if="form.question?.question_type == 'sorting'" class="form-field">
          <label for="correct_item" class="form-label">Правильный пункт:</label>
          <input v-model="form.correct_item" id="correct_item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.correct_item" class="error">{{ errors.correct_item }}</span>
        </div>

        <div v-if="form.question?.question_type == 'text_input'" class="form-field">
          <label for="correct_text_input" class="form-label">Правильный ответ:</label>
          <input v-model="form.correct_text_input" id="correct_text_input" type="text" class="form-input" placeholder="Введите правильный ответ" required />
          <span v-if="errors.correct_text_input" class="error">{{ errors.correct_text_input }}</span>
        </div>

        <div v-if="form.question?.question_type == 'numeric_input'" class="form-field">
          <label for="correct_numeric_input" class="form-label">Правильный ответ:</label>
          <input v-model="form.correct_numeric_input" id="correct_numeric_input" type="number" class="form-input" placeholder="Введите правильный ответ" />
          <span v-if="errors.correct_numeric_input" class="error">{{ errors.correct_numeric_input }}</span>
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
import { reactive, onMounted, ref, watch } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  question: null,
  item: null,
  text: '',
  score: null,
  correct_answer: false,
  correct_item: null,
  correct_text_input: '',
  correct_numeric_input: null,
  feedback_for_correct: 'Верно!',
  feedback_for_incorrect: 'Неверно!',
});

const loading = ref(false);

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

const questionId = route.query.questionId || '';
const loadQuestionById = () => {
  if (questionId) {
    console.log('Question ID:', questionId);
    const question = questions?.value.find(question => question.id === parseInt(questionId, 10));
    if (question) {
      form.question = question;
    } else {
      console.error('Question не найден.');
    }
  } else {
    console.log('Question ID не найден.');
  }
};

const pictureFile = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    pictureFile.value = file;
  }
};

watch(
  () => form.question,
  (newValue) => {
    if (newValue?.question_type != 'single_selection' && newValue?.question_type != 'multiple_choice' ) {
      form.correct_answer = false
    }
    if (newValue?.question_type != 'sorting') {
      form.correct_item = null
    }
    if (newValue?.question_type != 'text_input') {
      form.correct_text_input = ''
    }
    if (newValue?.question_type != 'numeric_input') {
      form.correct_numeric_input = null
    }
  }
);

const cancelEdit = () => {
  router.back();
};

const errors = reactive({});
const validateForm = () => {
  errors.question = form.question ? '' : 'Выбор вопроса обязателен!';
  errors.item = form.item && form.item > 0 ? '' : 'Пункт обязателен и должен быть больше 0!';
  if (form.question?.question_type != 'text_input' && form.question?.question_type != 'numeric_input') {
    errors.text = form.text ? '' : 'Текст ответа обязателен!';
  }
  errors.score = form.score != undefined ? '' : 'Баллы обязательны!';

  if (form.question?.question_type == 'sorting') {
    errors.correct_item = form.correct_item && form.correct_item > 0 ? '' : 'Правильный пункт обязателен и должен быть больше 0!';
  } else if (form.question?.question_type == 'text_input') {
    errors.correct_text_input = form.correct_text_input ? '' : 'Правильный ответ обязателен!';
  } else if (form.question?.question_type == 'numeric_input') {
    errors.correct_numeric_input = form.correct_numeric_input ? '' : 'Правильный ответ обязателен!';
  }

  errors.feedback_for_correct = form.feedback_for_correct ? '' : 'Обратная связь при правильном ответе обязательна!';
  errors.feedback_for_incorrect = form.feedback_for_incorrect ? '' : 'Обратная связь при неправильном ответе обязательна!';
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
      question: form.question?.id,
      item: form.item,
      text: form.text,
      score: form.score,
      correct_answer: form.correct_answer,
      correct_item: form.correct_item,
      correct_text_input: form.correct_text_input,
      correct_numeric_input: form.correct_numeric_input,
      feedback_for_correct: form.feedback_for_correct,
      feedback_for_incorrect: form.feedback_for_incorrect,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/answers/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    if (pictureFile.value) {
      const pictureFormData = new FormData();
      pictureFormData.append('picture', pictureFile.value);

      const picturePatchUrl = `${baseUrl}/answers/${jsonResponse.data.id}/`;
      const picturePatchResponse = await axios.patch(picturePatchUrl, pictureFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Картинка успешно обновлена:', picturePatchResponse.data);
    }

    router.push({ name: 'QuestionDetail', params: { id: jsonResponse.data.question }  });
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
    await loadQuestions();
    await loadQuestionById();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
