<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание шаблона задачи</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label for="is_child" class="form-label">Дочерняя:</label>
          <input v-model="form.is_child" id="is_child" type="checkbox" class="form-input" :disabled="!!planId" />
        </div>

        <div  v-if="form.is_child" class="form-field">
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

        <div v-if="form.is_child" class="form-field">
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
          <label for="slot_select" class="form-label">Выбор слота:</label>
          <input v-model="form.slot_select" id="slot_select" type="checkbox" class="form-input" />
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
          <label class="form-label">Тип срока:</label>
          <multiselect
            v-model="form.term_type"
            :options="term_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип срока"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.term_type" class="error">{{ errors.term_type }}</span>
        </div>

        <div v-if="form.term_type && form.term_type.value != 'none'" class="form-field">
          <label for="term_value" class="form-label">Срок:</label>
          <input 
            v-model="form.term_value" 
            id="term_value" 
            type="number" 
            class="form-input" 
            placeholder="Введите срок"
          />
          <span v-if="errors.term_value" class="error">{{ errors.term_value }}</span>
        </div>

        <div class="form-field">
          <label for="waiting" class="form-label">Ожидает активации:</label>
          <input v-model="form.waiting" id="waiting" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="self_assignment" class="form-label">Самоназначение:</label>
          <input v-model="form.self_assignment" id="self_assignment" type="checkbox" class="form-input" />
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const form = reactive({
  is_child: false,
  plan: null,
  item: null,
  delay_type: '',
  delay_value: null,
  task_type: '',
  material: null,
  new: null,
  course: null,
  test: null,
  slot_select: true,
  event_template: null,
  event_slot: null,
  manual: '',
  require_review: false,
  name: '',
  term_type: '',
  term_value: null,
  waiting: false,
  self_assignment: false,
  task_outcome: false,
  categories: [],
  desc: '',
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

const term_types = [
  { label: 'Минуты', value: 'minutes' },
  { label: 'Часы', value: 'hours' },
  { label: 'Дни', value: 'days' },
  { label: 'Без срока', value: 'none' },
];

const delay_types = [
  { label: 'Минуты', value: 'minutes' },
  { label: 'Часы', value: 'hours' },
  { label: 'Дни', value: 'days' },
  { label: 'Без задержки', value: 'none' },
];

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
    const response = await axios.get(`${baseUrl}/task_templates/`, {
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

const loadPlanById = () => {
  if (planId) {
    console.log('Plan ID:', planId);
    const plan = plans.value.find(plan => plan.id === parseInt(planId, 10));
    if (plan) {
      form.is_child = true,
      form.plan = plan;
    } else {
      console.error('Plan не найден.');
    }
  } else {
    console.log('Plan ID не найден.');
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

watch(
  () => form.is_child,
  (newValue) => {
    if (newValue == false) {
      form.plan = null;
      form.item = null;
      form.delay_type = '';
      form.delay_value = null;
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
        option => option.id === newValue.event_template.id
      );
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

watch(
  () => form.term_type,
  (newValue) => {
    if (newValue.value == 'none') {
      form.term_value = null;
    }
  }
);

const cancelEdit = () => {
  const planId = route.query.planId || '';
  if (planId){
    router.push({ name: 'TaskTemplateDetail', params: { id: planId }  });
  } else {
    router.push({ name: 'TaskTemplateList' });
  }
};

const errors = reactive({});
const validateForm = () => {
  if (form.is_child) {
    errors.plan = form.plan ? '' : 'Выбор плана обязателен!';
    errors.item = form.item ? '' : 'Порядок пункта обязателен!';
    errors.delay_type = form.delay_type ? '' : 'Тип задержки обязателен!';
    if (form.delay_type && form.delay_type.value != 'none') {
      errors.delay_value = form.delay_value && form.delay_value > 0 ? '' : 'Задержка обязательна и должна быть больше 0!';
    }
  }
  errors.task_type = form.task_type.value ? '' : 'Тип задачи обязателен!';
  if (form.task_type.value == 'common_task' || form.task_type.value == 'plan_implementation') {
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
  errors.term_type = form.term_type ? '' : 'Тип срока обязателен!';
  if (form.term_type && form.term_type.value != 'none') {
    errors.term_value = form.term_value && form.term_value > 0 ? '' : 'Срок обязателен и должен быть больше 0!';
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
      is_child: form.is_child,
      plan: form.plan?.id || null,
      item: form.item,
      delay_type: form.delay_type?.value || '',
      delay_value: form.delay_value,
      task_type: form.task_type.value,
      material: form.material?.id,
      new: form.new?.id,
      course: form.course?.id,
      test: form.test?.id,
      slot_select: form.slot_select,
      event_template: form.event_template?.id,
      event_slot: form.event_slot?.id,
      require_review: form.require_review,
      name: form.name,
      manual: form.manual || "",
      desc: form.desc,
      term_type: form.term_type.value,
      term_value: form.term_value, 
      waiting: form.waiting,
      self_assignment: form.self_assignment,
      task_outcome: form.task_outcome,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/task_templates/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    const planId = route.query.planId || '';
    if (planId){
      router.push({ name: 'TaskTemplateDetail', params: { id: planId }  });
    } else {
      router.push({ name: 'TaskTemplateDetail', params: { id: jsonResponse.data.id }  });
    }
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
    await loadCategories();
    await loadPlans();
    await loadPlanById();
    await loadMaterials();
    await loadNews();
    await loadCourses();
    await loadTests();
    await loadEventTemplates();
    await loadEventSlots();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
