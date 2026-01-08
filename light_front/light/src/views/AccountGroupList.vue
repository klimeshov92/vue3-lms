<template>

  <div v-if="loading">

    <div v-if="state.canViewAccountGroup" class="list-page">

      <div class="list-header">
        <h1>Группы</h1>
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
              <input v-model="filters.username" class="filters-input" placeholder="Введите название" />
            </div>

            <div class="filters-field">
              <label class="filters-label">Тип:</label>
              <multiselect
                v-model="filters.type"
                :options="types"
                :searchable="false"
                :multiple="false"
                :close-on-select="true"
                :clear-on-select="true"
                placeholder="Выберите"
                label="label"
                track-by="value"
                :preselect-first="false"
                :select-label="``"
                :deselect-label="``"
                :selected-label="``"
              />
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
              <label class="filters-label">Аккаунты:</label>
              <multiselect
                v-model="filters.accounts"
                :options="accounts"
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
              <label class="filters-label">Разрешения:</label>
              <multiselect
                v-model="filters.user_permissions"
                :options="permissions"
                :multiple="true"
                :close-on-select="false"
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
                <h2>{{ item.name || 'Нет названия' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem"><span class="list-card-text-label">Тип:</span> {{ item.type_display || 'Нет типа' }}</div>
              <div class="list-card-text-elem">
                <span class="list-card-text-label">Категории:</span>
                {{ item.categories.length > 0 ? item.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'AccountGroupDetail', params: { id: item.id },  query: { tab: 'desc' } }" class="minibutton">
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

      <div v-if="state.canAddAccountGroup" class="list-menu button-group">

        <router-link
          v-if="state.canAddAccountGroup"
          :to="{ name: 'AccountGroupCreate' }"
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
  canAddAccountGroup: false,
  canViewAccountGroup: false
});

const loading = ref(false);

const types = [
  { label: 'Пользовательская', value: 'custom' },
  { label: 'Системная', value: 'system' },
  { label: 'Организация', value: 'organization' },
  { label: 'Подразделение', value: 'subdivision' },
  { label: 'Должность', value: 'position' },
  { label: 'Назначение', value: 'assignment' },
  { label: 'Импорт из Excel', value: 'excel_import' },
  { label: 'Импорт по API', value: 'api_import' },
  { label: 'Участники мероприятия', value: 'event_participants' },
  { label: 'Ответственные мероприятия', value: 'event_responsible' },
];

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

const accounts = ref([]);
const loadAccounts = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    const response = await axios.get(`${baseUrl}/accounts/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
    });

    accounts.value = response.data.results || [];
    console.log('Аккаунты загружены:', accounts.value);
  } catch (error) {
    console.error("Ошибка при загрузке аккаунтов:", error.response ? error.response.data : error.message);
  }
};

const permissions = ref([]);
const loadPermissions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    const response = await axios.get(`${baseUrl}/permissions/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
    });

    permissions.value = response.data.results || [];
    console.log('Разрешения загружены:', permissions.value);
  } catch (error) {
    console.error("Ошибка при загрузке разрешений:", error.response ? error.response.data : error.message);
  }
};

const filters = reactive({
  name: route.query.name || '',
  type: types.find(option => option.value === route.query.type || ''),
  categories: route.query.categories
    ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
    : [],
  accounts: route.query.accounts
    ? route.query.accounts.map(account => ({ id: parseInt(account, 10) }))
    : [],
  group_permissions: route.query.group_permissions
    ? route.query.group_permissions.map(permission => ({ id: parseInt(permission, 10) }))
    : [],
  order: orders.find(option => option.value === route.query.order || 'name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('accountGroupFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('accountGroupPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка групп с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'AccountGroupList',
    query: {
      name: filters.name || '',
      type: filters.type ? filters.type.value : '',
      categories: filters.categories.map(category => category.id) || [],
      accounts: filters.accounts.map(account => account.id) || [],
      group_permissions: filters.group_permissions.map(permission => permission.id) || [],
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('accountGroupFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/account_groups/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        name: filters.name,
        type: filters.type ? filters.type.value : '',
        categories: filters.categories.map(category => category.id),
        user_set: filters.accounts.map(account => account.id),
        group_permissions: filters.group_permissions.map(permission => permission.id),
        ordering: filters.order.value
      },
    });

    console.log('Список групп загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка групп:', error);
  }
};

const changePage = (page) => {
  console.log('Смена страницы на:', page);
  currentPage.value = page;

  router.push({
    name: 'AccountGroupList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('accountGroupPage', currentPage.value);

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
  filters.type = '';
  filters.categories = [];
  filters.accounts = [];
  filters.user_permissions = [];
  filters.order = orders.find(option => option.value === 'name');

  localStorage.removeItem('accountGroupFilters');
  localStorage.removeItem('accountGroupPage');
  currentPage.value = 1;

  router.push({
    name: 'AccountGroupList',
    query: {
      name: '',
      type: '',
      categories: [],
      accounts: [],
      user_permissions: [],
      order: filters.order.value,
      page: currentPage.value,
    },
  });


  loadObjects(filters, currentPage.value);
};

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

    state.canAddAccountGroup = state.globalPermissionsList.includes('core.add_accounts_group');
    console.log('Права на добавление групп:', state.canAddAccountGroup);
    
    state.canViewAccountGroup = state.globalPermissionsList.includes('core.view_accounts_group') || !!state.objectPermissionsDict['core.view_accounts_group'];
    console.log('Права на просмотр групп:', state.canViewAccountGroup);

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
    await loadAccounts(),
    await loadPermissions(),
    await loadUserPermissions(),
    await loadObjects(filters, currentPage.value)
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
