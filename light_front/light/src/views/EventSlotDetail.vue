<template>
  <div v-if="loading">
    <div v-if="state.canViewEventSlot" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-image-outer">
            <div v-if="state.object.event_template.avatar" class="detail-card-image-inner">
              <img :src="state.object.event_template.avatar || '/default-avatar.png'" alt="Аватар" />
            </div>
            <div v-else class="detail-card-image-none">
              <span class="none-text">Нет аватара</span>
            </div>
          </div>
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.str || 'Безымянный мероприятия' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Статус:</span> {{ state.object.status_display || 'Нет статуса' }} 
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Количество участников:</span> {{ state.object.number_of_participants || 'Нет количества участников' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Регистрация открыта:</span> {{ state.object.registration ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Начало по плану:</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.deadline" class="detail-card-text-elem">
                <span class="detail-card-text-label">Завершение по плану:</span> {{ state.object.planned_end ? formatDateTime(state.object.planned_end) : 'Нет данных о завершении' }}
              </div>
            </div>
            <div class="detail-menu button-group">

              <router-link 
                v-if="state.object.last_task" 
                :to="{ name: 'TaskDetail', params: { id: state.object.last_task.id } }"
                class="button"
              >
                 К задаче
              </router-link>

              <button 
                v-if="state.canSelfAssignment" 
                @click="selfAssignment(state.object.self_assignment_task_template)"
                class="button"
              >
                Самоназначение
              </button>

              <router-link 
                v-if="state.canEditEventSlot" 
                :to="{ name: 'EventSlotEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteEventSlot" 
                @click="openEventSlotDeleteModal"
                class="button"
              >
                Удалить
              </button>
            </div>
            <div v-if="showEventSlotDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянного мероприятия' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmEventSlotDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeEventSlotDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Статус:</span> {{ state.object.status_display || 'Нет статуса' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Мероприятие:</span> {{ state.object.event_template.str || 'Нет мероприятия' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Количество участников:</span> {{ state.object.number_of_participants || 'Нет количества участников' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Регистрация открыта:</span> {{ state.object.registration ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Сроки:</span> {{ state.object.deadline ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Начало по плану:</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.deadline" class="detail-tab-elem">
                <span class="detail-tab-label">Завершение по плану:</span> {{ state.object.planned_end ? formatDateTime(state.object.planned_end) : 'Нет данных о завершении' }}
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

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'eventslot'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'eventslot'" />

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
  canViewEventSlot: false,
  canSelfAssignment: false,
  canEditEventSlot: false,
  canDeleteEventSlot: false,
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
    const response = await axios.get(`${baseUrl}/event_slots/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные мероприятия:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных мероприятия:', error);
  }
};

const showEventSlotDeleteModal = ref(false);
const openEventSlotDeleteModal = () => {
  showEventSlotDeleteModal.value = true;
};
const closeEventSlotDeleteModal = () => {
  showEventSlotDeleteModal.value = false;
};
const confirmEventSlotDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/event_slots/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeEventSlotDeleteModal();
    router.push({ name: 'EventSlotList' });
  } catch (error) {
    console.error('Ошибка удаления мероприятияа:', error);
  }
};

const selfAssignment = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
  try {
    const self_assignment = await axios.post(`${baseUrl}/self_assignment/${id}/`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('Самоназначение:', self_assignment.data); 
    router.push({ name: 'TaskDetail', params: { id: self_assignment.data.id } });
  } catch (error) {
    console.error('Ошибка самоназначения:', error);
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

    state.canViewEventSlot = state.globalPermissionsList.includes('events.view_event_slot') ||
      (state.objectPermissionsDict['events.view_event_slot'] &&
      state.objectPermissionsDict['events.view_event_slot'].includes(Number(id)));
    console.log('Права на просмотр аккаунтов:', state.canViewEventSlot);

    state.canSelfAssignment = state.canViewEventSlot && state.object.self_assignment_task_template
    console.log('Права на самоназначение:', state.canSelfAssignment);

    state.canEditEventSlot = state.globalPermissionsList.includes('events.change_event_slot') ||
      (Array.isArray(state.objectPermissionsDict['events.change_event_slot']) &&
      state.objectPermissionsDict['events.change_event_slot'].includes(Number(id)));
    console.log('Права на редактирование аккаунтов:', state.canEditEventSlot);

    state.canDeleteEventSlot = state.globalPermissionsList.includes('events.delete_event_slot') ||
      (Array.isArray(state.objectPermissionsDict['events.delete_event_slot']) &&
      state.objectPermissionsDict['events.delete_event_slot'].includes(Number(id)));
    console.log('Права на удаление аккаунтов:', state.canDeleteEventSlot);

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
  { name: 'desc', label: 'Описание' },
  { name: 'details', label: 'Детали' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeEventSlotTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeEventSlotTab-${route.params.id}`, newTab);
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
