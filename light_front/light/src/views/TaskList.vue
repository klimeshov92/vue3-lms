<template>

  <div v-if="loading">

    <div v-if="state.canViewTask" class="list-page">

      <div class="list-header">
        <h1>Задачи</h1>
      </div>

      <div class="list-settings">
        <button @click="toggleFilters" class="list-settings-button">
          Параметры
        </button>
      </div>

      <div v-if="showFilters" class="filters-overlay" @click="toggleFilters">

        <div class="filters-outer" @click.stop>

          <div class="filters-close_button-inner">
            <button @click="toggleFilters" class="filters-close_button">
              ×
            </button>
          </div>

          <div class="filters-inner">

            <div class="filters-field">
              <label class="filters-label">Название:</label>
              <input v-model="filters.name" class="filters-input" placeholder="Введите название" />
            </div>

            <div class="filters-field">
              <label class="filters-label">Категории:</label>
              <multiselect
                v-model="filters.categories"
                :options="categories"
                :multiple="true"
                :close-on-select="false"
                :clear-on-select="false"
                :preserve-search="false"
                placeholder="Выберите"
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

            <div class="filters-field">
              <label class="filters-label">Сортировка:</label>
              <multiselect
                v-model="filters.order"
                :options="orders"
                :searchable="false"
                :multiple="false"
                :close-on-select="false"
                :clear-on-select="false"
                placeholder="Выберите"
                label="label"
                track-by="value"
                :preselect-first="false"
                :select-label="``"
                :deselect-label="``"
                :selected-label="``"
                :allow-empty="false"
              >
              </multiselect>
            </div>

          </div>

          <div class="filters-menu button-group">
            <button @click="loadObjects(filters, currentPage.value)" class="button">Применить</button>
            <button @click="resetFilters" class="button">Сбросить</button>
          </div>

        </div>

      </div>
      
      <div v-if="state.items.length !== 0" class="list-items">

        <div class="list-grid">

          <div v-for="item in state.items" :key="item.id" class="list-card">

            <div class="list-card-icons">
              <div v-if="item.result?.status == 'waiting'" class="list-card-icon-grey">
                <span class="list-card-icon">
                  <i class="fa-solid fa-lock"></i>
                </span>
                В ожидании
              </div>
              <div v-else-if="item.result?.status == 'assigned'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-thumbtack"></i>
                </span>
                Назначено
              </div>
              <div v-else-if="item.result?.status == 'in_progress'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-hourglass-half"></i>
                </span>
                В процессе
              </div>
              <div v-else-if="item.result?.status == 'under_review'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-magnifying-glass"></i>
                </span>
                На проверке
              </div>
              <div v-else-if="item.result?.status == 'completed'" class="list-card-icon-completed">
                <span class="list-card-icon">
                  <i class="fa-solid fa-circle-check"></i>
                </span>
                 Выполнено
              </div>
              <div v-else-if="item.result?.status == 'failed'" class="list-card-icon-attention">
                <span class="list-card-icon">
                  <i class="fa-solid fa-circle-xmark"></i>
                </span>
                Провалено
              </div>
              <div v-else-if="item.result?.status == 'canceled'" class="list-card-icon-grey">
                <span class="list-card-icon">
                  <i class="fa-solid fa-ban"></i>
                </span>
                Отменено
              </div>
            </div>

            <div class="list-card-header">
              <div class="list-card-header-title">
                <h2>{{ item.plan ? item.plan.name + ' - ' : '' }}{{ item.item ? item.item  + ' - ' : ''  }}{{ item.name || 'Нет названия' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem">
                <span class="list-card-text-label">Тип задачи:</span> {{ item.task_type_display || 'Нет типа задачи' }}
              </div>
              <div class="list-card-text-elem">
                <span class="list-card-text-label">Срок завершения:</span>
                {{ item.planned_end ? formatDateTime(item.planned_end) : 'Нет срока' }}
              </div>
              <div class="list-card-text-elem">
                <span class="list-card-text-label">Категории:</span>
                {{ item.categories.length > 0 ? item.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'TaskDetail', params: { id: item.id },  query: { tab: 'desc' } }" class="minibutton">
                Подробнее
              </router-link>
            </div>

          </div>

        </div>

        <div class="list-pagination">

          <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="list-settings-button">
            Назад
          </button>

          <span>Страница {{ currentPage }} из {{ totalPages }}</span>

          <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="list-settings-button">
            Вперед
          </button>

        </div>
      
      </div>

      <div v-else class="none-card">
        <div>Список пуст</div>
      </div>

      <div v-if="state.canAddTask" class="list-menu button-group">

        <router-link
          v-if="state.canAddTask"
          :to="{ name: 'TaskCreate' }"
          class="button"
        >
          Создать
        </router-link>

      </div>

    </div>

    <div v-else class="loading">
      <div>У вас нет разрешения на просмотр</div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>

</template>

<script setup>
import axios from 'axios';
import { reactive, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils';
const route = useRoute();
const router = useRouter();

const state = reactive({
  items: [],
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddTask: false,
  canViewTask: false
});

const loading = ref(false);

const orders = [
  { label: 'Планируемое завершение: по возрастанию', value: 'planned_end' },
  { label: 'Планируемое завершение: по убыванию', value: '-planned_end' },
  { label: 'Название плана: по возрастанию', value: 'plan__name' },
  { label: 'Название плана: по убыванию', value: '-plan__name' },
  { label: 'Название: по возрастанию', value: 'name' },
  { label: 'Название: по убыванию', value: '-name' },
];

const categories = ref([]);
const loadCategories = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    const response = await axios.get(`${baseUrl}/categories/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
    });

    categories.value = response.data.results || [];
    console.log('Категории загружены:', categories.value);
  } catch (error) {
    console.error("Ошибка при загрузке категорий:", error.response ? error.response.data : error.message);
  }
};

const filters = reactive({
  name: route.query.name || '',
  categories: route.query.categories
    ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
    : [],
  order: orders.find(option => option.value === route.query.order || 'plan__name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('taskFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('taskPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка задач с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'TaskList',
    query: {
      name: filters.name || '',
      categories: filters.categories.map(category => category.id) || [],
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('taskFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/tasks/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        name: filters.name,
        categories: filters.categories.map(category => category.id),
        ordering: filters.order.value
      },
    });

    console.log('Список задач загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка задач:', error);
    //if (error.response && error.response.status === 404) {
      //await resetFilters()
      //await loadObjects(filters, currentPage.value);
    //}
  }
};

const changePage = (page) => {
  console.log('Смена страницы на:', page);
  currentPage.value = page;

  router.push({
    name: 'TaskList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('taskPage', currentPage.value);

  loadObjects(filters, page);
};

const showFilters = ref(false);

const toggleFilters = () => {
  showFilters.value = !showFilters.value;
  console.log('Текущий статус показа фильтров:', showFilters.value);
};

const resetFilters = () => {
  console.log('Сбрасываем фильтры');
  filters.name = '';
  filters.categories = [];
  filters.order = orders.find(option => option.value === 'plan__name');

  localStorage.removeItem('taskFilters');
  localStorage.removeItem('taskPage');
  currentPage.value = 1;

  router.push({
    name: 'TaskList',
    query: {
      name: '',
      categories: [],
      page: currentPage.value,
    },
  });


  loadObjects(filters, currentPage.value);
};


const checkPermissionsVersion = async () => {
  console.log('Проверяем версию прав')
  const localPermissions = JSON.parse(localStorage.getItem('userPermissions'))

  if (!localPermissions?.permissions_version) return
  console.log('Текущая версия прав:', localPermissions.permissions_version)

  let token = localStorage.getItem('access_token')
  const validToken = isTokenValid(token)
  if (!token || !validToken) return

  try {
    const resp = await axios.get(
      `${baseUrl}/user_permissions_version/${localPermissions.permissions_version}/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!resp.data.actual) {
      console.log('Версия прав устарела — очищаем память')
      localStorage.removeItem('userPermissions')
    } else {
      console.log('Версия прав актуальна')
    }

  } catch (error) {
    console.error('Ошибка проверки версии прав:', error);
    localStorage.removeItem('userPermissions')
  }
}

const loadUserPermissions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    let userPermissions = JSON.parse(localStorage.getItem('userPermissions')) || {};
    console.log('Разрешения пользователя из памяти', userPermissions);
    
    if (Object.keys(userPermissions).length > 0) {
      console.log('ID пользователя в разрешениях из памяти:', userPermissions.user_id);

      if (!validToken && userPermissions.user_id !== 1 || validToken && validToken.user_id !== userPermissions.user_id) {
        console.log('Разрешения пользователя из памяти не соотвествуют пользователю и будут обнулены');
        localStorage.removeItem('userPermissions');
        userPermissions = {};
      } else {
        console.log('Разрешения пользователя из памяти соотвествуют пользователю');
      }
    }

    if (Object.keys(userPermissions).length === 0) {
      const response = await axios.get(`${baseUrl}/user_permissions/`, {
        headers: {
          ...(token && { 'Authorization': `Bearer ${token}` })
        }
      });
      console.log('Разрешения пользователя загружены:', response.data);
      userPermissions = response.data
      localStorage.setItem('userPermissions', JSON.stringify(userPermissions));
    }

    state.globalPermissionsList = userPermissions.global_permissions || [];
    state.objectPermissionsDict = userPermissions.object_permissions || {};

    state.canAddTask = state.globalPermissionsList.includes('bpms.add_task');
    console.log('Права на добавление задач:', state.canAddTask);
    
    state.canViewTask = state.globalPermissionsList.includes('bpms.view_task') || !!state.objectPermissionsDict['bpms.view_task'];
    console.log('Права на просмотр задач:', state.canViewTask);
    
  } catch (error) {
    console.error('Ошибка при получении разрешений пользователя:', error);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadFilters(),
    await loadCurrentPage(),
    await loadCategories(),
    await checkPermissionsVersion();
    await loadUserPermissions();
    await loadObjects(filters, currentPage.value)
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
