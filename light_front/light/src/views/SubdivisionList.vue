<template>

  <div v-if="loading">

    <div v-if="state.canViewSubdivision" class="list-page">

      <div class="list-header">
        <h1>Подразделения</h1>
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
              <label class="filters-label">Организация:</label>
              <multiselect
                v-model="filters.organization"
                :options="organizations"
                :multiple="false"
                :close-on-select="true"
                :clear-on-select="false"
                :preserve-search="false"
                placeholder="Выберите"
                label="legal_name"
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
              <label class="filters-label">Родительское подразделение:</label>
              <multiselect
                v-model="filters.parent_subdivision"
                :options="subdivisions"
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
                <h2>{{ item.name || 'Нет названия' }}</h2>
              </div>
            </div>

            <div class="list-card-text">
              <div class="list-card-text-elem"><span class="list-card-text-label">Организация:</span> {{ item.organization?.legal_name || 'Нет организации' }}</div>
              <div class="list-card-text-elem"><span class="list-card-text-label">Родительское подразделение:</span> {{ item.parent_subdivision?.name || 'Нет родительского подразделения' }}</div>
            </div>

            <div class="list-card-menu minibutton-group">
              <router-link :to="{ name: 'SubdivisionDetail', params: { id: item.id },  query: { tab: 'details' } }" class="minibutton">
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

      <div v-if="state.canAddSubdivision" class="list-menu button-group">

        <router-link
          v-if="state.canAddSubdivision"
          :to="{ name: 'SubdivisionCreate' }"
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
  canAddSubdivision: false,
  canViewSubdivision: false
});

const loading = ref(false);

const orders = [
  { label: 'Название: по возрастанию', value: 'name' },
  { label: 'Название: по убыванию', value: '-name' },
  { label: 'Юридическое назнание организации: по возрастанию', value: 'organization__legal_name' },
  { label: 'Юридическое назнание организации: по убыванию', value: '-organization__legal_name' },
  { label: 'Название родительского подразделения: по возрастанию', value: 'parent_subdivision__name' },
  { label: 'Название родительского подразделения: по убыванию', value: '-parent_subdivision__name' },
];

const organizations = ref([]);
const loadOrganizations = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    const response = await axios.get(`${baseUrl}/organizations/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
    });

    organizations.value = response.data.results || [];
    console.log('Организации загружены:', organizations.value);
  } catch (error) {
    console.error("Ошибка при загрузке организаций:", error.response ? error.response.data : error.message);
  }
};

const subdivisions = ref([]);
const loadSubdivisions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  try {
    const response = await axios.get(`${baseUrl}/subdivisions/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
    });

    subdivisions.value = response.data.results || [];
    console.log('Подразделения загружены:', subdivisions.value);
  } catch (error) {
    console.error("Ошибка при загрузке подразделений:", error.response ? error.response.data : error.message);
  }
};

const filters = reactive({
  name: route.query.name || '',
  organization: route.query.organization || '',
  parent_subdivision: route.query.parent_subdivision || '',
  order: orders.find(option => option.value === route.query.order || 'name')
});

const loadFilters = () => {
  const storedFilters = localStorage.getItem('subdivisionFilters');
  if (storedFilters) {
    console.log('Загруженные фильры:', storedFilters);
    Object.assign(filters, JSON.parse(storedFilters));
  }
};

const currentPage = ref(Number(route.query.page) || 1);
const totalPages = ref(1);

const loadCurrentPage = () => {
  const storedPage = localStorage.getItem('subdivisionPage');
  if (storedPage) {
    console.log('Загруженная странциа:', storedPage);
    currentPage.value = parseInt(storedPage, 10);
  }
};

const loadObjects = async (filters, page) => {
  console.log('Загрузка подразделений с фильтрами:', filters, 'для страницы:', page);
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }

  router.push({
    name: 'SubdivisionList',
    query: {
      name: filters.name || '',
      organization: filters.organization || '',
      parent_subdivision: filters.parent_subdivision || '',
      order: filters.order.value,
      page: currentPage.value,
    },
  });

  localStorage.setItem('subdivisionFilters', JSON.stringify(filters))

  try {
    const response = await axios.get(`${baseUrl}/subdivisions/`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      params: {
        page: page,
        page_size: 12,
        name: filters.name,
        organization: filters.organization?.id,
        parent_subdivision: filters.parent_subdivision?.id,
        ordering: filters.order.value
      },
    });

    console.log('Список организаций загружен:', response.data); 
    state.items = response.data.results;
    //state.items = [];
    totalPages.value = Math.ceil(response.data.count / 12);
  } catch (error) {
    console.error('Ошибка при загрузке списка организаций:', error);
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
    name: 'SubdivisionList',
    query: {
      ...route.query,
      page: currentPage.value,
    },
  });

  localStorage.setItem('subdivisionPage', currentPage.value);

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
  filters.organization = '',
  filters.parent_subdivision = '',
  filters.order = orders.find(option => option.value === 'name');

  localStorage.removeItem('subdivisionFilters');
  localStorage.removeItem('subdivisionPage');
  currentPage.value = 1;

  router.push({
    name: 'SubdivisionList',
    query: {
      name: '',
      organization: '',
      parent_subdivision: '',
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

    state.canAddSubdivision = state.globalPermissionsList.includes('core.add_subdivision');
    console.log('Права на добавление подразделений:', state.canAddSubdivision);
    
    state.canViewSubdivision = state.globalPermissionsList.includes('core.view_subdivision') || !!state.objectPermissionsDict['core.view_subdivision'];
    console.log('Права на просмотр подразделений:', state.canViewSubdivision);
    
  } catch (error) {
    console.error('Ошибка при получении разрешений пользователя:', error);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadFilters(),
    await loadCurrentPage(),
    await loadOrganizations(),
    await loadSubdivisions(), 
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
