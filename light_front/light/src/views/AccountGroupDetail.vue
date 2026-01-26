<template>
  <div v-if="loading">
    <div v-if="state.canViewAccountGroup" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">

            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянная группа' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип:</span> {{ state.object.type_display || 'Нет типа' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div v-if="state.object.type === 'custom' " class="detail-card-text-elem">
                <span class="detail-card-text-label">Аккаунты добавлены:</span> {{ state.object.generator_group ? 'Да' : 'Нет' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <button 
                v-if="state.canEditAccountGroup" 
                @click="provideAccess"
                class="button"
              >
              Отправить приглашение
              </button>
              <router-link 
                v-if="state.canEditAccountGroup" 
                :to="{ name: 'AccountGroupEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteAccountGroup" 
                @click="openAccountGroupDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showAccountGroupDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянная группы' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmAccountGroupDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeAccountGroupDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Тип:</span> {{ state.object.type_display || 'Нет типа' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Права:</span>
                {{ state.object.permissions.length > 0 ? state.object.permissions.map(permission => permission.name).join(', ') : 'Нет прав' }}
              </div>
              <div v-if="state.object.type === 'custom' " class="detail-tab-elem">
                <span class="detail-tab-label">Аккаунты добавлены:</span> {{ state.object.generator_group ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Добавляемые аккунты:</span>
                {{ state.object.generator_group.added_users.length > 0 ? state.object.generator_group.added_users.map(user => user.str).join(', ') : 'Нет аккаунтов' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Исключаемые аккунты:</span>
                {{ state.object.generator_group.excluded_users.length > 0 ? state.object.generator_group.excluded_users.map(user => user.str).join(', ') : 'Нет аккаунтов' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Добавляемые группы:</span>
                {{ state.object.generator_group.added_groups.length > 0 ? state.object.generator_group.added_groups.map(group => group.name).join(', ') : 'Нет групп' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Исключаемые группы:</span>
                {{ state.object.generator_group.excluded_groups.length > 0 ? state.object.generator_group.excluded_groups.map(group => group.name).join(', ') : 'Нет групп' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Отработано от (дней):</span> {{ state.object.generator_group.days_worked_gte ? state.object.generator_group.days_worked_gte : 'Не указано' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Отработано до (дней):</span> {{ state.object.generator_group.days_worked_lte ? state.object.generator_group.days_worked_lte : 'Не указано' }}
              </div>
              <div v-if="state.object.generator_group" class="detail-tab-elem">
                <span class="detail-tab-label">Автообновление:</span> {{ state.object.generator_group.autoupdate ? 'Да' : 'Нет' }}
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
            <div v-if="activeTab === 'accounts'" class="table-tab">
                
                <div v-if="state.object.user_set  && state.object.user_set.length > 0" class="tab-search-field">
                    <input 
                      v-model="accountsSearchQuery" 
                      type="text" 
                      placeholder="Поиск" 
                      class="tab-search-input"
                    />
                  </div>

                <div v-if="filteredAccounts.length > 0" class="tab-list-inner">

                <div class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Имя пользователя</th>
                              <th>Личные данные</th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="account in paginatedAccounts" :key="account.id">
                          <td>{{ account.username || 'Нет данных' }}</td>
                          <td>{{ account.str || 'Нет данных' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div class="tab-pagination">
                    <button 
                      :disabled="accountsCurrentPage === 1" 
                      @click="accountsCurrentPage--"
                      class="tab-settings-button"
                    >
                      Назад
                    </button>
                    <span>Страница {{ accountsCurrentPage }} из {{ accountsTotalPages }}</span>
                    <button 
                      :disabled="accountsCurrentPage === accountsTotalPages" 
                      @click="accountsCurrentPage++"
                      class="tab-settings-button"
                    >
                      Вперед
                    </button>
                  </div>
              </div>

              <div v-else >
                <div class="none-border">Нет аккаунтов</div>
              </div>

              <div v-if="state.canAddAccountGroupGenerator || state.canEditAccountGroupGenerator " class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddAccountGroupGenerator && !state.object.generator_group"
                  :to="{ name: 'CreateAccountGroupGenerator', query: { groupId: state.object.id } }"
                  class="minibutton"
                >
                  Добавить
                </router-link>
                <router-link
                  v-if="state.canEditAccountGroupGenerator && state.object.generator_group"
                  :to="{ name: 'AccountGroupGeneratorEdit', params: { id: state.object.generator_group.id}, query: { groupId: state.object.id } }"
                  class="minibutton"
                >
                  Изменить
                </router-link>
              </div>

            </div>

            <div v-if="activeTab === 'selfObjectPermissions'" class="table-tab">
              <div v-if="state.canViewAccountsGroupObjectPermission">
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
                          <td>{{ self_object_permission.group.name ? self_object_permission.group.name : 'Нет данных' }}</td>
                          <td>{{ self_object_permission.permission.name ? self_object_permission.permission.name : 'Нет данных' }}</td>
                          <td>{{ self_object_permission.permission.content_type.str ? self_object_permission.permission.content_type.str : 'Нет данных' }}</td>
                          <td>{{ self_object_permission.content_object ? self_object_permission.content_object : 'Нет данных' }}</td>
                          <td>
                            <div v-if="state.canDeleteAccountsGroupObjectPermission">
                              <div class="table-tab-menu">
                                <button 
                                  v-if="state.canDeleteAccountsGroupObjectPermission" 
                                  @click="openAccountsGroupObjectPermissionDeleteModal(self_object_permission)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showAccountsGroupObjectPermissionDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedAccountsGroupObjectPermission.content_object || 'Объектное право без пользователя' }} {{ selectedAccountsGroupObjectPermission.permission.name || 'Безымянное объектное право' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmAccountsGroupObjectPermissionDelete(selectedAccountsGroupObjectPermission.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeAccountsGroupObjectPermissionDeleteModal" class="minibutton">Отменить</button>
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

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'accountsgroup'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'accountsgroup'" />

            </div>

          </div>
        </div>
      </div>
      <div v-else-if="!state.object.id" class="none-card">
        <div>Объект не найден</div>
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
  canViewAccountGroup: false,
  canEditAccountGroup: false,
  canDeleteAccountGroup: false,
  canViewAccount: false,
  canViewAccountIds: [],
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
  canAddAccountGroupGenerator: false,
  canViewAccountGroupGenerator: false,
  canEditAccountGroupGenerator: false,
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
    const response = await axios.get(`${baseUrl}/account_groups/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные группы:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных группы:', error);
  }
};

const showAccountGroupDeleteModal = ref(false);
const openAccountGroupDeleteModal = () => {
  showAccountGroupDeleteModal.value = true;
};
const closeAccountGroupDeleteModal = () => {
  showAccountGroupDeleteModal.value = false;
};
const confirmAccountGroupDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/account_groups/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeAccountGroupDeleteModal();
    router.push({ name: 'AccountGroupList' });
  } catch (error) {
    console.error('Ошибка удаления группы:', error);
  }
};

const accountsSearchQuery = ref('');
const accountsCurrentPage = ref(1);
const accountsItemsPerPage = 10;
const filteredAccounts = computed(() => {
  if (!accountsSearchQuery.value) return state.object.user_set;
  return state.object.user_set.filter(user => 
    user.first_name.toLowerCase().includes(accountsSearchQuery.value.toLowerCase()) || 
    user.last_name.toLowerCase().includes(accountsSearchQuery.value.toLowerCase()) || 
    user.username.toLowerCase().includes(accountsSearchQuery.value.toLowerCase())
  );
});
const accountsTotalPages = computed(() => Math.ceil(filteredAccounts.value.length / accountsItemsPerPage));
const paginatedAccounts = computed(() => {
  const start = (accountsCurrentPage.value - 1) * accountsItemsPerPage;
  const end = start + accountsItemsPerPage;
  return filteredAccounts.value.slice(start, end);
});
watch(accountsSearchQuery, () => {
  accountsCurrentPage.value = 1;
});

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

    const jsonResponse = await axios.post(`${baseUrl}/provide_access_group/${state.object.id}/`, jsonData, {
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

    state.canViewAccountGroup = state.globalPermissionsList.includes('core.view_accounts_group') ||
      (state.objectPermissionsDict['core.view_accounts_group'] &&
      state.objectPermissionsDict['core.view_accounts_group'].includes(Number(id)));
    console.log('Права на просмотр групп:', state.canViewAccountGroup);

    state.canEditAccountGroup = state.globalPermissionsList.includes('core.change_accounts_group') ||
      (Array.isArray(state.objectPermissionsDict['core.change_accounts_group']) &&
      state.objectPermissionsDict['core.change_accounts_group'].includes(Number(id)));
    console.log('Права на редактирование групп:', state.canEditAccountGroup);

    state.canDeleteAccountGroup = state.globalPermissionsList.includes('core.delete_accounts_group') ||
      (Array.isArray(state.objectPermissionsDict['core.delete_accounts_group']) &&
      state.objectPermissionsDict['core.delete_accounts_group'].includes(Number(id)));
    console.log('Права на удаление групп:', state.canDeleteAccountGroup);

    state.canViewAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.view_accounts_group_object_permission');
    console.log('Права на просмотр объектных прав групп:', state.canViewAccountsGroupObjectPermission);

    state.canAddAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.add_accounts_group_object_permission');
    console.log('Права на добавление объектных прав групп:', state.canAddAccountsGroupObjectPermission);

    state.canDeleteAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.delete_accounts_group_object_permission');
    console.log('Права на удаление объектных прав групп:', state.canDeleteAccountsGroupObjectPermission);

    state.canAddAccountGroupGenerator = state.globalPermissionsList.includes('core.add_group_generator') && state.object.type == 'custom';
    console.log('Права на добавление генератора группы:', state.canAddAccountGroupGenerator);

    state.canViewAccountGroupGenerator = state.globalPermissionsList.includes('core.view_group_generator');
    console.log('Права на просмотр генератора группы:', state.canViewAccountGroupGenerator);

    state.canEditAccountGroupGenerator = state.globalPermissionsList.includes('core.change_group_generator') && state.object.type == 'custom';
    console.log('Права на изменение генератора группы:', state.canEditAccountGroupGenerator);

    state.canViewAccountObjectPermission = state.globalPermissionsList.includes('core.view_account_object_permission');
    console.log('Права на просмотр объектных прав аккаунтов:', state.canViewAccountObjectPermission);

    state.canAddAccountObjectPermission = state.globalPermissionsList.includes('core.add_account_object_permission');
    console.log('Права на добавление объектных прав аккаунтов:', state.canAddAccountObjectPermission);

    state.canDeleteAccountObjectPermission = state.globalPermissionsList.includes('core.delete_account_object_permission');
    console.log('Права на удаление объектных прав аккаунтов:', state.canDeleteAccountObjectPermission);

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  router.back();
};

const tabs = computed(() => [
  { name: 'desc', label: 'Описание' },
  { name: 'details', label: 'Детали' },
  { name: 'accounts', label: 'Аккаунты' },
  state.canViewAccountsGroupObjectPermission ? { name: 'selfObjectPermissions', label: 'Объектные права группы' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeAccountGroupTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeAccountGroupTab-${route.params.id}`, newTab);
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
