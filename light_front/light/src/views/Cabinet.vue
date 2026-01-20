<template>
  <div v-if="loading">
    <div v-if="state.canUseCabinet" class="detail-page">
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
                <h1>{{ state.object.username || 'Безымянная учетная запись' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Фамилия:</span> {{ state.object.last_name || 'Нет фамилии' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Имя:</span> {{ state.object.first_name || 'Нет имени' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Отчество:</span> {{ state.object.fathers_name || 'Нет отчества' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Электронная почта:</span> {{ state.object.email || 'Нет электронной почты' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Активен:</span> {{ state.object.is_active ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Последний вход:</span> {{ state.object.last_login ? formatDate(state.object.last_login) : 'Нет данных о последнем входе' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <button @click="logout" class="button">Выйти</button>
              <router-link 
                :to="{ name: 'Login' }"
                class="button"
              >
                Сменить аккаунт
              </router-link>
              <router-link 
                :to="{ name: 'PasswordResetRequest' }"
                class="button"
              >
                Сменить пароль
              </router-link>
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
                <span class="detail-tab-label">Фамилия:</span> {{ state.object.last_name || 'Нет фамилии' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Имя:</span> {{ state.object.first_name || 'Нет имени' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Отчество:</span> {{ state.object.fathers_name || 'Нет отчества' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Электронная почта:</span> {{ state.object.email || 'Нет электронной почты' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Активен:</span> {{ state.object.is_active ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Последний вход:</span> {{ state.object.last_login ? formatDate(state.object.last_login) : 'Нет данных о последнем входе' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">MDM ID:</span> {{ state.object.mdm_id || 'Нет MDM ID' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Дата регистрации:</span> {{ state.object.date_joined ? formatDate(state.object.date_joined) : 'Нет данных о регистрации' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Самостоятельная регистрация:</span> {{ state.object.self_registration ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Подтверждение электронной почты:</span> {{ state.object.email_confirmed ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Согласие с политикой конфиденциальности:</span> {{ state.object.agree_to_privacy_policy ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Согласие на обработку персональных данных:</span> {{ state.object.agree_to_data_processing ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Персонал:</span> {{ state.object.is_staff ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Суперпользователь:</span> {{ state.object.is_superuser ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Права:</span>
                {{ state.object.user_permissions.length > 0 ? state.object.user_permissions.map(permission => permission.name).join(', ') : 'Нет прав' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Группы:</span>
                {{ state.object.groups.length > 0 ? state.object.groups.map(group => group.name).join(', ') : 'Нет групп' }}
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
            
            <div v-if="activeTab === 'placements'" class="table-tab">
              <div>
                <div v-if="state.object.placements && state.object.placements.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Организация</th>
                              <th>Подразделение</th>
                              <th>Должность</th>
                              <th>Роль</th>
                              <th>Дата начала</th>
                              <th>Дата конца</th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="placement in state.object.placements" :key="placement.id">
                          <td>{{ placement.position.subdivision.organization ? placement.position.subdivision.organization.legal_name : 'Нет данных' }}</td>
                          <td>{{ placement.position.subdivision ? placement.position.subdivision.name : 'Нет данных' }}</td>
                          <td>{{ placement.position ? placement.position.name : 'Нет данных' }}</td>
                          <td>  
                            {{
                                placement.role === 'employee'
                                  ? 'Сотрудник'
                                  : placement.role === 'manager'
                                  ? 'Менеджер'
                                  : 'Нет данных'
                              }}
                          </td>
                          <td>{{ placement.start_date ? formatDate(placement.start_date) : 'Нет данных' }}</td>
                          <td>{{ placement.end_date ? formatDate(placement.end_date) : 'Нет данных' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else >
                  <div class="none-border">Нет должностей</div>
                </div>
              </div>
            </div>

            <div v-if="activeTab === 'notification_settings'">
              <div v-if="state.object.notification_settings" class="detail-tab">
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Отслеживание своих задач:</span> {{ state.object.notification_settings.self_tasks_tracking ? 'Да' : 'Нет' }}
                </div>
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Отслеживание задач на контроле:</span> {{ state.object.notification_settings.controlled_tasks_tracking ? 'Да' : 'Нет' }}
                </div>
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Отслеживание задач под наблюдением:</span> {{ state.object.notification_settings.observed_tasks_tracking ? 'Да' : 'Нет' }}
                </div>
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Период напоминания для своих задач (дней):</span> {{ state.object.notification_settings.self_tasks_reminder_period || 'Нет данных' }}
                </div>
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Период напоминания для задач на контроле (дней):</span> {{ state.object.notification_settings.controlled_tasks_reminder_period || 'Нет данных' }}
                </div>
                <div class="detail-tab-elem">
                  <span class="detail-tab-label">Период напоминания для задач под наблюдением (дней):</span> {{ state.object.notification_settings.observed_tasks_reminder_period || 'Нет данных' }}
                </div>
              </div>
              <div v-else >
                <div class="none-border">Нет настроек оповещений</div>
              </div>
              <div v-if="state.object.notification_settings" class="tab-menu minibutton-group">
                <router-link 
                  :to="{ name: 'NotificationSettingsEdit', params: { id: state.object.notification_settings.id } }"
                  class="minibutton"
                >
                  Изменить
                </router-link>
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
import { formatDate, formatDateTime, baseUrl, isTokenValid, auth_user_id, clearUserId } from '../utils/utils'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const logout = () => {
  localStorage.removeItem('access_token');
  clearUserId();
  router.push({ name: 'HomePage' });
};

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canUseCabinet: false,
});

const id = ref(null)
const fetchObject = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/cabinet/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные аккаунта:', response.data); 
    state.object = response.data;
    id.value = response.data.id
    console.log('ID aккаунта:', id.value); 
  } catch (error) {
    console.error('Ошибка при получении данных аккаунта:', error);
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

    console.log('ID aккаунта:', id.value); 
    state.canUseCabinet = id.value == validToken.user_id;
    console.log('Права на просмотр кабинета:', state.canUseCabinet);

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  router.back();
};

const tabs = computed(() => [
  { name: 'details', label: 'Детали' },
  { name: 'placements', label: 'Должности' },
  { name: 'notification_settings', label: 'Настройки уведомлений' },
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeAccountTab-${id.value}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeAccountTab-${id.value}`, newTab);
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
