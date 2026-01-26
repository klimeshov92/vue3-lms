<template>

  <div v-if="loading">

    <div v-if="state.canViewCategory" class="list-page">

      <div class="list-header">
        <h1>Категории</h1>
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
              <label class="filters-label">Родительская категория:</label>
              <multiselect
                v-model="filters.parent_category"
                :options="categories"
                :multiple="false"
                :close-on-select="true"
                :clear-on-select="false"
                :preserve-search="false"
                placeholder="Выберите"
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

            <div class="list-card-header">
              <div class="list-card-header-title">
                <h2>{{ item.name || 'Нет имени пользователя' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem"><span class="list-card-text-label">Родительская категория:</span> {{ item.parent_category?.name || 'Нет родительской категории' }}</div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'CategoryDetail', params: { id: item.id }, query: { tab: 'desc' } }" class="minibutton">
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

      <div v-if="state.canAddCategory" class="list-menu button-group">

        <router-link
          v-if="state.canAddCategory"
          :to="{ name: 'CategoryCreate' }"
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
import { baseUrl, isTokenValid } from '../utils/utils';
const route = useRoute();
const router = useRouter();

const state = reactive({
  items: [],
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddCategory: false,
  canViewCategory: false
});

const loading = ref(false);

const orders = [
  { label: 'Название: по возрастанию', value: 'name' },
  { label: 'Название: по убыванию', value: '-name' },
  { label: 'Название родительской категории: по возрастанию', value: 'parent_category__name' },
  { label: 'Название родительской категории: по убыванию', value: '-parent_category__name' },
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
  parent_category: route.query.parent_category || '',
  order: orders.find(option => option.value === route.query.order || 'name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('categoryFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('categoryPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка категорий с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'CategoryList',
    query: {
      name: filters.name || '',
      parent_category: filters.parent_category || '',
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('categoryFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/categories/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        name: filters.name,
        parent_category: filters.parent_category?.id,
        ordering: filters.order.value
      },
    });

    console.log('Список категорий загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка категорий:', error);
  }
};

const changePage = (page) => {
  console.log('Смена страницы на:', page);
  currentPage.value = page;

  router.push({
    name: 'CategoryList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('categoryPage', currentPage.value);

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
  filters.parent_category = null;
  filters.order = orders.find(option => option.value === 'name');

  localStorage.removeItem('categoryFilters');
  localStorage.removeItem('categoryPage');
  currentPage.value = 1;

  router.push({
    name: 'AccountList',
    query: {
      name: '',
      parent_category: null,
      order: filters.order.value,
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
        },
      });
      console.log('Разрешения пользователя загружены:', response.data);
      userPermissions = response.data
      localStorage.setItem('userPermissions', JSON.stringify(userPermissions));
    }

    state.globalPermissionsList = userPermissions.global_permissions || [];
    state.objectPermissionsDict = userPermissions.object_permissions || {};

    state.canAddCategory = state.globalPermissionsList.includes('core.add_category');
    console.log('Права на добавление аккаунтов:', state.canAddCategory);
    
    state.canViewCategory = state.globalPermissionsList.includes('core.view_category') || !!state.objectPermissionsDict['core.view_category'];
    console.log('Права на просмотр аккаунтов:', state.canViewCategory);
    
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
