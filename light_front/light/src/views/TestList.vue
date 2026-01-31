<template>

  <div v-if="loading">

    <div v-if="state.canViewTest" class="list-page">

      <div class="list-header">
        <h1>Тесты</h1>
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

            <div class="list-card-image-outer">
              <div v-if="item.avatar" class="list-card-image-inner">
                <img :src="item.avatar" alt="Аватар" />
              </div>
              <div v-else class="list-card-image-none">
                <spa class="none-text">Нет аватара</spa>
              </div>
            </div>

            <div class="list-card-icons">
              <div v-if="item.last_task?.result?.status == 'waiting'" class="list-card-icon-grey">
                <span class="list-card-icon">
                  <i class="fa-solid fa-lock"></i>
                </span>
                В ожидании
              </div>
              <div v-else-if="item.last_task?.result?.status == 'assigned'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-thumbtack"></i>
                </span>
                Назначено
              </div>
              <div v-else-if="item.last_task?.result?.status == 'in_progress'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-hourglass-half"></i>
                </span>
                В процессе
              </div>
              <div v-else-if="item.last_task?.result?.status == 'under_review'" class="list-card-icon-progress">
                <span class="list-card-icon">
                  <i class="fa-solid fa-magnifying-glass"></i>
                </span>
                На проверке
              </div>
              <div v-else-if="item.last_task?.result?.status == 'completed'" class="list-card-icon-completed">
                <span class="list-card-icon">
                  <i class="fa-solid fa-circle-check"></i>
                </span>
                 Выполнено
              </div>
              <div v-else-if="item.last_task?.result?.status == 'failed'" class="list-card-icon-attention">
                <span class="list-card-icon">
                  <i class="fa-solid fa-circle-xmark"></i>
                </span>
                Провалено
              </div>
              <div v-else-if="item.last_task?.result?.status == 'canceled'" class="list-card-icon-grey">
                <span class="list-card-icon">
                  <i class="fa-solid fa-ban"></i>
                </span>
                Отменено
              </div>
              <div v-else-if="!item.last_task" class="list-card-icon-grey">
                <span class="list-card-icon">
                  <i class="fa-solid fa-ban"></i>
                </span>
                Не назначено
              </div>
            </div>

            <div class="list-card-header">
              <div class="list-card-header-title">
                <h2>{{ item.name || 'Нет названия' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem">
                <span class="list-card-text-label">Категории:</span>
                {{ item.categories.length > 0 ? item.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'TestDetail', params: { id: item.id },  query: { tab: 'details' } }" class="minibutton">
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

      <div v-if="state.canAddTest" class="list-menu button-group">

        <router-link
          v-if="state.canAddTest"
          :to="{ name: 'TestCreate' }"
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
const route = useRoute();
const router = useRouter();

const state = reactive({
  items: [],
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddTest: false,
  canViewTest: false
});

const loading = ref(false);

const orders = [
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
  order: orders.find(option => option.value === route.query.order || 'name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('testFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('testPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка тестов с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'TestList',
    query: {
      name: filters.name || '',
      categories: filters.categories.map(category => category.id) || [],
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('testFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/tests/`, {
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

    console.log('Список тестов загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка тестов:', error);
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
    name: 'TestList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('testPage', currentPage.value);

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
  filters.order = orders.find(option => option.value === 'name');

  localStorage.removeItem('testFilters');
  localStorage.removeItem('testPage');
  currentPage.value = 1;

  router.push({
    name: 'TestList',
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

    state.canAddTest = state.globalPermissionsList.includes('tests.add_test');
    console.log('Права на добавление тестов:', state.canAddTest);
    
    state.canViewTest = state.globalPermissionsList.includes('tests.view_test') || !!state.objectPermissionsDict['tests.view_test'];
    console.log('Права на просмотр тестов:', state.canViewTest);
    
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
