<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание действия</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label class="form-label">Управляющий элемент:</label>
          <multiselect
            v-model="form.control_element"
            :options="control_elements"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите управляющий элемент"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!control_elementId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.control_element" class="error">{{ errors.control_element }}</span>
        </div>

        <div class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Действие:</label>
          <multiselect
            v-model="form.action_type"
            :options="action_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите действие"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.action_type" class="error">{{ errors.action_type }}</span>
        </div>

        <div v-if="form.action_type?.value == 'change_task_status' || form.action_type?.value == 'change_task_outcome' || form.action_type?.value == 'assign_task' || form.action_type?.value ==  'add_task_to_queue'" class="form-field">
          <label class="form-label">Шаблон задачи:</label>
          <multiselect
            v-model="form.task_template"
            :options="filtred_task_templates"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите шаблон задачи"
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
          <span v-if="errors.task_template" class="error">{{ errors.task_template }}</span>
        </div>

        <div v-if="form.action_type?.value == 'change_task_status' || form.action_type?.value == 'change_task_outcome'  || form.action_type?.value == 'add_task_to_queue'" class="form-field">
          <label class="form-label">Целевая задача:</label>
          <multiselect
            v-model="form.target_task"
            :options="target_tasks"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите целевую задачу"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.target_task" class="error">{{ errors.target_task }}</span>
        </div>

        <div v-if="form.action_type?.value == 'change_task_status'" class="form-field">
          <label class="form-label">Статус задачи:</label>
          <multiselect
            v-model="form.task_status"
            :options="task_statuses"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите статус задачи"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.task_status" class="error">{{ errors.task_status }}</span>
        </div>

        <div v-if="form.action_type?.value == 'change_task_outcome'" class="form-field">
          <label class="form-label">Итог задачи:</label>
          <multiselect
            v-model="form.task_outcome"
            :options="task_outcomes"
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
          <span v-if="errors.task_outcome" class="error">{{ errors.task_outcome }}</span>
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label class="form-label">Целевое взаимодействие:</label>
          <multiselect
            v-model="form.target_interaction"
            :options="target_interactions"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите целевое взаимодействие"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.target_interaction" class="error">{{ errors.target_interaction }}</span>
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label class="form-label">Тип исполнителя:</label>
          <multiselect
            v-model="form.executor_type"
            :options="executor_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип исполнителя"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.executor_type" class="error">{{ errors.executor_type }}</span>
        </div>

        <div v-if="form.executor_type?.value == 'selected_executor'" class="form-field">
          <label class="form-label">Исполнитель:</label>
          <multiselect
            v-model="form.executor"
            :options="accounts"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите исполнителя"
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
          <span v-if="errors.executor" class="error">{{ errors.executor }}</span>
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label for="manager_control" class="form-label">Контроль руководителей:</label>
          <input v-model="form.manager_control" id="manager_control" type="checkbox" class="form-input" />
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label class="form-label">Группа контролеров:</label>
          <multiselect
            v-model="form.controller_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу контролеров"
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
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label class="form-label">Группа наблюдателей:</label>
          <multiselect
            v-model="form.observer_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу наблюдателей"
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
        </div>

        <div v-if="form.action_type?.value == 'assign_task'" class="form-field">
          <label class="form-label">Тип задержки:</label>
          <multiselect
            v-model="form.delay_type"
            :options="delay_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип задержки"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.delay_type" class="error">{{ errors.delay_type }}</span>
        </div>

        <div v-if="form.delay_type && form.delay_type.value != 'none'" class="form-field">
          <label for="delay_value" class="form-label">Задержка:</label>
          <input v-model="form.delay_value" id="delay_value" type="number" class="form-input" placeholder="Введите задержку" />
          <span v-if="errors.delay_value" class="error">{{ errors.delay_value }}</span>
        </div>

        <div v-if="form.action_type?.value == 'add_task_to_queue'" class="form-field">
          <label class="form-label">Очередь:</label>
          <multiselect
            v-model="form.queue"
            :options="queues"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите очередь"
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
          <span v-if="errors.queue" class="error">{{ errors.queue }}</span>
        </div>

        <div v-if="form.action_type?.value == 'add_to_group' || form.action_type?.value == 'remove_from_group'" class="form-field">
          <label class="form-label">Целевая группа:</label>
          <multiselect
            v-model="form.target_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите целевую группу"
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
          <span v-if="errors.target_group" class="error">{{ errors.target_group }}</span>
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
import { reactive, onMounted, ref, watch, computed  } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const router = useRouter();
const route = useRoute();

const loading = ref(false);

const action_types = [
  { label: 'Изменить статус задачи', value: 'change_task_status' },
  { label: 'Изменить итог задачи', value: 'change_task_outcome' },
  { label: 'Назначить задачу', value: 'assign_task' },
  { label: 'Добавить задачу в очередь', value: 'add_task_to_queue' },
  { label: 'Новое взаимодействие', value: 'new_interaction' },
  { label: 'Добавить аккаунт взаимодействия в группу', value: 'add_to_group' },
  { label: 'Удалить аккаунт взаимодействия из группы', value: 'remove_from_group' },
];

const task_statuses = [
  { label: 'В ожидании', value: 'waiting' },
  { label: 'Назначена', value: 'assigned' },
  { label: 'В процессе', value: 'in_progress' },
  { label: 'На проверке', value: 'under_review' },
  { label: 'Выполнена', value: 'completed' },
  { label: 'Провалена', value: 'failed' },
  { label: 'Отменена', value: 'canceled' },
];

const target_tasks = [
  { label: 'В рамках текущего взаимодействия', value: 'current' },
  { label: 'В рамках всех взаимодействий', value: 'all' },
];

const target_interactions = [
  { label: 'Текущее', value: 'current' },
  { label: 'Последнее', value: 'last' },
];

const executor_types = [
  { label: 'Текущий исполнитель', value: 'current_executor' },
  { label: 'Выбранный исполнитель', value: 'selected_executor' },
  { label: 'Без исполнителя', value: 'none' },
];

const delay_types = [
  { label: 'Минуты', value: 'minutes' },
  { label: 'Часы', value: 'hours' },
  { label: 'Дни', value: 'days' },
  { label: 'Без задержки', value: 'none' },
];

const form = reactive({
  control_element: null,
  item: null,
  action_type: '',
  task_template: null,
  task_status: '',
  task_outcome: null,
  target_task: '',
  target_group: null,
  target_interaction: '',
  executor_type: '',
  executor: null,
  manager_control: false,
  controller_group: null,
  observer_group: null,
  delay_type: '',
  delay_value: null,
  queue: null,
});
const errors = reactive({});

const control_elements = ref([]);
const loadControlElements = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/control_elements/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    control_elements.value = response.data.results || [];
    console.log('Управлябщие элементы загружены:', control_elements.value);
  } catch (error) {
    console.error('Ошибка при загрузке управлябщих элементов:', error.response ? error.response.data : error.message);
  }
};

const control_elementId = route.query.control_elementId || '';

const loadControlElementById = () => {
  if (control_elementId) {
    console.log('ControlElement ID:', control_elementId);
    const control_element = control_elements.value.find(control_element => control_element.id === parseInt(control_elementId, 10));
    if (control_element) {
      form.control_element = control_element;
    } else {
      console.error('ControlElement не найден.');
    }
  } else {
    console.log('ControlElement ID не найден.');
  }
};

const task_templates = ref([]);
const loadTaskTemplates = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/task_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    task_templates.value = response.data.results || [];
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

const filtred_task_templates = computed(() => {
    if (form.action_type?.value === "assign_task") {
        return task_templates.value.filter(task_template => !task_template.is_child);
    }
    return task_templates.value;
});

const task_outcomes = computed(() => {
  if (control_elements) {
    return control_elements.value.filter(
      control_element => control_element.type_of_work === 'task_outcome'
    );
  }
});

const accounts = ref([]);
const loadAccounts = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/accounts/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    accounts.value = response.data.results || [];
    console.log('Аккаунты загружены:', accounts.value);
  } catch (error) {
    console.error('Ошибка при загрузке сотрудников:', error.response ? error.response.data : error.message);
  }
};

const groups = ref([]);
const loadGroups = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/account_groups/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    groups.value = response.data.results || [];
    console.log('Группы загружены:', groups.value);
  } catch (error) {
    console.error('Ошибка при загрузке групп:', error.response ? error.response.data : error.message);
  }
};

const queues = ref([]);
const loadQueues = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/queues/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    queues.value = response.data.results || [];
    console.log('Очереди загружены:', queues.value);
  } catch (error) {
    console.error('Ошибка при загрузке очередей:', error.response ? error.response.data : error.message);
  }
};

watch(
  () => form.action_type,
  (newValue, oldValue) => {
    if (newValue.value != 'change_task_status' && newValue.value != 'change_task_outcome' && newValue.value != 'add_task_to_queue') {
      form.target_task = '';
    }
    if (newValue.value != 'change_task_status') {
      form.task_status = '';
    }
    if (newValue.value != 'change_task_outcome') {
      form.task_outcome = null;
    }
    if ((newValue && oldValue) && newValue.value == 'assign_task') {
      form.task_template = null;
    }
    if (newValue.value != 'assign_task') {
      form.target_interaction = '';
      form.executor_type = '';
      form.executor = null;
      form.controller_group = null;
      form.observer_group = null;
      form.delay_type = '';
      form.delay_value = null;
    }
    if (newValue.value != 'add_task_to_queue') {
      form.queue = null;
    }
    if (newValue.value != 'add_to_group' && newValue.value != 'remove_from_group') {
      form.target_group = null;
    }
  }
);

watch(
  () => form.executor_type,
  (newValue) => {
    if (newValue.value == 'none' || newValue.value == 'current_executor') {
      form.executor = null;
    }
  }
);

watch(
  () => form.delay_type,
  (newValue) => {
    if (newValue?.value == 'none') {
      form.delay_value = null;
    }
  }
);

const validateForm = () => {
  errors.control_element = form.control_element ? '' : 'Управляющий элемент обязателен';
  errors.action_type = form.action_type.value ? '' : 'Действие обязательно!';
  errors.item = form.item && form.item > 0 ? '' : 'Пункт обязателен и должен быть больше 0!';
  if (form.condition_type == 'change_task_status') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.target_task = form.target_task ? '' : 'Целевая задача обязательна!';
    errors.task_status = form.task_status.value ? '' : 'Статус задачи обязателен!';
  }
  if (form.condition_type == 'change_task_outcome') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.target_task = form.target_task ? '' : 'Целевая задача обязательна!';
    errors.task_outcome = form.task_outcome ? '' : 'Итог задачи обязателен!';
  }
  if (form.condition_type == 'assign_task') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.target_interaction = form.target_interaction ? '' : 'Целевое взаимодействие обязательно!';
    errors.executor_type = form.executor_type ? '' : 'Тип исполнителя обязателен!';
    if (form.executor_type?.value == 'selected_executor') {
      errors.executor = form.executor ? '' : 'Выбор исполнителя обязателен!';
    }
    errors.delay_type = form.delay_type ? '' : 'Тип задержки обязателен!';
    if (form.delay_type?.value != 'none') {
      errors.delay_value = form.delay_value && form.delay_value > 0 ? '' : 'Задержка обязательна и должна быть больше 0!';
    }
  }
  if (form.condition_type == 'add_task_to_queue') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.target_task = form.target_task ? '' : 'Целевая задача обязательна!';
    errors.queue = form.queue ? '' : 'Очередь обязательна!';
  }
  if (form.condition_type == 'add_to_group' || form.condition_type == 'remove_from_group') {
    errors.target_group = form.target_group ? '' : 'Целевая группа обязательна!';
  }

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
      control_element: form.control_element.id,
      item: form.item,
      action_type: form.action_type.value,
      task_template: form.task_template?.id || null,
      task_status: form.task_status?.value || '',
      task_outcome: form.task_outcome?.id || null,
      target_interaction: form.target_interaction?.value || '',
      target_task: form.target_task?.value || '',
      target_group: form.target_group?.id || null,
      executor_type: form.executor_type?.value || '',
      executor: form.executor?.id || null,
      manager_control: form.manager_control,
      controller_group: form.controller_group?.id || null,
      observer_group: form.observer_group?.id || null,
      delay_type: form.delay_type?.value || '',
      delay_value: form.delay_value,
      queue: form.queue?.id || null,
    };
    const control_elementId = form.control_element.id

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/control_element_actions/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);
    router.push({ name: 'ControlElementDetail', params: { id: control_elementId }  });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }
};

const cancelEdit = () => {
  const control_elementId = form.control_element.id
  router.push({ name: 'ControlElementDetail', params: { id: control_elementId } });
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadControlElements();
    await loadControlElementById();
    await loadTaskTemplates();
    await loadAccounts();
    await loadGroups();
    await loadQueues();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>
