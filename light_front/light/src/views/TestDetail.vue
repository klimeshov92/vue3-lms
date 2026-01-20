<template>
  <div v-if="loading">
    <div v-if="state.canViewTest" class="detail-page">
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
                <h1>{{ state.object.name || 'Безымянный тест' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Проходной балл:</span> {{ state.object.passing_score || 'Нет проходного балла' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Время на выполнение (минут):</span> {{ state.object.time_to_complete || 'Нет времени на выполнение' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Попытки:</span> {{ state.object.attempts || 'Нет попыток' }}
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
                v-if="state.canSelfAssignment && !state.object.last_task" 
                @click="selfAssignment(state.object.self_assignment_task_template)"
                class="button"
              >
                Самоназначение
              </button>

              <router-link 
                v-if="state.canEditTest" 
                :to="{ name: 'TestEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteTest" 
                @click="openTestDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showTestDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.username || 'Безымянная учетная запись' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmTestDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeTestDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Проходной балл:</span> {{ state.object.passing_score || 'Нет проходного балла' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Время на выполнение (минут):</span> {{ state.object.time_to_complete || 'Нет времени на выполнение' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Попытки:</span> {{ state.object.attempts || 'Нет попыток' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Случайный порядок вопросов:</span> {{ state.object.random_questions ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Случайный порядок ответов:</span> {{ state.object.random_answers ? 'Да' : 'Нет' }}
              </div>

              <div class="detail-tab-elem">
                <span class="detail-tab-label">Показывать результаты вопросов:</span> {{ state.object.show_questions_results ? 'Да' : 'Нет' }}
              </div>

              <div class="detail-tab-elem">
                <span class="detail-tab-label">Показывать результаты ответов:</span> {{ state.object.show_answers_results ? 'Да' : 'Нет' }}
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
            
            
            <div v-if="activeTab === 'test_sections'" class="test-section-tab">
              
              <div v-if="state.canEditTest">
                
                <div v-if="state.object.test_sections && state.object.test_sections.length > 0" class="test-section-tab-flex">
                  
                  <div v-for="test_section in state.object.test_sections" :key="test_section.id" class="test-section-tab-item">

                    <div class="test-section-tab-item-top">

                      <div class="test-section-tab-item-title">
                        <h2>
                          {{ test_section.item ? test_section.item : 'Нет данных' }} - {{ test_section.name ? test_section.name : 'Нет имени' }}
                        </h2>
                      </div>

                    </div>

                    <div class="test-section-tab-item-detail">
                      
                      <div class="test-section-tab-item-detail-elem">
                        <span class="test-section-tab-item-detail-label">Размер выборки:</span> {{ test_section.sample_size ? test_section.sample_size : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="state.canViewTest" class="test-section-table_container">
                      <div v-if="test_section.test_section_questions && test_section.test_section_questions.length > 0" class="test-section-table-outer">
                        <div class="test-section-table-inner">
                          <table>
                            <thead>
                                <tr>
                                    <th>Порядок</th>
                                    <th>Вопрос</th>
                                    <th>
                                      Действия
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                              <tr v-for="test_section_question in test_section.test_section_questions" :key="test_section_question.id">

                                <td>{{ test_section_question.item ? test_section_question.item : '-' }}</td>
                                <td>{{ test_section_question.question.text ? test_section_question.question.text : '-' }}</td>

                                <td>
                                  <div v-if="state.canViewTest">
                                    <div class="test-section-menu">
                                      <router-link 
                                        v-if="state.canEditTest" 
                                        :to="{ name: 'TestSectionQuestionEdit', params: { id: test_section_question.id }, query: { testSectionId: test_section.id, testId: state.object.id } }"
                                        class="test-section-button"
                                      >
                                        Изменить
                                      </router-link>
                                      <button 
                                        v-if="state.canEditTest" 
                                        @click="openTestSectionQuestionDeleteModal(test_section_question)"
                                        class="test-section-button"
                                      >
                                        Удалить
                                      </button>
                            
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
                        <div class="none-border-mini">Нет вопросов теста</div>
                      </div>
                    </div>

                    <div  v-if="state.canViewTest" class="test-section-tab-item-menu-outer">
                      <div class="test-section-tab-item-menu-inner">
                            
                          <router-link
                            v-if="state.canEditTest"
                            :to="{ name: 'TestSectionQuestionCreate',  query: { testSectionId: test_section.id, testId: state.object.id } }"
                            class="test-section-button"
                          >
                            Создать
                          </router-link>

                          <router-link 
                            v-if="state.canEditTest" 
                            :to="{ name: 'TestSectionEdit', params: { id: test_section.id }, query: { testId: state.object.id }  }"
                            class="test-section-button"
                          >
                            Изменить
                          </router-link>
                          <button 
                            v-if="state.canEditTest" 
                            @click="openTestSectionDeleteModal(test_section)"
                            class="test-section-button"
                          >
                            Удалить
                          </button>
                         
                      </div>
                    </div>
                    <div v-else> 
                      -
                    </div>

                  </div>

                  <div v-if="showTestSectionDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedTestSection.str || 'Безымянная подзадача' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmTestSectionDelete(selectedTestSection.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeTestSectionDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div>

                  <div v-if="showTestSectionQuestionDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedTestSectionQuestion.str || 'Безымянная подзадача' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmTestSectionQuestionDelete(selectedTestSectionQuestion.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeTestSectionQuestionDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div>

                </div>
                
                <div v-else >
                  <div class="none-border">Нет разделов теста</div>
                </div>
              </div>

              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>

              <div v-if="state.canEditTest" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canEditTest"
                  :to="{ name: 'TestSectionCreate', query: { testId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'test'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'test'" />

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
  canViewTest: false,
  canSelfAssignment: false,
  canEditTest: false,
  canDeleteTest: false,
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
    const response = await axios.get(`${baseUrl}/tests/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные теста:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных теста:', error);
  }
};

const showTestDeleteModal = ref(false);
const openTestDeleteModal = () => {
  showTestDeleteModal.value = true;
};
const closeTestDeleteModal = () => {
  showTestDeleteModal.value = false;
};
const confirmTestDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/tests/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeTestDeleteModal();
    router.push({ name: 'TestList' });
  } catch (error) {
    console.error('Ошибка удаления теста:', error);
  }
};

const showTestSectionDeleteModal = ref(false);
const selectedTestSection = ref(null);
const openTestSectionDeleteModal = (test_section) => {
  selectedTestSection.value = test_section;
  showTestSectionDeleteModal.value = true;
};
const closeTestSectionDeleteModal = () => {
  showTestSectionDeleteModal.value = false;
};
const confirmTestSectionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/test_sections/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeTestSectionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления раздела теста:', error);
  }
};

const showTestSectionQuestionDeleteModal = ref(false);
const selectedTestSectionQuestion = ref(null);
const openTestSectionQuestionDeleteModal = (test_section_question) => {
  selectedTestSectionQuestion.value = test_section_question;
  showTestSectionQuestionDeleteModal.value = true;
};
const closeTestSectionQuestionDeleteModal = () => {
  showTestSectionQuestionDeleteModal.value = false;
};
const confirmTestSectionQuestionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/test_section_questions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeTestSectionQuestionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления вопроса раздела теста:', error);
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

    state.canViewTest = state.globalPermissionsList.includes('tests.view_test') ||
      (state.objectPermissionsDict['tests.view_test'] &&
      state.objectPermissionsDict['tests.view_test'].includes(Number(id)));
    console.log('Права на просмотр аккаунтов:', state.canViewTest);

    state.canSelfAssignment = state.canViewTest && state.object.self_assignment_task_template
    console.log('Права на самоназначение:', state.canSelfAssignment);

    state.canEditTest = state.globalPermissionsList.includes('tests.change_test') ||
      (Array.isArray(state.objectPermissionsDict['tests.change_test']) &&
      state.objectPermissionsDict['tests.change_test'].includes(Number(id)));
    console.log('Права на редактирование аккаунтов:', state.canEditTest);

    state.canDeleteTest = state.globalPermissionsList.includes('tests.delete_test') ||
      (Array.isArray(state.objectPermissionsDict['tests.delete_test']) &&
      state.objectPermissionsDict['tests.delete_test'].includes(Number(id)));
    console.log('Права на удаление аккаунтов:', state.canDeleteTest);

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
  { name: 'details', label: 'Детали' },
  state.canEditTest ? { name: 'test_sections', label: 'Раздел теста' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeTestTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeTestTab-${route.params.id}`, newTab);
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
