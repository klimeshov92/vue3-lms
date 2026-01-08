<template>
  <div v-if="loading">
    <div v-if="state.canViewQueue" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянная очередь' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Автоназначение исполнителя:</span> {{ state.object.auto_assignment ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <router-link 
                v-if="state.canEditQueue" 
                :to="{ name: 'QueueEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteQueue" 
                @click="openQueueDeleteModal"
                class="button"
              >
                Удалить
              </button>
            </div>
            <div v-if="showQueueDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянная очередь' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmQueueDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeQueueDeleteModal" class="minibutton">Отменить</button>
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

            <div v-if="activeTab === 'desc'" class="desc-tab">
              <div v-if="state.object.desc">
                {{ state.object.desc }}
              </div>
              <div v-else>
                <div class="none-border">Описание отсуствует</div>
              </div>
            </div>

            <div v-if="activeTab === 'details'" class="detail-tab">
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Автоназначение исполнителя:</span> {{ state.object.auto_assignment ? 'Да' : 'Нет' }}
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

            <div v-if="activeTab === 'queue_executors'" class="table-tab">
              <div v-if="state.canViewQueueExecutor">
                <div v-if="state.object.queue_executors && state.object.queue_executors.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Пункт</th>
                              <th>Исполнитель</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="queue_executor in state.object.queue_executors" :key="queue_executor.id">
                          <td>{{ queue_executor.item ? queue_executor.item : 'Нет данных' }}</td>
                          <td>{{ queue_executor.executor ? queue_executor.executor.str : 'Нет данных' }}</td>
                          <td>
                            <div v-if="state.canEditQueueExecutor || state.canDeleteQueueExecutor">
                              <div class="table-tab-menu">
                                <router-link 
                                  v-if="state.canEditQueueExecutor" 
                                  :to="{ name: 'QueueExecutorEdit', params: { id: queue_executor.id }, query: { queueId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeleteQueueExecutor" 
                                  @click="openQueueExecutorDeleteModal(queue_executor)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showQueueExecutorDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedQueueExecutor.str || 'Безымянный исполнитель очереди' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmQueueExecutorDelete(selectedQueueExecutor.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeQueueExecutorDeleteModal" class="minibutton">Отменить</button>
                                    </div>
                                  </div>
                                </div>                            
                              </div>
                            </div>
                            <div v-else> 
                              -
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else >
                  <div class="none-border">Нет исполнителей</div>
                </div>
              </div>
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
              <div v-if="state.canAddQueueExecutor" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddQueueExecutor"
                  :to="{ name: 'CreateQueueExecutor', query: { queueId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'queue_tasks'" class="table-tab">
              <div v-if="state.canViewQueueTask">
                <div v-if="state.object.queue_tasks && state.object.queue_tasks.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Пункт</th>
                              <th>Задача</th>
                              <th>Исполнитель</th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="queue_task in state.object.queue_tasks" :key="queue_task.id">
                          <td>{{ queue_task.item ? queue_task.item : 'Нет данных' }}</td>
                          <td>{{ queue_task.task ? queue_task.task.str : 'Нет данных' }}</td>
                          <td>{{ queue_task.task ? queue_task.executor.str : 'Нет данных' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else >
                  <div class="none-border">Нет задач</div>
                </div>
              </div>
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
              <div v-if="state.canAddQueueTask" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddQueueTask"
                  :to="{ name: 'CreateQueueTask', query: { queueId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'queue'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'queue'" />

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
import { ref, reactive, onMounted, computed, watch } from 'vue';
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
  canViewQueue: false,
  canEditQueue: false,
  canDeleteQueue: false,
  canAddQueueExecutor: false,
  canViewQueueExecutor: false,
  canEditQueueExecutor: false,
  canDeleteQueueExecutor: false,
  canAddQueueTask: false,
  canViewQueueTask: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
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
    const response = await axios.get(`${baseUrl}/queues/${id}/`, {
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

const showQueueDeleteModal = ref(false);
const openQueueDeleteModal = () => {
  showQueueDeleteModal.value = true;
};
const closeQueueDeleteModal = () => {
  showQueueDeleteModal.value = false;
};
const confirmQueueDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/queues/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeQueueDeleteModal();
    router.push({ name: 'QueueList' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
  }
};

const showQueueExecutorDeleteModal = ref(false);
const selectedQueueExecutor = ref(null);
const openQueueExecutorDeleteModal = (queue_executor) => {
  selectedQueueExecutor.value = queue_executor;
  showQueueExecutorDeleteModal.value = true;
};
const closeQueueExecutorDeleteModal = () => {
  showQueueExecutorDeleteModal.value = false;
};
const confirmQueueExecutorDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/queue_executors/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeQueueExecutorDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
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

    state.canViewQueue = state.globalPermissionsList.includes('bpms.view_queue') ||
      (state.objectPermissionsDict['bpms.view_queue'] &&
      state.objectPermissionsDict['bpms.view_queue'].includes(Number(id)));
    console.log('Права на просмотр очередей:', state.canViewQueue);

    state.canEditQueue = state.globalPermissionsList.includes('bpms.change_queue') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_queue']) &&
      state.objectPermissionsDict['bpms.change_queue'].includes(Number(id)));
    console.log('Права на редактирование очередей:', state.canEditQueue);

    state.canDeleteQueue = state.globalPermissionsList.includes('bpms.delete_queue') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_queue']) &&
      state.objectPermissionsDict['bpms.delete_queue'].includes(Number(id)));
    console.log('Права на удаление очередей:', state.canDeleteQueue);

    state.canAddQueueExecutor = state.globalPermissionsList.includes('bpms.add_queue_executor');
    console.log('Права на добавление исполнителей:', state.canAddQueueExecutor);

    state.canViewQueueExecutor = state.globalPermissionsList.includes('bpms.view_queue_executor');
    console.log('Права на просмотр исполнителей:', state.canViewQueueExecutor);

    state.canEditQueueExecutor = state.globalPermissionsList.includes('bpms.change_queue_executor');
    console.log('Права на редактирование исполнителей:', state.canEditQueueExecutor);

    state.canDeleteQueueExecutor = state.globalPermissionsList.includes('bpms.delete_queue_executor');
    console.log('Права на удаление исполнителей:', state.canDeleteQueueExecutor);

    state.canAddQueueTask = state.globalPermissionsList.includes('bpms.add_queue_task');
    console.log('Права на добавление задач:', state.canAddQueueTask);

    state.canViewQueueTask = state.globalPermissionsList.includes('bpms.view_queue_task');
    console.log('Права на просмотр задач:', state.canViewQueueTask);

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
  { name: 'desc', label: 'Описание' },
  { name: 'queue_executors', label: 'Исполнители очереди' },
  { name: 'queue_tasks', label: 'Задачи очереди' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeQueueTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeQueueTab-${route.params.id}`, newTab);
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
