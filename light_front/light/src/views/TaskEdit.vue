<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование задачи</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label for="is_child" class="form-label">Дочерняя:</label>
          <input v-model="form.is_child" id="is_child" type="checkbox" class="form-input" :disabled="!!planId" />
        </div>

        <div v-if="form.is_child" class="form-field">
          <label class="form-label">План:</label>
          <multiselect
            v-model="form.plan"
            :options="plans"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите план"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!planId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.plan" class="error">{{ errors.plan }}</span>
        </div>

        <div v-if="form.is_child" class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Тип задачи:</label>
          <multiselect
            v-model="form.task_type"
            :options="task_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип задачи"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.task_type" class="error">{{ errors.task_type }}</span>
        </div>

        <div v-if="form.task_type.value == 'news_reading'" class="form-field">
          <label class="form-label">Новость:</label>
          <multiselect
            v-model="form.new"
            :options="news"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите новость"
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
          <span v-if="errors.new" class="error">{{ errors.new }}</span>
        </div>

        <div v-if="form.task_type.value == 'material_review'" class="form-field">
          <label class="form-label">Материал:</label>
          <multiselect
            v-model="form.material"
            :options="materials"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите материал"
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
          <span v-if="errors.material" class="error">{{ errors.material }}</span>
        </div>

        <div v-if="form.task_type.value == 'course_study'" class="form-field">
          <label class="form-label">Курс:</label>
          <multiselect
            v-model="form.course"
            :options="courses"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите курс"
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
          <span v-if="errors.course" class="error">{{ errors.course }}</span>
        </div>

        <div v-if="form.task_type.value == 'test_taking'" class="form-field">
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

        <div v-if="form.task_type.value == 'event_participation'" class="form-field">
          <label class="form-label">Мероприятие:</label>
          <multiselect
            v-model="form.event_template"
            :options="event_templates"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите мероприятие"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!form.slot_select"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.event_template" class="error">{{ errors.event_template }}</span>
        </div>

        <div v-if="form.task_type.value == 'event_participation' && !form.slot_select" class="form-field">
          <label class="form-label">Слот мероприятия:</label>
          <multiselect
            v-model="form.event_slot"
            :options="event_slots"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите слот мероприятия"
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
          <span v-if="errors.event_slot" class="error">{{ errors.event_slot }}</span>
        </div>

        <div class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div class="form-field form-field-full_width">
          <label for="desc" class="form-label">Содержание:</label>
          
          <EditorComponent v-model="form.manual" />

          <span v-if="errors.manual" class="error">{{ errors.manual }}</span>
        </div>

        <div class="form-field">
          <label for="desc" class="form-label">Описание:</label>
          <textarea v-model="form.desc" id="desc" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
        </div>

        <div v-if="form.task_type?.value == 'common_task' || form.task_type?.value == 'plan_implementation'" class="form-field">
          <label for="require_review" class="form-label">Требуется проверка:</label>
          <input v-model="form.require_review" id="require_review" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="task_outcome" class="form-label">Итог задачи:</label>
          <input v-model="form.task_outcome" id="task_outcome" type="checkbox" class="form-input" />
        </div>
        
        <div class="form-field">
          <label for="planned_start" class="form-label">Начало по плану:</label>
          <input v-model="form.planned_start" id="planned_start" type="datetime-local" class="form-input" />
          <span v-if="errors.planned_start" class="error">{{ errors.planned_start }}</span>
        </div>

        <div class="form-field">
          <label for="deadline" class="form-label">Сроки:</label>
          <input v-model="form.deadline" id="deadline" type="checkbox" class="form-input" />
        </div>

        <div v-if="form.deadline" class="form-field">
          <label for="planned_end" class="form-label">Завершение по плану:</label>
          <input v-model="form.planned_end" id="planned_end" type="datetime-local" class="form-input" />
          <span v-if="errors.planned_end" class="error">{{ errors.planned_end }}</span>
        </div>

        <div class="form-field">
          <label for="waiting" class="form-label">Ожидает активации:</label>
          <input v-model="form.waiting" id="waiting" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
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

        <div class="form-field">
          <label class="form-label">Соисполнители:</label>
          <multiselect
            v-model="form.co_executors"
            :options="accounts"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите соисполнителей"
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

        <div class="form-field">
          <label class="form-label">Контролеры:</label>
          <multiselect
            v-model="form.controllers"
            :options="accounts"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите конролеров"
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

        <div class="form-field">
          <label class="form-label">Наблюдатели:</label>
          <multiselect
            v-model="form.observers"
            :options="accounts"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите наблюдателей"
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

        <div class="form-field">
          <label class="form-label">Взаимодействие:</label>
          <multiselect
            v-model="form.interaction"
            :options="interactions"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите взаимодействие"
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
          <span v-if="errors.interaction" class="error">{{ errors.interaction }}</span>
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

import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { formatDate, formatDateTime, baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  interaction: null,
  is_child: false,
  plan: null,
  item: null,
  task_type: '',
  material: null,
  new: null,
  course: null,
  test: null,
  slot_select: true,
  event_template: null,
  event_slot: null,
  name: '',
  manual: '',
  desc: '',
  require_review: false,
  deadline: false,
  planned_start: null,
  planned_end: null,
  waiting: false,
  executor: null,
  co_executors: [],
  controllers: [],
  observers: [],
  task_outcome: false,
  categories: [],
});

const loading = ref(false);

const task_types = [
  { label: 'Обычная задача', value: 'common_task' },
  { label: 'Реализация плана', value: 'plan_implementation' },
  { label: 'Чтение новостей', value: 'news_reading' },
  { label: 'Ознакомление с материалом', value: 'material_review' },
  { label: 'Прохождение теста', value: 'test_taking' },
  { label: 'Изучение курса', value: 'course_study' },
  { label: 'Участие в мероприятии', value: 'event_participation' },
];

const interactions = ref([]);
const loadInteractions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/interactions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    interactions.value = response.data.results || [];
    console.log('Взаимодействия загружены:', interactions.value);
  } catch (error) {
    console.error('Ошибка при загрузке взимодействий:', error.response ? error.response.data : error.message);
  }
};


const tasks = ref([]);
const plans = ref([]);
const loadPlans = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/tasks/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    tasks.value = response.data.results || [];
    console.log('Задачи загружены:', tasks.value);
    plans.value = tasks.value.filter(task => task.task_type === 'plan_implementation')
    console.log('Планы загружены:', plans.value);
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error.response ? error.response.data : error.message);
  }
};

const planId = route.query.planId || '';

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

const materials = ref([]);
const loadMaterials = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/materials/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    materials.value = response.data.results || [];
    console.log('Материалы загружены:', materials.value);
  } catch (error) {
    console.error('Ошибка при загрузке материалов:', error.response ? error.response.data : error.message);
  }
};

const news = ref([]);
const loadNews = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/news/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    news.value = response.data.results || [];
    console.log('Новости загружены:', news.value);
  } catch (error) {
    console.error('Ошибка при загрузке новостей:', error.response ? error.response.data : error.message);
  }
};

const courses = ref([]);
const loadCourses = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/courses/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    courses.value = response.data.results || [];
    console.log('Курсы загружены:', courses.value);
  } catch (error) {
    console.error('Ошибка при загрузке курсов:', error.response ? error.response.data : error.message);
  }
};

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
    console.log('Тесты загружены:', tests.value);
  } catch (error) {
    console.error('Ошибка при загрузке тестов:', error.response ? error.response.data : error.message);
  }
};

const event_templates = ref([]);
const loadEventTemplates = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/event_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    event_templates.value = response.data.results || [];
    console.log('Мероприятия загружены:', event_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке мероприятий:', error.response ? error.response.data : error.message);
  }
};

const event_slots = ref([]);
const loadEventSlots = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/event_slots/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    event_slots.value = response.data.results || [];
    console.log('Слоты мероприятий загружены:', event_slots.value);
  } catch (error) {
    console.error('Ошибка при загрузке слотов мероприятий:', error.response ? error.response.data : error.message);
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
    const response = await axios.get(`${baseUrl}/tasks/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    object.value.task_type = task_types.find(option => option.value === object.value.task_type);
    object.value.planned_start = object.value.planned_start.slice(0, 16)
    if (object.value.planned_end) {
      object.value.planned_end = object.value.planned_end.slice(0, 16)
    }
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);
  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

watch(
  () => form.is_child,
  (newValue) => {
    if (newValue == false) {
      form.plan = null;
      form.item = null;
    }
  }
);

watch(
  () => form.task_type,
  (newValue) => {
    if (newValue.value != 'common_task' && newValue.value != 'plan_implementation') {
      form.require_review = false;
    }
    if (newValue.value != 'news_reading') {
      form.new = null;
    }
    if (newValue.value != 'material_review') {
      form.material = null;
    }
    if (newValue.value != 'course_study') {
      form.course = null;
    }
    if (newValue.value != 'test_taking') {
      form.test = null;
    }
    if (newValue.value != 'event_participation') {
      form.event_template = null;
      form.event_slot = null;
      form.slot_select = false;
    }
  }
);

watch(
  () => form.slot_select,
  (newValue) => {
    if (newValue == true) {
      form.event_slot = null;
    }
  }
);

watch(
  () => form.event_slot,
  (newValue) => {
    if (newValue && newValue.event_template) {
      form.event_template = event_templates.value.find(
        option => option.id === newValue.event_template
      );
    }
  }
);

watch(
  () => form.deadline,
  (newValue) => {
    if (newValue == false) {
      form.planned_end = null;
    }
  }
);

const errors = reactive({});
const validateForm = () => {
  errors.interaction = form.interaction ? '' : 'Выбор взаимодейтсвия обязателен!';
  if (form.is_child) {
    errors.stage = form.plan ? '' : 'Выбор плана обязателен!';
    errors.item = form.item ? '' : 'Порядок пункта обязателен!';
  }
  errors.task_type = form.task_type.value ? '' : 'Тип задачи обязателен!';
  if (form.task_type == 'common_task' || form.task_type == 'plan_implementation') {
    errors.manual = form.manual.trim() ? '' : 'Содержание обязательно!';
  }
  if (form.task_type.value == 'news_reading') {
    errors.new = form.new ? '' : 'Новость обязательна!';
  }
  if (form.task_type.value == 'material_review') {
    errors.material = form.material ? '' : 'Материал обязателен!';
  }
  if (form.task_type.value == 'course_study') {
    errors.course = form.course ? '' : 'Курс обязателен!';
  }
  if (form.task_type.value == 'test_taking') {
    errors.test = form.test ? '' : 'Тест обязателен!';
  }
  if (form.task_type.value == 'event_participation') {
    if (form.slot_select == true) {
    errors.event_template = form.event_template ? '' : 'Мероприятие обязательно!';
    }
    if (form.slot_select == false) {
      errors.event_slot = form.event_slot ? '' : 'Слот мероприятия обязателен!';
    }
  }
  errors.name = form.name ? '' : 'Название обязательно!';
  errors.planned_start = form.planned_start ? '' : 'Выбор начала обязателен';
  if (form.deadline) {
    errors.planned_end = form.planned_end ? '' : 'Выбор завершения обязателен';
  }
  errors.executor = form.executor ? '' : 'Выбор исполнителя обязателен!';
  return Object.values(errors).every((error) => !error);
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
      interaction: form.interaction?.id,
      is_child: form.is_child,
      plan: form.plan?.id,
      item: form.item,
      task_type: form.task_type.value,
      material: form.material?.id,
      new: form.new?.id,
      course: form.course?.id,
      test: form.test?.id,
      slot_select: form.slot_select,
      event_template: form.event_template?.id,
      event_slot: form.event_slot?.id,
      manual: form.manual || "",
      desc: form.desc,
      require_review: form.require_review,
      name: form.name,
      deadline: form.deadline,
      planned_start: form.planned_start,
      planned_end: form.planned_end,
      waiting: form.waiting,
      executor: form.executor?.id,
      co_executors: form.co_executors.map(item => item.id),
      controllers: form.controllers.map(item => item.id),
      observers: form.observers.map(item => item.id),
      task_outcome: form.task_outcome,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/tasks/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    const planId = route.query.planId || '';
    if (planId){
      router.push({ name: 'TaskDetail', params: { id: planId }  });
    } else {
      router.push({ name: 'TaskDetail', params: { id: id } });
    }

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
    await loadInteractions();
    await loadPlans();
    await loadAccounts();
    await loadCategories();
    await loadMaterials();
    await loadNews();
    await loadCourses();
    await loadTests();
    await loadEventTemplates();
    await loadEventSlots();
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});



</script>
