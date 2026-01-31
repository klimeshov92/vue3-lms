<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование чата</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label class="form-label">Тип чата:</label>
          <multiselect
            v-model="form.topic_type"
            :options="topic_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип чата"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.topic_type" class="error">{{ errors.topic_type }}</span>
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

        <div v-if="form.topic_type?.value == 'task_topic'" class="form-field">
          <label class="form-label">Задача:</label>
          <multiselect
            v-model="form.task"
            :options="tasks"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите задачу"
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
          <span v-if="errors.task" class="error">{{ errors.task }}</span>
        </div>

        <div v-if="form.topic_type?.value == 'queue_topic'" class="form-field">
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


        <div v-if="form.topic_type?.value == 'public_plan_topic'" class="form-field">
          <label class="form-label">План:</label>
          <multiselect
            v-model="form.public_plan"
            :options="public_plans"
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
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.public_plan" class="error">{{ errors.public_plan }}</span>
        </div>

        <div v-if="form.topic_type?.value == 'public_task_topic'" class="form-field">
          <label class="form-label">План:</label>
          <multiselect
            v-model="form.public_task"
            :options="public_tasks"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите задание"
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
          <span v-if="errors.public_task" class="error">{{ errors.public_task }}</span>
        </div>

        <div v-if="form.topic_type?.value == 'new_topic'" class="form-field">
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

        <div v-if="form.topic_type?.value == 'material_topic'" class="form-field">
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

        <div v-if="form.topic_type?.value == 'course_topic'" class="form-field">
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

        <div v-if="form.topic_type?.value == 'test_topic'" class="form-field">
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

        <div v-if="form.topic_type?.value == 'event_template_topic'" class="form-field">
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

        <div v-if="form.topic_type?.value == 'event_slot_topic'" class="form-field">
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

import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  topic_type: '',
  task: null,
  queue: null,
  public_plan: null,
  public_task: null,
  material: null,
  new: null,
  course: null,
  test: null,
  event_template: null,
  event_slot: null,
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const topic_types = [
  { label: 'Обычный топик', value: 'common_topic' },
  { label: 'Топик задачи', value: 'task_topic' },
  { label: 'Топик очереди', value: 'queue_topic' },
  { label: 'Топик задачи', value: 'task_topic' },
  { label: 'Топик плана', value: 'public_plan_topic' },
  { label: 'Топик задания', value: 'public_task_topic' },
  { label: 'Топик новости', value: 'new_topic' },
  { label: 'Топик материала', value: 'material_topic' },
  { label: 'Топик курса', value: 'course_topic' },
  { label: 'Топик теста', value: 'test_topic' },
  { label: 'Топик мероприятия', value: 'event_template_topic' },
  { label: 'Топик слота мероприятия', value: 'event_slot_topic' },
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

const tasks = ref([]);
const loadTasks = async () => {
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
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error.response ? error.response.data : error.message);
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


const public_plans = ref([]);
const loadPablicPlans = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/public_plans/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    public_plans.value = response.data.results || [];
    console.log('Планы загружены:', public_plans.value);
  } catch (error) {
    console.error('Ошибка при загрузке материалов:', error.response ? error.response.data : error.message);
  }
};

const public_tasks = ref([]);
const loadPablicTasks = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/public_tasks/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    public_tasks.value = response.data.results || [];
    console.log('Задания загружены:', public_tasks.value);
  } catch (error) {
    console.error('Ошибка при загрузке материалов:', error.response ? error.response.data : error.message);
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
    const response = await axios.get(`${baseUrl}/topics/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    object.value.topic_type = topic_types.find(option => option.value === object.value.topic_type);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);
  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

watch(
  () => form.topic_type,
  (newValue) => {
    if (newValue.value != 'task_topic') {
      form.task = null;
    }
    if (newValue.value != 'queue_topic') {
      form.queue = null;
    }
    if (newValue.value != 'public_plan_topic') {
      form.public_plan = null;
    }
    if (newValue.value != 'public_task_topic') {
      form.public_task = null;
    }
    if (newValue.value != 'new_topic') {
      form.new = null;
    }
    if (newValue.value != 'material_topic') {
      form.material = null;
    }
    if (newValue.value != 'course_topic') {
      form.course = null;
    }
    if (newValue.value != 'test_topic') {
      form.test = null;
    }
    if (newValue.value != 'event_template_topic') {
      form.event_template = null;
    }
    if (newValue.value != 'event_slot_topic') {
      form.event_slot = null;
    }
  }
);

const errors = reactive({});
const validateForm = () => {
  errors.name = form.name ? '' : 'Название обязательно!';
  if (form.topic_type == 'task_topic') {
    errors.task = form.task ? '' : 'Задача обязательна!';
  }
  if (form.topic_type == 'queue_topic') {
    errors.queue = form.queue ? '' : 'Очередь обязательна!';
  }
  if (form.topic_type == 'public_plan_topic') {
    errors.public_plan = form.public_plan ? '' : 'План обязателен!';
  }
  if (form.topic_type == 'public_task_topic') {
    errors.public_task = form.public_task ? '' : 'Задание обязательно!';
  }
  if (form.topic_type == 'new_topic') {
    errors.new = form.new ? '' : 'Новость обязательна!';
  }
  if (form.topic_type == 'material_topic') {
    errors.material = form.material ? '' : 'Материал обязателен!';
  }
  if (form.topic_type == 'course_topic') {
    errors.course = form.course ? '' : 'Курс обязателен!';
  }
  if (form.topic_type == 'test_topic') {
    errors.test = form.test ? '' : 'Тест обязателен!';
  }
  if (form.topic_type == 'event_template_topic') {
    errors.event_template = form.event_template ? '' : 'Мероприятие обязательно!';
  }
  if (form.topic_type == 'event_slot_topic') {
    errors.event_slot = form.event_slot ? '' : 'Слот обязателен!';
  }
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
      topic_type: form.topic_type.value,
      task: form.task?.id,
      queue: form.queue?.id,
      public_plan: form.public_plan?.id,
      public_task: form.public_task?.id,
      new: form.new?.id,
      material: form.material?.id, 
      course: form.course?.id,
      test: form.test?.id,
      event_template: form.event_template?.id,
      event_slot: form.event_slot?.id, 
      name: form.name,
      desc: form.desc,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/topics/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

  console.log('Данные обновлены');
  router.push({ name: 'TopicDetail', params: { id: id }  });

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
    await loadTasks();
    await loadQueues();
    await loadPablicPlans();
    await loadPablicTasks();
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
