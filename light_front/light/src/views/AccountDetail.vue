<template>
  <div v-if="loading">
    <div v-if="state.canViewAccount" class="detail-page">
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
              <button 
                v-if="state.canEditAccount" 
                @click="provideAccess"
                class="button"
              >
              Отправить приглашение
              </button>
              <router-link 
                v-if="state.canEditAccount" 
                :to="{ name: 'AccountEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteAccount" 
                @click="openAccountDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>

            </div>
            <div v-if="showAccountDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.username || 'Безымянная учетная запись' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmAccountDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeAccountDeleteModal" class="minibutton">Отменить</button>
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
              <div v-if="state.canViewPlacement">
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
                              <th>
                                Действия
                              </th>
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
                          <td>
                            <div v-if="state.canEditPlacement || state.canDeletePlacement">
                              <div class="table-tab-menu">
                                <router-link 
                                  v-if="state.canEditPlacement" 
                                  :to="{ name: 'PlacementEdit', params: { id: placement.id }, query: { accountId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeletePlacement" 
                                  @click="openPlacementDeleteModal(placement)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showPlacementDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedPlacement.position.name || 'Безымянное назначение на должность' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmPlacementDelete(selectedPlacement.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closePlacementDeleteModal" class="minibutton">Отменить</button>
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
                  <div class="none-border">Нет должностей</div>
                </div>
              </div>
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
              <div v-if="state.canAddPlacement" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddPlacement"
                  :to="{ name: 'CreatePlacement', query: { accountId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'selfObjectPermissions'" class="table-tab">
              <div v-if="state.canViewAccountObjectPermission">
                <div v-if="state.object.self_object_permissions && state.object.self_object_permissions.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Владелец</th>
                              <th>Право</th>
                              <th>Тип контента</th>
                              <th>Объект</th>
                              <th>Действия</th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="self_object_permission in state.object.self_object_permissions" :key="self_object_permission.id">
                          <td>{{ self_object_permission.user.str ? self_object_permission.user.str: 'Нет данных' }}</td>
                          <td>{{ self_object_permission.permission.name ? self_object_permission.permission.name : 'Нет данных' }}</td>
                          <td>{{ self_object_permission.permission.content_type.str ? self_object_permission.permission.content_type.str : 'Нет данных' }}</td>
                          <td>{{ self_object_permission.content_object ? self_object_permission.content_object : 'Нет данных' }}</td>
                          <td>
                            <div v-if="state.canDeleteAccountObjectPermission">
                              <div class="table-tab-menu">
                                <button 
                                  v-if="state.canDeleteAccountObjectPermission" 
                                  @click="openAccountObjectPermissionDeleteModal(self_object_permission)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showAccountObjectPermissionDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedAccountObjectPermission.content_object || 'Объектное право без пользователя' }} {{ selectedAccountObjectPermission.permission.name || 'Безымянное объектное право' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmAccountObjectPermissionDelete(selectedAccountObjectPermission.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeAccountObjectPermissionDeleteModal" class="minibutton">Отменить</button>
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
                  <div class="none-border">Нет объектных прав</div>
                </div>
              </div>
            </div>
            
            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'account'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'account'" />

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
import { formatDate, formatDateTime, baseUrl, isTokenValid, frontendUrl , goBackSmart } from '../utils/utils';
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewAccount: false,
  canEditAccount: false,
  canDeleteAccount: false,
  canAddPlacement: false,
  canViewPlacement: false,
  canEditPlacement: false,
  canDeletePlacement: false,
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
    const response = await axios.get(`${baseUrl}/accounts/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные аккаунта:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных аккаунта:', error);
  }
};

const showAccountDeleteModal = ref(false);
const openAccountDeleteModal = () => {
  showAccountDeleteModal.value = true;
};
const closeAccountDeleteModal = () => {
  showAccountDeleteModal.value = false;
};
const confirmAccountDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/accounts/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeAccountDeleteModal();
    router.push({ name: 'AccountList' });
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const showPlacementDeleteModal = ref(false);
const selectedPlacement = ref(null);
const openPlacementDeleteModal = (placement) => {
  selectedPlacement.value = placement;
  showPlacementDeleteModal.value = true;
};
const closePlacementDeleteModal = () => {
  showPlacementDeleteModal.value = false;
};
const confirmPlacementDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/placements/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closePlacementDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const provideAccess = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    console.log('Отправляем данные для создания запроса:', form);

    const jsonData = {
      frontend_url: frontendUrl,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.post(`${baseUrl}/provide_access_user/${state.object.id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('Запрос создан:', jsonResponse.data);

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании запроса:', error.response.data);
    } else {
      console.error('Ошибка при создании запроса:', error.message);
    }
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

    state.canViewAccount = state.globalPermissionsList.includes('core.view_account') ||
      (state.objectPermissionsDict['core.view_account'] &&
      state.objectPermissionsDict['core.view_account'].includes(Number(id)));
    console.log('Права на просмотр аккаунтов:', state.canViewAccount);

    state.canEditAccount = state.globalPermissionsList.includes('core.change_account') ||
      (Array.isArray(state.objectPermissionsDict['core.change_account']) &&
      state.objectPermissionsDict['core.change_account'].includes(Number(id)));
    console.log('Права на редактирование аккаунтов:', state.canEditAccount);

    state.canDeleteAccount = state.globalPermissionsList.includes('core.delete_account') ||
      (Array.isArray(state.objectPermissionsDict['core.delete_account']) &&
      state.objectPermissionsDict['core.delete_account'].includes(Number(id)));
    console.log('Права на удаление аккаунтов:', state.canDeleteAccount);

    state.canAddPlacement = state.globalPermissionsList.includes('core.add_placement');
    console.log('Права на добавление назначений:', state.canAddPlacement);

    state.canViewPlacement = state.globalPermissionsList.includes('core.view_placement');
    console.log('Права на просмотр назначений:', state.canViewPlacement);

    state.canEditPlacement = state.globalPermissionsList.includes('core.change_placement');
    console.log('Права на редактирование назначений:', state.canEditPlacement);

    state.canDeletePlacement = state.globalPermissionsList.includes('core.delete_placement');
    console.log('Права на удаление назначений:', state.canDeletePlacement);

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
  goBackSmart(router);
};

const tabs = computed(() => [
  { name: 'details', label: 'Детали' },
  state.canViewPlacement ? { name: 'placements', label: 'Должности' } : null,
  state.canViewAccountObjectPermission ? { name: 'selfObjectPermissions', label: 'Объектные права аккаунта' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeAccountTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeAccountTab-${route.params.id}`, newTab);
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
