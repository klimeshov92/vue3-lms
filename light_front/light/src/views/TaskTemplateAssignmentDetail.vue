<template>
  <div v-if="loading">
    <div v-if="state.canViewTaskTemplateAssignment" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянное назначение шаблона задачи' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div v-if="!state.object.last_executor_interaction" class="detail-card-text-elem">
                <span class="detail-card-text-label">Взаимодействие:</span> {{ state.object.interaction ? state.object.interaction.str : 'Нет взаимодействия' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Шаблон задачи:</span> {{ state.object.task_template ? state.object.task_template.str : 'Нет плана' }}
              </div>
              <div v-if="state.object.task_template?.term_type != 'none'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Начало по плану:</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип исполнителя:</span> {{ state.object.executor_type_display || 'Нет типа исполнителя' }}
              </div>
              <div v-if="state.object.executor_type?.value == 'selected'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Исполнитель:</span> {{ state.object.executor ? state.object.executor.str : 'Нет исполнителя' }}
              </div>
              <div v-if="state.object.executor_type?.value == 'group'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Группа исполнителей:</span> {{ state.object.executor_group ? state.object.executor_group.str : 'Нет группы исполнителей' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Контроль руководителей:</span> {{ state.object.manager_control ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Группа контролеров:</span> {{ state.object.controller_group ? state.object.controller_group.str : 'Нет группы контролеров' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Группа наблюдателей:</span> {{ state.object.observer_group ? state.object.observer_group.str : 'Нет группы наблюдателей' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <button 
                v-if="state.canDeleteTaskTemplateAssignment" 
                @click="openTaskTemplateAssignmentDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showTaskTemplateAssignmentDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный задача' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmTaskTemplateAssignmentDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeTaskTemplateAssignmentDeleteModal" class="minibutton">Отменить</button>
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
              <div v-if="!state.object.last_executor_interaction" class="detail-tab-elem">
                <span class="detail-tab-label">Взаимодействие:</span> {{ state.object.interaction ? state.object.interaction.str : 'Нет взаимодействия' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Шаблон задачи:</span> {{ state.object.task_template ? state.object.task_template.str : 'Нет плана' }}
              </div>
              <div v-if="state.object.task_template?.term_type != 'none'" class="detail-tab-elem">
                <span class="detail-tab-label">Начало по плану</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Тип исполнителя:</span> {{ state.object.executor_type_display || 'Нет типа исполнителя' }}
              </div>
              <div v-if="state.object.executor_type?.value == 'selected'" class="detail-tab-elem">
                <span class="detail-tab-label">Исполнитель:</span> {{ state.object.executor ? state.object.executor.str : 'Нет исполнителя' }}
              </div>
              <div v-if="state.object.executor_type?.value == 'group'" class="detail-tab-elem">
                <span class="detail-tab-label">Группа исполнителей:</span> {{ state.object.executor_group ? state.object.executor_group.str : 'Нет группы исполнителей' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Контроль руководителей:</span> {{ state.object.manager_control ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Группа контролеров:</span> {{ state.object.controller_group ? state.object.controller_group.str : 'Нет группы контролеров' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Группа наблюдателей:</span> {{ state.object.observer_group ? state.object.observer_group.str : 'Нет группы наблюдателей' }}
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

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewTaskTemplateAssignment: false,
  canEditTaskTemplateAssignment: false,
  canDeleteTaskTemplateAssignment: false,
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
    const response = await axios.get(`${baseUrl}/task_template_assignments/${id}/`, {
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

const showTaskTemplateAssignmentDeleteModal = ref(false);
const openTaskTemplateAssignmentDeleteModal = () => {
  showTaskTemplateAssignmentDeleteModal.value = true;
};
const closeTaskTemplateAssignmentDeleteModal = () => {
  showTaskTemplateAssignmentDeleteModal.value = false;
};
const confirmTaskTemplateAssignmentDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/task_template_assignments/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeTaskTemplateAssignmentDeleteModal();
    router.push({ name: 'TaskTemplateAssignmentList' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
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

    state.canViewTaskTemplateAssignment = state.globalPermissionsList.includes('bpms.view_task_template_assignment') ||
      (state.objectPermissionsDict['bpms.view_task_template_assignment'] &&
      state.objectPermissionsDict['bpms.view_task_template_assignment'].includes(Number(id)));
    console.log('Права на просмотр задач:', state.canViewTaskTemplateAssignment);

    state.canEditTaskTemplateAssignment = state.globalPermissionsList.includes('bpms.change_task_template_assignment') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_task_template_assignment']) &&
      state.objectPermissionsDict['bpms.change_task_template_assignment'].includes(Number(id)));
    console.log('Права на редактирование задач:', state.canEditTaskTemplateAssignment);

    state.canDeleteTaskTemplateAssignment = state.globalPermissionsList.includes('bpms.delete_task_template_assignment') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_task_template_assignment']) &&
      state.objectPermissionsDict['bpms.delete_task_template_assignment'].includes(Number(id)));
    console.log('Права на удаление задач:', state.canDeleteTaskTemplateAssignment);


  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  router.back();
};

const tabs = computed(() => [
  { name: 'details', label: 'Детали' },
  { name: 'desc', label: 'Описание' },
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeTaskTemplateAssignmentTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeTaskTemplateAssignmentTab-${route.params.id}`, newTab);
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
