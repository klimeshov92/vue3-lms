<template>
  <div v-if="loading">
    <div v-if="state.canViewCourse" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 

          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянный курс' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип курса:</span> {{ state.object.constructor_type_display || 'Нет типа курса' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="detail-menu button-group">

              <router-link
                v-if="state.object.last_task"
                :to="{ name: 'ScormContent', params: { id: state.object.last_task.id } }"
                target="_blank"
                rel="noopener noreferrer"
                class="button"
              >
                Пройти
              </router-link>

              <router-link 
                v-if="state.object.last_task" 
                :to="{ name: 'TaskDetail', params: { id: state.object.last_task.id } }"
                class="button"
              >
                Задача
              </router-link>

              <button 
                v-if="state.canSelfAssignment && !state.object.last_task" 
                @click="selfAssignment(state.object.self_assignment_task_template)"
                class="button"
              >
                Самоназначение
              </button>

              <button 
                v-if="state.object?.upload_file"
                @click="downloadCourse"
                class="button"
              >
                Скачать
              </button>
              <router-link 
                v-if="state.canEditCourse" 
                :to="{ name: 'CourseEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteCourse" 
                @click="openCourseDeleteModal"
                class="button"
              >
                Удалить
              </button>
            </div>
            <div v-if="showCourseDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный курс' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmCourseDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeCourseDeleteModal" class="minibutton">Отменить</button>
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
              <span class="detail-tab-label">Тип курса:</span> {{ state.object.constructor_type_display || 'Нет типа курса' }}
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

            <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'course'" />

          </div>

          <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

            <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'course'" />

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
  canViewCourse: false,
  canSelfAssignment: false,
  canEditCourse: false,
  canDeleteCourse: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
});

const downloadCourse = async () => {
  const courseId = state.object?.id;
  const courseName = state.object?.name || 'downloaded_course';

  if (!courseId) {
    console.warn('ID курса не найден.');
    return;
  }

  const token = localStorage.getItem('access_token');

  if (!token || !isTokenValid(token)) {
    console.warn('Токен невалиден, переход на логин');
    router.push({ name: 'Login' });
    return;
  }

  try {
    const url = `${baseUrl}/download_scorm/${courseId}/`;
    console.log(`Скачивание с URL: ${url}`);

    const response = await axios.get(url, {
      responseType: 'blob',
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.status === 200) {
      // Создаем Blob-объект из полученных данных (binary large object),
      // указываем тип контента из заголовков ответа, чтобы браузер понимал, что это за файл
      const blob = new Blob([response.data], { type: response.headers['content-type'] });

      // Создаем временный URL для Blob-объекта — он будет использоваться как ссылка на файл
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);

      // Устанавливаем имя файла, которое браузер покажет в диалоге сохранения
      link.setAttribute('download', courseName);

      // Добавляем ссылку в DOM (обязательно, иначе `click()` не сработает в некоторых браузерах)
      document.body.appendChild(link);

      // Программно кликаем по ссылке, чтобы запустить скачивание
      link.click();

      // Удаляем ссылку из DOM, чтобы не засорять документ
      link.remove();

      // Освобождаем память, удаляя временный URL
      window.URL.revokeObjectURL(link.href);

      console.log('Файл успешно скачан');
    } else {
      // Если код ответа не 200 — логируем ошибку
      console.error(`Ошибка при скачивании файла. Код: ${response.status}`);
    }


  } catch (error) {
    console.error('Ошибка при скачивании файла:', error);
  }
};

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
    const response = await axios.get(`${baseUrl}/courses/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные курса:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных курса:', error);
  }
};

const showCourseDeleteModal = ref(false);
const openCourseDeleteModal = () => {
  showCourseDeleteModal.value = true;
};
const closeCourseDeleteModal = () => {
  showCourseDeleteModal.value = false;
};
const confirmCourseDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/courses/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeCourseDeleteModal();
    router.push({ name: 'CourseList' });
  } catch (error) {
    console.error('Ошибка удаления курса:', error);
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

    state.canViewCourse = state.globalPermissionsList.includes('courses.view_course') ||
      (state.objectPermissionsDict['courses.view_course'] &&
      state.objectPermissionsDict['courses.view_course'].includes(Number(id)));
    console.log('Права на просмотр курсов:', state.canViewCourse);

    state.canSelfAssignment = state.canViewCourse && state.object.self_assignment_task_template
    console.log('Права на самоназначение:', state.canSelfAssignment);

    state.canEditCourse = state.globalPermissionsList.includes('courses.change_course') ||
      (Array.isArray(state.objectPermissionsDict['courses.change_course']) &&
      state.objectPermissionsDict['courses.change_course'].includes(Number(id)));
    console.log('Права на редактирование курсов:', state.canEditCourse);

    state.canDeleteCourse = state.globalPermissionsList.includes('courses.delete_course') ||
      (Array.isArray(state.objectPermissionsDict['courses.delete_course']) &&
      state.objectPermissionsDict['courses.delete_course'].includes(Number(id)));
    console.log('Права на удаление курсов:', state.canDeleteCourse);

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

const activeTab = ref(route.query.tab || localStorage.getItem(`activeCourseTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeCourseTab-${route.params.id}`, newTab);
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
