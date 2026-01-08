<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Результат плана</h1>
      </div>

      <form @submit.prevent="saveChanges" class="modal-form" id="edit-form">

        <div class="form-field">
          <label class="form-label">Статус:</label>
          <multiselect
            v-model="form.status"
            :options="statuses"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите статус"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.status" class="error">{{ errors.status }}</span>
        </div>

        <div v-if="object?.task?.task_outcome" class="form-field">
          <label class="form-label">Итог задачи:</label>
          <multiselect
            v-model="form.outcome"
            :options="outcomes"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите итог задачи"
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
          <span v-if="errors.outcome" class="error">{{ errors.outcome }}</span>
        </div>

      </form>

      <div class="button-group modal-menu">
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

import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  task: null,
  status: '',
  outcome: null,
});

const loading = ref(false);


const outcomes = ref([]);
const role = ref();
const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/plan_result_update/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    outcomes.value = object.value.outcomes
    console.log(`Итоги задачи:`, outcomes.value);
    if (object.value.task.controllers.some(user => user == validToken.user_id)) {
      role.value = 'controller';
    } else if  (object.value.task.executor == validToken.user_id || object.value.task.co_executors.some(user => user.id == validToken.user_id)) {
      role.value = 'executor';
    }
    console.log(`Роль:`, role.value);

    object.value.status = statuses.value.find(option => option.value === object.value.status);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);
  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const statuses = computed(() => [
  !object.value.task.require_review || role.value == 'controller' ? { label: 'В ожидании', value: 'waiting' } : null,
  !object.value.task.require_review || role.value == 'controller' ? { label: 'Назначено', value: 'assigned' } : null,
  { label: 'В процессе', value: 'in_progress' },
  { label: 'На проверке', value: 'under_review' },
  !object.value.task.require_review || role.value == 'controller' ? { label: 'Выполнено', value: 'completed' } : null,
  !object.value.task.require_review || role.value == 'controller' ? { label: 'Провалено', value: 'failed' } : null,
  !object.value.task.require_review || role.value == 'controller' ? { label: 'Отменено', value: 'canceled' } : null,
  !object.value.task.require_review || role.value == 'controller' ? { name: 'desc', label: 'Описание' } : null,
].filter(Boolean));

const errors = reactive({});
const validateForm = () => {
  errors.status = form.status.value ? '' : 'Статус задачи обязателен!';
  return Object.values(errors).every((error) => !error);
};

const saveChanges = async () => {
  const id = route.params.id;
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonData = {
      status: form.status.value,
      outcome: form.outcome?.id || null,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/plan_result_update/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');
    
    router.push({ name: 'TaskDetail', params: { id: id } });

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
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});



</script>
