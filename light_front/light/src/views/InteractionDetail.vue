<template>
  <div v-if="loading">
    <div v-if="state.canViewInteraction" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.id || 'Безымянное взаимодействие' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип задачи:</span> {{ state.object.object_type_display || 'Нет типа объекта' }}
              </div>
              <div v-if="state.object.object_type == 'client'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Клиент:</span> {{ state.object.client ? state.object.client.str : 'Нет итога' }}
              </div>
              <div v-if="state.object.object_type == 'account'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Клиент:</span> {{ state.object.account ? state.object.account.str : 'Нет итога' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>

            <div class="detail-menu button-group">

              <router-link 
                v-if="state.canEditInteraction" 
                :to="{ name: 'InteractionEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
               
              <button 
                v-if="state.canDeleteInteraction" 
                @click="openInteractionDeleteModal"
                class="button"
              >
                Удалить
              </button>

            </div>

            <div v-if="showInteractionDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный задача' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmInteractionDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeInteractionDeleteModal" class="minibutton">Отменить</button>
                </div>
              </div>
            </div>

          </div>
        </div>


        <div class="detail-tabs">
          <div class="tabs-header">
            <button 
              v-for="tab in tabs" 
              :key="tab.name" 
              :class="{ active: activeTab === tab.name }"
              @click="activeTab = tab.name"
              class="tab-button"
            >
              {{ tab.label }}
            </button>
          </div>

          <div v-if="activeTab" class="tabs-content">

            <div v-if="activeTab === 'details'" class="detail-tab">
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Тип задачи:</span> {{ state.object.object_type_display || 'Нет типа объекта' }}
              </div>
              <div v-if="state.object.object_type == 'client'" class="detail-tab-elem">
                <span class="detail-tab-label">Клиент:</span> {{ state.object.client ? state.object.client.str : 'Нет итога' }}
              </div>
              <div v-if="state.object.object_type == 'account'" class="detail-tab-elem">
                <span class="detail-tab-label">Клиент:</span> {{ state.object.account ? state.object.account.str : 'Нет итога' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Создан:</span> {{ state.object.created ? formatDateTime(state.object.created) : 'Нет данных о создании' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Создатель:</span> {{ state.object.creator ? state.object.creator : 'Нет создателя' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Изменён:</span> {{ state.object.changed ? formatDateTime(state.object.changed) : 'Нет данных об изменениях' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Редактор:</span> {{ state.object.editor ? state.object.editor : 'Нет редактора' }}
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'interaction'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'interaction'" />

            </div>

          </div>
        </div>

      </div>
      <div v-else-if="!state.object.id" class="none-container">
        <div class="none-card">
          <div>Объект не найден.</div>
        </div>
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
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils'; 
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddInteraction: false,
  canViewInteraction: false,
  canEditInteraction: false,
});

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/interactions/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные задачи:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных задачи:', error);
  }
};

const showInteractionDeleteModal = ref(false);
const openInteractionDeleteModal = () => {
  showInteractionDeleteModal.value = true;
};
const closeInteractionDeleteModal = () => {
  showInteractionDeleteModal.value = false;
};
const confirmInteractionDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/interactions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeInteractionDeleteModal();
    router.push({ name: 'InteractionList' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
  }
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
        }
      });
      console.log('Разрешения пользователя загружены:', response.data);
      userPermissions = response.data
      localStorage.setItem('userPermissions', JSON.stringify(userPermissions));
    }
    
    state.globalPermissionsList = userPermissions.global_permissions || [];
    state.objectPermissionsDict = userPermissions.object_permissions || {};

    const id = route.params.id;
    console.log('ID объекта:', id);

    state.canAddInteraction = state.globalPermissionsList.includes('bpms.add_interaction');
    console.log('Права на добавление задач:', state.canAddInteraction);

    state.canViewInteraction = state.globalPermissionsList.includes('bpms.view_interaction') ||
      (state.objectPermissionsDict['bpms.view_interaction'] &&
      state.objectPermissionsDict['bpms.view_interaction'].includes(Number(id)));
    console.log('Права на просмотр задачи:', state.canViewInteraction);

    state.canEditInteraction = state.globalPermissionsList.includes('bpms.change_interaction') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_interaction']) &&
      state.objectPermissionsDict['bpms.change_interaction'].includes(Number(id)));
    console.log('Права на редактирование задачи:', state.canEditInteraction);

    state.canDeleteInteraction = state.globalPermissionsList.includes('bpms.delete_interaction') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_interaction']) &&
      state.objectPermissionsDict['bpms.delete_interaction'].includes(Number(id)));
    console.log('Права на удаление задачи:', state.canDeleteInteraction);

    state.canViewAccountObjectPermission = state.globalPermissionsList.includes('core.view_account_object_permission');
    console.log('Права на просмотр объектных прав аккаунтов:', state.canViewAccountObjectPermission);

    state.canAddAccountObjectPermission = state.globalPermissionsList.includes('core.add_account_object_permission');
    console.log('Права на добавление объектных прав аккаунтов:', state.canAddAccountObjectPermission);

    state.canDeleteAccountObjectPermission = state.globalPermissionsList.includes('core.delete_account_object_permission');
    console.log('Права на удаление объектных прав аккаунтов:', state.canDeleteAccountObjectPermission);

    state.canViewAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.view_accounts_group_object_permission');
    console.log('Права на просмотр объектных прав групп:', state.canViewAccountsGroupObjectPermission);

    state.canAddAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.add_accounts_group_object_permission');
    console.log('Права на добавление объектных прав групп:', state.canAddAccountsGroupObjectPermission);

    state.canDeleteAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.delete_accounts_group_object_permission');
    console.log('Права на удаление объектных прав групп:', state.canDeleteAccountsGroupObjectPermission);
    
  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const tabs = computed(() => [
  { name: 'details', label: 'Детали' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeInteractionTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeInteractionTab-${route.params.id}`, newTab);
  router.push({ query: { tab: newTab } });
  console.log('Загружен таб:', newTab);
});

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await fetchObject();
    await loadUserPermissions();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
