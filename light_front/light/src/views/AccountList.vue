<template>

  <div v-if="loading">

    <div v-if="state.canViewAccount" class="list-page">

      <div class="list-header">
        <h1>Аккаунты</h1>
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
              <label class="filters-label">Имя пользователя:</label>
              <input v-model="filters.username" class="filters-input" placeholder="Введите имя пользователя" />
            </div>

            <div class="filters-field">
              <label class="filters-label">Электронная почта:</label>
              <input v-model="filters.email" class="filters-input" placeholder="Введите электронную почту" />
            </div>

            <div class="filters-field">
              <label class="filters-label">Фамилия:</label>
              <input v-model="filters.last_name" class="filters-input" placeholder="Введите фамилию" />
            </div>

            <div class="filters-field">
              <label class="filters-label">Активен:</label>
              <multiselect
                v-model="filters.is_active"
                :options="[
                  { label: 'Да', value: 'true' },
                  { label: 'Нет', value: 'false' }
                ]"
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
              <label class="filters-label">Самостоятельная регистрация:</label>
              <multiselect
                v-model="filters.self_registration"
                :options="[
                  { label: 'Да', value: 'true' },
                  { label: 'Нет', value: 'false' }
                ]"
                :multiple="false"
                :searchable="false"
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

            <div class="list-card-image-outer">
              <div v-if="item.avatar" class="list-card-image-inner">
                <img :src="item.avatar" alt="Аватар" />
              </div>
              <div v-else class="list-card-image-none">
                <spa class="none-text">Нет аватара</spa>
              </div>
            </div>

            <div class="list-card-header">
              <div class="list-card-header-title">
                <h2>{{ item.username || 'Нет имени пользователя' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem"><span class="list-card-text-label">Фамилия:</span> {{ item.last_name || 'Нет фамилии' }}</div>
              <div class="list-card-text-elem"><span class="list-card-text-label">Имя:</span> {{ item.first_name || 'Нет имени' }}</div>
              <div class="list-card-text-elem"><span class="list-card-text-label">Отчество:</span> {{ item.fathers_name || 'Нет отчества' }}</div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'AccountDetail', params: { id: item.id },  query: { tab: 'details' } }" class="minibutton">
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

      <div v-if="state.canAddAccount" class="list-menu button-group">

        <router-link
          v-if="state.canAddAccount"
          :to="{ name: 'AccountCreate' }"
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
  canAddAccount: false,
  canViewAccount: false
});

const loading = ref(false);

const orders = [
  { label: 'Фамилия: по возрастанию', value: 'last_name' },
  { label: 'Фамилия: по убыванию', value: '-last_name' },
  { label: 'Имя пользователя: по возрастанию', value: 'username' },
  { label: 'Имя пользователя: по убыванию', value: '-username' },
  { label: 'Электронная почта: по возрастанию', value: 'email' },
  { label: 'Электронная почта: по убыванию', value: '-email' },
];

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
  username: route.query.username || '',
  email: route.query.email || '',
  last_name: route.query.last_name || '',
  is_active: route.query.is_active
    ? { label: route.query.is_active === 'true' ? 'Да' : 'Нет', value: route.query.is_active }
    : '',
  self_registration: route.query.self_registration
    ? { label: route.query.self_registration === 'true' ? 'Да' : 'Нет', value: route.query.self_registration }
    : '',
  user_permissions: route.query.user_permissions
    ? route.query.user_permissions.map(permission => ({ id: parseInt(permission, 10) }))
    : [],
  order: orders.find(option => option.value === route.query.order || 'last_name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('accountFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('accountPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка аккаунтов с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'AccountList',
    query: {
      username: filters.username || '',
      email: filters.email || '',
      last_name: filters.last_name || '',
      is_active: filters.is_active ? filters.is_active.value : '',
      self_registration: filters.self_registration ? filters.self_registration.value : '',
      user_permissions: filters.user_permissions.map(permission => permission.id) || [],
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('accountFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/accounts/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        username: filters.username,
        email: filters.email,
        last_name: filters.last_name,
        is_active: filters.is_active ? filters.is_active.value: '',
        self_registration: filters.self_registration ? filters.self_registration.value: '',
        user_permissions: filters.user_permissions.map(permission => permission.id),
        ordering: filters.order.value
      },
    });

    console.log('Список аккаунтов загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка аккаунтов:', error);
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
    name: 'AccountList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('accountPage', currentPage.value);

  loadObjects(filters, page);
};

const showFilters = ref(false);

const toggleFilters = () => {
  showFilters.value = !showFilters.value;
  console.log('Текущий статус показа фильтров:', showFilters.value);
};

const resetFilters = () => {
  console.log('Сбрасываем фильтры');
  filters.username = '';
  filters.email = '';
  filters.last_name = ''; 
  filters.is_active = ''; 
  filters.self_registration = '';
  filters.user_permissions = [];
  filters.order = orders.find(option => option.value === 'last_name');

  localStorage.removeItem('accountFilters');
  localStorage.removeItem('accountPage');
  currentPage.value = 1;

  router.push({
    name: 'AccountList',
    query: {
      username: '',
      email: '',
      last_name: '',
      is_active: '',
      self_registration: '',
      user_permissions: [],
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
        }
      });
      console.log('Разрешения пользователя загружены:', response.data);
      userPermissions = response.data
      localStorage.setItem('userPermissions', JSON.stringify(userPermissions));
    }

    state.globalPermissionsList = userPermissions.global_permissions || [];
    state.objectPermissionsDict = userPermissions.object_permissions || {};

    state.canAddAccount = state.globalPermissionsList.includes('core.add_account');
    console.log('Права на добавление аккаунтов:', state.canAddAccount);
    
    state.canViewAccount = state.globalPermissionsList.includes('core.view_account') || !!state.objectPermissionsDict['core.view_account'];
    console.log('Права на просмотр аккаунтов:', state.canViewAccount);
    
  } catch (error) {
    console.error('Ошибка при получении разрешений пользователя:', error);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadFilters(),
    await loadCurrentPage(), 
    await loadPermissions(),
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
