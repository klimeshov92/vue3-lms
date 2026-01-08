<template>

  <div v-if="loading">

    <div v-if="state.canViewAccountPermission" class="list-page">

      <div class="list-header">
        <h1>Права пользователей</h1>
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
              <label class="filters-label">Пользователь:</label>
              <multiselect
                v-model="filters.account"
                :options="accounts"
                :multiple="false"
                :close-on-select="true"
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

          <div v-for="perm in state.items" :key="`${perm.user.id}-${perm.type}-${perm.permission.id}`" class="list-card">

            <div class="list-card-header">
              <div class="list-card-header-title">
                <h2>
                  {{ perm.user?.username || 'Нет имени пользователя' }} | 
                  {{ perm.permission?.name || 'Нет названия права' }}
                </h2>
              </div>
            </div>

            <!-- Контент карточки в зависимости от типа права -->
            <div class="list-card-text">
              <!-- Прямое право -->
              <div v-if="perm.type === 'direct'">
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип права:</span>
                  {{ perm.user.is_superuser ? 'Администратор' : 'Назначенное' }}
                </div>
              </div>

              <!-- Групповое право -->
              <div v-else-if="perm.type === 'group'">
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип права:</span> Групповое
                </div>
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Группа:</span> {{ perm.group?.name || 'Нет имени группы' }}
                </div>
              </div>

              <!-- Прямое объектное право -->
              <div v-else-if="perm.type === 'object_direct'">
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип права:</span> Прямое объектное
                </div>
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип объекта:</span> {{ perm.content_type?.verbose_name || 'Нет типа объекта' }}
                </div>
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Объект:</span> {{ perm.object?.str || 'Нет объекта' }}
                </div>
              </div>

              <!-- Групповое объектное право -->
              <div v-else-if="perm.type === 'object_group'">
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип права:</span> Групповое объектное
                </div>
                <div class="list-card-text-elem" v-if="perm.group">
                  <span class="list-card-text-label">Группа:</span> {{ perm.group.name }}
                </div>
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Тип объекта:</span> {{ perm.content_type?.verbose_name || 'Нет типа объекта' }}
                </div>
                <div class="list-card-text-elem">
                  <span class="list-card-text-label">Объект:</span> {{ perm.object?.str || 'Нет объекта' }}
                </div>
              </div>
            </div>

            <div class="list-card-menu minibutton-group">

              <!-- Прямое право -->
              <div v-if="perm.type === 'direct'">
                <router-link 
                  :to="{ name: 'AccountDetail', params: { id: perm.user.id }, query: { tab: 'details' } }" 
                  class="minibutton">
                  Пользователь
                </router-link>
              </div>

              <!-- Групповое право -->
              <div v-else-if="perm.type === 'group'">
                <router-link 
                  :to="{ name: 'AccountGroupDetail', params: { id: perm.group.id }, query: { tab: 'details' } }" 
                  class="minibutton">
                  Группа
                </router-link>
              </div>

              <!-- Прямое объектное право -->
              <div v-else-if="perm.type === 'object_direct'">
                <button @click="openPermDeleteModal(perm)" class="minibutton"> Удалить</button>
              </div>

              <!-- Групповое объектное право -->
              <div v-else-if="perm.type === 'object_group'">
                <button @click="openPermDeleteModal(perm)" class="minibutton"> Удалить</button>
              </div>

            </div>

          </div>

        </div>

        <div v-if="showPermDeleteModal" class="modal-overlay">
          <div class="modal">
            <div class="modal-header">
              <h2 class="modal-header-h2">Удаление {{ selectedPerm.permission.name || 'Безымянный исполнитель очереди' }}</h2>
            </div>
            <div class="minibutton-group modal-menu">
              <button @click="confirmPermDelete(selectedPerm.object_perm_id)" class="minibutton">Подтвердить</button>
              <button @click="closePermDeleteModal" class="minibutton">Отменить</button>
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
  canAddAccountPermission: false,
  canViewAccountPermission: false,
});

const loading = ref(false);

const orders = [
  { label: 'Название: по возрастанию', value: 'name' },
  { label: 'Название: по убыванию', value: '-name' },
];

const accounts = ref([]);
const loadAccount = async () => {
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
    console.error('Ошибка при загрузке групп:', error.response ? error.response.data : error.message);
  }
};

const filters = reactive({
  name: route.query.name || '',
  account: route.query.account || '',
  order: orders.find(option => option.value === route.query.order || 'name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('permissionFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('permissionPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка прав с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'AccountPermissionList',
    query: {
      name: filters.name || '',
      account: filters.account || '',
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('permissionFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/users_permissions/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        name: filters.name,
        account: filters.account?.id,
        ordering: filters.order.value
      },
    });

    console.log('Список прав загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка прав:', error);
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
    name: 'AccountPermissionList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('permissionPage', currentPage.value);

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
  filters.account = null;
  filters.order = orders.find(option => option.value === 'name');

  localStorage.removeItem('permissionFilters');
  localStorage.removeItem('permissionPage');
  currentPage.value = 1;

  router.push({
    name: 'AccountPermissionList',
    query: {
      name: '',
      account: null,
      page: currentPage.value,
    },
  });


  loadObjects(filters, currentPage.value);
};

const showPermDeleteModal = ref(false);
const selectedPerm = ref(null);
const openPermDeleteModal = (perm) => {
  selectedPerm.value = perm;
  showPermDeleteModal.value = true;
};
const closePermDeleteModal = () => {
  showPermDeleteModal.value = false;
};
const confirmPermDelete = async (id) => {

  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  if (selectedPerm.value.type == 'object_group') {
    
    try {
      await axios.delete(`${baseUrl}/accounts_group_object_permissions/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

    } catch (error) {
      console.error('Ошибка удаления права:', error);
    }
  }

  if (selectedPerm.value.type == 'object_direct') {

    try {
      await axios.delete(`${baseUrl}/account_object_permissions/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

    } catch (error) {
      console.error('Ошибка удаления права:', error);
    }
  }

  await loadObjects(filters, currentPage.value);
  closePermDeleteModal();
  
};



const loadAccountPermissions = async () => {
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

    state.canAddAccountPermission = state.globalPermissionsList.includes('auth.add_permission');
    console.log('Права на добавление прав:', state.canAddAccountPermission);
    
    state.canViewAccountPermission = state.globalPermissionsList.includes('auth.view_permission') || !!state.objectPermissionsDict['auth.view_permission'];
    console.log('Права на просмотр прав:', state.canViewAccountPermission);
    
  } catch (error) {
    console.error('Ошибка при получении разрешений пользователя:', error);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadAccount();
    await loadFilters();
    await loadCurrentPage(); 
    await loadAccountPermissions();
    await loadObjects(filters, currentPage.value);
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
