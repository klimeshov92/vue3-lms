<template>

  <div v-if="loading">

    <div v-if="state.canViewAnalytic" class="analytic-page">

      <div class="analytic-header">
        <h1>Аналитика по задачам</h1>
      </div>

      <form class="analytic-form" id="analytic-form">

          <div class="form-field">
            <label class="form-label">Отчет:</label>
            <multiselect
              v-model="form.report"
              :options="reports"
              :searchable="false"
              :multiple="false"
              :close-on-select="true"
              :clear-on-select="true"
              placeholder="Выберите отчет"
              label="label"
              track-by="value"
              :preselect-first="false"
              :select-label="``"
              :deselect-label="``"
              :selected-label="``"
            />
            <span v-if="errors.report" class="error">{{ errors.report }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label class="form-label">Шаблон задачи:</label>
            <multiselect
              v-model="form.task_template"
              :options="task_templates"
              :multiple="false"
              :close-on-select="true"
              :clear-on-select="false"
              :preserve-search="true"
              placeholder="Выберите шаблон задачи"
              label="str"
              track-by="id"
              :preselect-first="false"
              :select-label="``"
              :deselect-label="``"
              :selected-label="``"
            >
              <template #noOptions>
                <span>Список пуст</span>
              </template>
              <template #noResult>
                <span>Ничего не найдено</span>
              </template>
            </multiselect>
            <span v-if="errors.task_template" class="error">{{ errors.task_template }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label class="form-label">Исполнители:</label>
            <multiselect
              v-model="form.executor_type"
              :options="executor_types"
              :searchable="false"
              :multiple="false"
              :close-on-select="true"
              :clear-on-select="true"
              placeholder="Выберите тип исполнителя"
              label="label"
              track-by="value"
              :preselect-first="false"
              :select-label="``"
              :deselect-label="``"
              :selected-label="``"
            />
            <span v-if="errors.executor_type" class="error">{{ errors.executor_type }}</span>
          </div>

          <div v-if="form.executor_type?.value == 'group'" class="form-field">
            <label class="form-label">Группа:</label>
            <multiselect
              v-model="form.group"
              :options="groups"
              :multiple="false"
              :close-on-select="true"
              :clear-on-select="false"
              :preserve-search="true"
              placeholder="Выберите группу исполнителей"
              label="str"
              track-by="id"
              :preselect-first="false"
              :select-label="``"
              :deselect-label="``"
              :selected-label="``"
            >
              <template #noOptions>
                <span>Список пуст</span>
              </template>
              <template #noResult>
                <span>Ничего не найдено</span>
              </template>
            </multiselect>
            <span v-if="errors.group" class="error">{{ errors.group }}</span>
          </div>

          <div v-if="form.executor_type?.value == 'account'" class="form-field">
            <label class="form-label">Исполнитель:</label>
            <multiselect
              v-model="form.account"
              :options="accounts"
              :multiple="false"
              :close-on-select="true"
              :clear-on-select="false"
              :preserve-search="true"
              placeholder="Выберите исполнителя"
              label="str"
              track-by="id"
              :preselect-first="false"
              :select-label="``"
              :deselect-label="``"
              :selected-label="``"
            >
              <template #noOptions>
                <span>Список пуст</span>
              </template>
              <template #noResult>
                <span>Ничего не найдено</span>
              </template>
            </multiselect>
            <span v-if="errors.account" class="error">{{ errors.account }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label for="planned_start_gte" class="form-label">Планируемое начало не ранее:</label>
            <input v-model="form.planned_start_gte" id="planned_start_gte" type="datetime-local" class="form-input" />
            <span v-if="errors.planned_start_gte" class="error">{{ errors.planned_start_gte }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label for="planned_start_lte" class="form-label">Планируемое начало не позднее:</label>
            <input v-model="form.planned_start_lte" id="planned_start_lte" type="datetime-local" class="form-input" />
            <span v-if="errors.planned_start_lte" class="error">{{ errors.planned_start_lte }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label for="planned_end_gte" class="form-label">Планируемое завершение не ранее:</label>
            <input v-model="form.planned_end_gte" id="planned_end_gte" type="datetime-local" class="form-input" />
            <span v-if="errors.planned_end_gte" class="error">{{ errors.planned_end_gte }}</span>
          </div>

          <div v-if="form.report?.value == 'task_template'" class="form-field">
            <label for="planned_end_lte" class="form-label">Планируемое завершение не позднее:</label>
            <input v-model="form.planned_end_lte" id="planned_end_lte" type="datetime-local" class="form-input" />
            <span v-if="errors.planned_end_lte" class="error">{{ errors.planned_end_lte }}</span>
          </div>

      </form>

      <div class="analytic-menu button-group">
        <button @click="loadObjects(form)" class="button">Сформировать отчет</button>
        <button @click="resetObjects" class="button">Сбросить отчет</button>
      </div>

      <div class="analytic-content">
        <div v-if="state.results.length !== 0" class="analytic-info">

          <div class="test-section-tab-flex">

            <div class="test-section-tab-item">

              <div class="test-section-tab-item-top">

                <div class="test-section-tab-item-title">
                  <h2>
                    Общая
                  </h2>
                </div>

              </div>

              <div class="test-section-tab-item-detail">
                
                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Всего:</span>  {{ state.results ? state.results.tasks_started : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Завершено:</span>  {{ state.results ? state.results.tasks_finished : 'Нет данных' }}
                </div>

              </div>

              <div class="test-section-tab-item-menu-outer">
                <!--<div class="test-section-tab-item-menu-inner">
                    
                </div>-->
              </div>

            </div>
            
            <div class="test-section-tab-item">

              <div class="test-section-tab-item-top">

                <div class="test-section-tab-item-title">
                  <h2>
                    Статусы
                  </h2>
                </div>

              </div>

              <div class="test-section-tab-item-detail">
                
                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">В ожидании:</span>  {{ state.results.statuses ? state.results.statuses.waiting : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Назначено:</span>  {{ state.results.statuses ? state.results.statuses.assigned : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">В процессе:</span>  {{ state.results.statuses ? state.results.statuses.in_progress : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Выполнено:</span>  {{ state.results.statuses ? state.results.statuses.completed : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Провалено:</span>  {{ state.results.statuses ? state.results.statuses.failed : 'Нет данных' }}
                </div>

                <div class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">Отменено:</span>  {{ state.results.statuses ? state.results.statuses.canceled : 'Нет данных' }}
                </div>

              </div>

              <div class="test-section-tab-item-menu-outer">
                <!--<div class="test-section-tab-item-menu-inner">
                    
                </div>-->
              </div>

            </div>

            <div class="test-section-tab-item">

              <div class="test-section-tab-item-top">

                <div class="test-section-tab-item-title">
                  <h2>
                    Итоги
                  </h2>
                </div>

              </div>

              <div v-if="state.results.outcomes && state.results.outcomes.length > 0" class="test-section-tab-item-detail">
                
                <div v-for="outcome in state.results.outcomes" :key="outcome.id" class="test-section-tab-item-detail-elem">
                  <span class="test-section-tab-item-detail-label">{{ outcome.name ? outcome.name : 'Нет данных' }}:</span> {{ outcome.count ? outcome.count : 'Нет данных' }}
                </div>

              </div>
              <div v-else class="none-border-container">
                <div class="none-border-mini">Нет итогов задач </div>
              </div>


              <div class="test-section-tab-item-menu-outer">
                <!--<div class="test-section-tab-item-menu-inner">
                    
                </div>-->
              </div>

            </div>

            <div class="test-section-tab-item">

              <div class="test-section-tab-item-top">

                <div class="test-section-tab-item-title">
                  <h2>
                    Список
                  </h2>
                </div>

              </div>

              <div class="test-section-table_container">
                <div v-if="state.results.tasks && state.results.tasks.length > 0" class="test-section-table-outer">
                  <div class="test-section-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Взаимодействие</th>
                              <th>Исполнитель</th>
                              <th>Статус</th>
                              <th>Итог</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="task in state.results.tasks" :key="task.id">

                          <td>{{ task.interaction?.str ? task.interaction.str : '-' }}</td>
                          <td>{{ task.executor?.str ? task.executor.str : '-' }}</td>
                          <td>{{ task.result?.status_display ? task.result.status_display : '-' }}</td>
                          <td>{{ task.result?.outcome?.str ? task.result.outcome.str : '-' }}</td>

                          <td>
                            <div>
                              <div class="test-section-menu">

                                <router-link :to="{ name: 'TaskDetail', params: { id: task.id },  query: { tab: 'desc' } }" class="test-section-button">
                                  Подробнее
                                </router-link>
                      
                              </div>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else >
                  <div class="none-border-mini">Нет задач </div>
                </div>
              </div>

              <div class="test-section-tab-item-menu-outer">
                <!--<div class="test-section-tab-item-menu-inner">
                    
                </div>-->
              </div>

            </div>

          </div>

        </div>
        <div v-else class="none-card">
          <div>Сформируйте отчет</div>
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
import axios from 'axios';
import { reactive, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const reports = [
  { label: 'По шаблону задачи', value: 'task_template' },
];

const executor_types = [
  { label: 'Все', value: 'all' },
  { label: 'Группа', value: 'group' },
  { label: 'Аккаунт', value: 'account' },
];

const form = reactive({
  report: '',
  task_template: null,
  executor_type: '',
  group: null,
  account: null,
  planned_start_gte: null,
  planned_start_lte: null,
  planned_end_gte: null,
  planned_end_lte: null,
});

const state = reactive({
  results: [],
});

const task_templates = ref([]);
const loadTaskTemplate = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/task_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    task_templates.value = (response.data.results || []).filter(
      task_template => !task_template.is_child
    );
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

const accounts = ref([]);
const loadAccounts = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/accounts/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    accounts.value = response.data.results || [];
    console.log('Аккаунты загружены:', accounts.value);
  } catch (error) {
    console.error('Ошибка при загрузке сотрудников:', error.response ? error.response.data : error.message);
  }
};

const groups = ref([]);
const loadGroups = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/account_groups/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    groups.value = response.data.results || [];
    console.log('Группы загружены:', groups.value);
  } catch (error) {
    console.error('Ошибка при загрузке групп:', error.response ? error.response.data : error.message);
  }
};

const errors = reactive({});
const validateForm = () => {

  errors.report = form.report?.value ? '' : 'Выберите отчет';
  if (form.report?.value === 'task_template') {
    errors.task_template = form.task_template ? '' : 'Выберите шаблон задачи';
  }
  errors.executor_type =  form.executor_type?.value ? '' : 'Выберите тип исполнителя'
  if (form.executor_type?.value === 'group') {
    errors.group = form.group ? '' : 'Выберите группу';
  }
  if (form.executor_type?.value === 'account') {
    errors.account = form.account ? '' : 'Выберите аккаунт';
  }
  return Object.values(errors).every((error) => !error);
};

const loadObjects = async () => {


  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }
  loading.value = false;
  try {
    console.log('Отправляем данные для создания объекта:', form);


    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonData = {
      report: form.report?.value,
    };

    if (form.report?.value === 'task_template') {
      jsonData.task_template = form.task_template?.id
      jsonData.executor_type = form.executor_type.value
      if (form.executor_type?.value === 'group') {
        jsonData.group = form.group?.id
      }
      if (form.executor_type?.value === 'account') {
        jsonData.account = form.account?.id
      }
      jsonData.planned_start_gte = form.planned_start_gte
      jsonData.planned_start_lte = form.planned_start_lte
      jsonData.planned_end_gte = form.planned_end_gte
      jsonData.planned_end_lte = form.planned_end_lte

      console.log('JSON данные перед отправкой:', jsonData);

      const jsonResponse = await axios.post(`${baseUrl}/analytics_task_template/`, jsonData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log('Данные отчеты:', jsonResponse.data);
      state.results = jsonResponse.data
    }

    loading.value = true;

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }
};

const resetObjects = () => {
  console.log('Сбрасываем фильтры');
  form.report = '',
  form.task_template = null,
  form.executor_type = '',
  form.group = null,
  form.account = null,
  form.planned_start_gte = '';
  form.planned_start_lte = '';
  form.planned_end_gte = '';
  form.planned_end_lte = '';
  state.results = []
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
        },
      });
      console.log('Разрешения пользователя загружены:', response.data);
      userPermissions = response.data
      localStorage.setItem('userPermissions', JSON.stringify(userPermissions));
    }

    state.globalPermissionsList = userPermissions.global_permissions || [];
    state.objectPermissionsDict = userPermissions.object_permissions || {};
    
    state.canViewAnalytic = state.globalPermissionsList.includes('bpms.view_analytics') || !!state.objectPermissionsDict['core.view_category'];
    console.log('Права на просмотр аналитики:', state.canViewAnalytic);
    
  } catch (error) {
    console.error('Ошибка при получении разрешений пользователя:', error);
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadTaskTemplate(),
    await loadGroups(),
    await loadAccounts(),
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
