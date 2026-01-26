<template>
  <div v-if="loading">
    <div v-if="state.canViewTopic" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div v-if="state.object.topic_type == 'common_topic'" class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'task_topic'" class="detail-header-title">
                <h1>{{ state.object.task?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'queue_topic'" class="detail-header-title">
                <h1>{{ state.object.queue?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'public_plan_topic'" class="detail-header-title">
                <h1>{{ state.object.public_plan?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'public_task_topic'" class="detail-header-title">
                <h1>{{ state.object.public_task?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'new_topic'" class="detail-header-title">
                <h1>{{ state.object.new?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'material_topic'" class="detail-header-title">
                <h1>{{ state.object.material?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'course_topic'" class="detail-header-title">
                <h1>{{ state.object.course?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'test_topic'" class="detail-header-title">
                <h1>{{ state.object.test?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'event_template_topic'" class="detail-header-title">
                <h1>{{ state.object.event_template?.str || 'Безымянный топик' }}</h1>
              </div>
              <div v-if="state.object.topic_type == 'event_slot_topic'" class="detail-header-title">
                <h1>{{ state.object.event_slot?.str || 'Безымянный топик' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип топика:</span> {{ state.object.topic_type_display || 'Нет типа топика' }}
              </div>
              <div v-if="state.object.topic_type == 'task_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Задача:</span> {{ state.object.task ? state.object.task.str : 'Нет задачи' }}
              </div>
              <div v-if="state.object.topic_type == 'queue_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Очередь:</span> {{ state.object.queue ? state.object.queue.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'public_plan_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">План:</span> {{ state.object.public_plan ? state.object.public_plan.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'public_task_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Задание:</span> {{ state.object.public_task ? state.object.public_task.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'new_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Новость:</span> {{ state.object.new ? state.object.new.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'material_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Материал:</span> {{ state.object.material ? state.object.material.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'course_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Курс:</span> {{ state.object.course ? state.object.course.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'test_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Тест:</span> {{ state.object.test ? state.object.test.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'event_template_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Мероприятия:</span> {{ state.object.event_template ? state.object.event_template.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'event_slot_topic'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Слот мероприятия:</span> {{ state.object.event_slot ? state.object.event_slot.str : 'Нет очереди' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <router-link 
                v-if="state.canEditTopic" 
                :to="{ name: 'TopicEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteTopic" 
                @click="openTopicDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showTopicDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный топик' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmTopicDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeTopicDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Тип топика:</span> {{ state.object.topic_type_display || 'Нет типа топика' }}
              </div>
              <div v-if="state.object.topic_type == 'task_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Задача:</span> {{ state.object.task ? state.object.task.str : 'Нет задачи' }}
              </div>
              <div v-if="state.object.topic_type == 'queue_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Очередь:</span> {{ state.object.queue ? state.object.queue.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'public_plan_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">План:</span> {{ state.object.public_plan ? state.object.public_plan.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'public_task_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Задание:</span> {{ state.object.public_task ? state.object.public_task.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'new_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Новость:</span> {{ state.object.new ? state.object.new.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'material_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Материал:</span> {{ state.object.material ? state.object.material.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'course_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Курс:</span> {{ state.object.course ? state.object.course.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'test_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Тест:</span> {{ state.object.test ? state.object.test.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'event_template_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Мероприятия:</span> {{ state.object.event_template ? state.object.event_template.str : 'Нет очереди' }}
              </div>
              <div v-if="state.object.topic_type == 'event_slot_topic'" class="detail-tab-elem">
                <span class="detail-tab-label">Слот мероприятия:</span> {{ state.object.event_slot ? state.object.event_slot.str : 'Нет очереди' }}
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
              
              <TopicMessages :topic_id="topic_id" />

            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'topic'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'topic'" />

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
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils'; 
import TopicMessages from '../components/TopicMessages.vue';
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddTopic: false,
  canViewTopic: false,
  canEditTopic: false,
  canDeleteTopic: false,
  canDeleteMessageGlobal: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
});

const topic_id = ref(null);
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
    const response = await axios.get(`${baseUrl}/topics/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные топика:', response.data); 
    state.object = response.data;
    topic_id.value = state.object.id; // Обновляем реактивную переменную topic_id
    console.log('ID топика:', topic_id.value);
  } catch (error) {
    console.error('Ошибка при получении данных топика:', error);
  }
};

const showTopicDeleteModal = ref(false);
const openTopicDeleteModal = () => {
  showTopicDeleteModal.value = true;
};
const closeTopicDeleteModal = () => {
  showTopicDeleteModal.value = false;
};
const confirmTopicDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/topics/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeTopicDeleteModal();
    router.push({ name: 'TopicList' });
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

    state.canAddTopic = state.globalPermissionsList.includes('comments.add_topic');
    console.log('Права на добавление топик:', state.canAddTopic);

    state.canViewTopic = state.globalPermissionsList.includes('comments.view_topic') ||
      (state.objectPermissionsDict['comments.view_topic'] &&
      state.objectPermissionsDict['comments.view_topic'].includes(Number(id)));
    console.log('Права на просмотр топика:', state.canViewTopic);

    state.canEditTopic = state.globalPermissionsList.includes('comments.change_topic') ||
      (Array.isArray(state.objectPermissionsDict['comments.change_topic']) &&
      state.objectPermissionsDict['comments.change_topic'].includes(Number(id)));
    console.log('Права на редактирование топика:', state.canEditTopic);

    state.canDeleteTopic = state.globalPermissionsList.includes('comments.delete_topic') ||
      (Array.isArray(state.objectPermissionsDict['comments.delete_topic']) &&
      state.objectPermissionsDict['comments.delete_topic'].includes(Number(id)));
    console.log('Права на удаление топика:', state.canDeleteTopic);

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

const back = () => {
  router.back();
};

const tabs = computed(() => [
  { name: 'desc', label: 'Описание' },
  { name: 'messages', label: 'Содержание' },
  { name: 'details', label: 'Детали' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeTopicTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeTopicTab-${route.params.id}`, newTab);
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

watch(
  () => route.params.id,
  async (newId) => {
    console.log('Параметр id изменился на:', newId);
    await fetchObject();
  }
);

</script>

<style scoped>

</style>
