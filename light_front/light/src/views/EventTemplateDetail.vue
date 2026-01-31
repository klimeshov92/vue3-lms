<template>
  <div v-if="loading">
    <div v-if="state.canViewEventTemplate" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-image-outer">
            <div v-if="state.object.avatar" class="detail-card-image-inner">
              <img :src="state.object.avatar || '/default-avatar.png'" alt="Аватар" />
            </div>
            <div v-else class="detail-card-image-none">
              <span class="none-text">Нет аватара</span>
            </div>
          </div>
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянный мероприятия' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Статус задачи:</span> {{ state.object.last_task?.result ? state.object.last_task?.result.status_display : 'Не назначено' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Форомат:</span> {{ state.object.format_display || 'Нет формата' }}
              </div>
              <div v-if="state.object.format == 'face_to_face' || state.object.format == 'mixed'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Локация:</span> {{ state.object.location || 'Нет локации' }}
              </div>
              <div v-if="state.object.format == 'webinar' || state.object.format == 'mixed'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Ссылка:</span> {{ state.object.link || 'Нет ссылки' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Ведущие:</span>
                {{ state.object.admins.length > 0 ? state.object.admins.map(admin => admin.str).join(', ') : 'Нет ведущих' }}
              </div> 
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div> 
            </div>
            <div class="detail-menu button-group">

              <router-link 
                v-if="state.object.last_task" 
                :to="{ name: 'TaskDetail', params: { id: state.object.last_task.id } }"
                class="button"
              >
                Задача
              </router-link>

              <button 
                v-if="state.canSelfAssignment"
                @click="selfAssignment(state.object.self_assignment_task_template)"
                class="button"
              >
                Самоназначение
              </button>

              <router-link 
                v-if="state.canEditEventTemplate" 
                :to="{ name: 'EventTemplateEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>

              <button 
                v-if="state.canDeleteEventTemplate" 
                @click="openEventTemplateDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showEventTemplateDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянного мероприятия' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmEventTemplateDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeEventTemplateDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Статус задачи:</span> {{ state.object.last_task?.result ? state.object.last_task?.result.status_display : 'Не назначено' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Форомат:</span> {{ state.object.format_display || 'Нет формата' }}
              </div>
              <div v-if="state.object.format == 'face_to_face' || state.object.format == 'mixed'" class="detail-tab-elem">
                <span class="detail-tab-label">Локация:</span> {{ state.object.location || 'Нет локации' }}
              </div>
              <div v-if="state.object.format == 'webinar' || state.object.format == 'mixed'" class="detail-tab-elem">
                <span class="detail-tab-label">Ссылка:</span> {{ state.object.link || 'Нет ссылки' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Ведущие:</span>
                {{ state.object.admins.length > 0 ? state.object.admins.map(admin => admin.str).join(', ') : 'Нет ведущих' }}
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

            <div v-if="activeTab === 'messages'" class="topic-tab">
              
              <TopicMessages :topic_id="state.object?.topic.id" />

            </div>
            
            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'eventtemplate'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'eventtemplate'" />

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
import { formatDate, formatDateTime, baseUrl, isTokenValid , goBackSmart } from '../utils/utils'; 
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 
import TopicMessages from '../components/TopicMessages.vue';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewEventTemplate: false,
  canEditEventTemplate: false,
  canDeleteEventTemplate: false,
  canSelfAssignment: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
  canViewTopic: false,
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
    const response = await axios.get(`${baseUrl}/event_templates/${id}/`, {
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

const showEventTemplateDeleteModal = ref(false);
const openEventTemplateDeleteModal = () => {
  showEventTemplateDeleteModal.value = true;
};
const closeEventTemplateDeleteModal = () => {
  showEventTemplateDeleteModal.value = false;
};
const confirmEventTemplateDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/event_templates/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeEventTemplateDeleteModal();
    router.push({ name: 'EventTemplateList' });
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

    const id = route.params.id;
    console.log('ID объекта:', id);

    state.canViewEventTemplate = state.globalPermissionsList.includes('events.view_event_template') ||
      (state.objectPermissionsDict['events.view_event_template'] &&
      state.objectPermissionsDict['events.view_event_template'].includes(Number(id)));
    console.log('Права на просмотр аккаунтов:', state.canViewEventTemplate);

    state.canSelfAssignment = state.canViewEventTemplate && 
    state.object.self_assignment_task_template && state.object.self_assignment_task_template && 
    (!state.object.last_task || (state.object.last_task?.result?.status == 'failed' || state.object.last_task?.result?.status == 'canceled'))
    console.log('Права на самоназначение:', state.canSelfAssignment);

    state.canEditEventTemplate = state.globalPermissionsList.includes('events.change_event_template') ||
      (Array.isArray(state.objectPermissionsDict['events.change_event_template']) &&
      state.objectPermissionsDict['events.change_event_template'].includes(Number(id)));
    console.log('Права на редактирование аккаунтов:', state.canEditEventTemplate);

    state.canDeleteEventTemplate = state.globalPermissionsList.includes('events.delete_event_template') ||
      (Array.isArray(state.objectPermissionsDict['events.delete_event_template']) &&
      state.objectPermissionsDict['events.delete_event_template'].includes(Number(id)));
    console.log('Права на удаление аккаунтов:', state.canDeleteEventTemplate);

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

    if (state.object.topic) {
      state.canViewTopic = state.globalPermissionsList.includes('comments.view_topic') ||
      (state.objectPermissionsDict['comments.view_topic'] && state.objectPermissionsDict['comments.view_topic'].includes(Number(state.object.topic.id)));
      console.log('Права на просмотр топика:', state.canViewTopic);
    }

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  goBackSmart(router);
};

const tabs = computed(() => [
  { name: 'desc', label: 'Описание' },
  { name: 'details', label: 'Детали' },
  state.canViewTopic ? { name: 'messages', label: 'Комментарии' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeEventTemplateTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeEventTemplateTab-${route.params.id}`, newTab);
  router.push({ query: { tab: newTab } });
  console.log('Загружен таб:', newTab);
});

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await fetchObject();
    await checkPermissionsVersion();
    await loadUserPermissions();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
