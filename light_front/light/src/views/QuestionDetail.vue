<template>
  <div v-if="loading">
    <div v-if="state.canViewQuestion" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-image-outer">
            <div v-if="state.object.picture" class="detail-card-image-inner">
              <img :src="state.object.picture || '/default-avatar.png'" alt="Картинка" />
            </div>
            <div v-else class="detail-card-image-none">
              <span class="none-text">Нет аватара</span>
            </div>
          </div>
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.text || 'Вопрос без текста' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип вопроса:</span> {{ state.object.question_type_display || 'Нет типа вопроса' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Инструкция:</span> {{ state.object.manual || 'Нет инструкции' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Балл:</span> {{ state.object.score != undefined ? state.object.score : 'Нет баллов' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories?.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="detail-menu button-group">
              <router-link 
                v-if="state.canEditQuestion" 
                :to="{ name: 'QuestionEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteQuestion" 
                @click="openQuestionDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showQuestionDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.username || 'Безымянная учетная запись' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmQuestionDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeQuestionDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Тип вопроса:</span> {{ state.object.question_type_display || 'Нет типа вопроса' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Инструкция:</span> {{ state.object.manual || 'Нет инструкции' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Балл:</span> {{ state.object.score != undefined ? state.object.score : 'Нет баллов' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Обратная связь при правильном ответе:</span> {{ state.object.feedback_for_correct || 'Нет обратной связи при правильном ответе' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Обратная связь при неправильном ответе:</span> {{ state.object.feedback_for_incorrect || 'Нет обратной связи при правильном ответе' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories?.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
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

            <div v-if="activeTab === 'answers'" class="table-tab">
              <div v-if="state.canEditQuestion">
                <div v-if="state.object.answers && state.object.answers.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Порядок</th>
                              <th>Текст</th>
                              <th>Картинка</th>
                              <th v-if="state.object.question_type == 'single_selection' || state.object.question_type == 'multiple_choice'">
                                Правильный ответ
                              </th>
                              <th v-else-if="state.object.question_type == 'sorting'">
                                Правильный порядок
                              </th>
                              <th v-else-if="state.object.question_type == 'text_input'">
                                Правильный текст
                              </th>
                              <th v-else-if="state.object.question_type == 'numeric_input'">
                                Правильное число
                              </th>
                              <th v-else-if="state.object.question_type == 'compliance'">
                                Соотвествующий пункт
                              </th>

                              <th>Балл</th>
                              <th>Обратная связь при правильном ответе</th>
                              <th>Обратная связь при неправильном ответе</th>

                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="answer in state.object.answers" :key="answer.id">
                          <td>{{ answer.item ? answer.item : 'Нет данных' }}</td>
                          <td>{{ answer.text ? answer.text : 'Нет данных' }}</td>
                          <td>
                            <a v-if="answer.picture" class="table-tab-button" :href="coreUrl + answer.picture" target="_blank" rel="noopener noreferrer">
                              Открыть
                            </a>
                            <span v-else>Нет</span>
                          </td>

                          <td v-if="state.object.question_type == 'single_selection' || state.object.question_type == 'multiple_choice'">{{ answer.correct_answer ? 'Да' : 'Нет' }}</td>
                          <td v-else-if="state.object.question_type == 'sorting'">{{ answer.correct_item ? answer.correct_item : 'Нет данных' }}</td>
                          <td v-else-if="state.object.question_type == 'text_input'">{{ answer.correct_text_input ? answer.correct_text_input : 'Нет данных' }}</td>
                          <td v-else-if="state.object.question_type == 'numeric_input'">{{ answer.correct_numeric_input ? answer.correct_numeric_input : 'Нет данных' }}</td>
                          <td v-else-if="state.object.question_type == 'compliance'">
                            {{ answer.relevant_point.text  ? answer.relevant_point.text : '' }}
                            <router-link
                              v-if="state.canDeleteQuestion && !answer.relevant_point.text"
                              :to="{ name: 'RelevantPointCreate', query: { answerId: answer.id, questionId: state.object.id } }"
                              class="table-tab-button table-tab-button-margin-left"
                            >
                              Создать
                            </router-link>
                            <router-link
                              v-if="state.canDeleteQuestion && answer.relevant_point.text"
                              :to="{ name: 'RelevantPointEdit', params: { id: answer.relevant_point.id }, query: { answerId: answer.id, questionId: state.object.id } }"
                              class="table-tab-button table-tab-button-margin-left"
                            >
                              Изменить
                            </router-link>
                          </td>


                          <td>{{ answer.score != undefined ? answer.score : 'Нет данных' }}</td>
                          <td>{{ answer.feedback_for_correct ? answer.feedback_for_correct : 'Нет данных' }}</td>
                          <td>{{ answer.feedback_for_incorrect ? answer.feedback_for_incorrect : 'Нет данных' }}</td>

                          <td>
                            <div v-if="state.canEditQuestion || state.canDeleteQuestion">
                              <div class="table-tab-menu">
                                <router-link 
                                  v-if="state.canEditQuestion" 
                                  :to="{ name: 'AnswerEdit', params: { id: answer.id }, query: { questionId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeleteQuestion" 
                                  @click="openAnswerDeleteModal(answer)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showAnswerDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedAnswer.text || 'Пустой вопрос' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmAnswerDelete(selectedAnswer.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeAnswerDeleteModal" class="minibutton">Отменить</button>
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
                  <div class="none-border">Нет ответов</div>
                </div>
              </div>
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
              <div v-if="state.canEditQuestion" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canEditQuestion"
                  :to="{ name: 'AnswerCreate', query: { questionId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'question'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'question'" />

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
import { formatDate, formatDateTime, baseUrl, coreUrl, isTokenValid , goBackSmart } from '../utils/utils'; 
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 


const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewQuestion: false,
  canEditQuestion: false,
  canDeleteQuestion: false,
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
    const response = await axios.get(`${baseUrl}/questions/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные вопроса:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных вопроса:', error);
  }
};

const showQuestionDeleteModal = ref(false);
const openQuestionDeleteModal = () => {
  showQuestionDeleteModal.value = true;
};
const closeQuestionDeleteModal = () => {
  showQuestionDeleteModal.value = false;
};
const confirmQuestionDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/questions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeQuestionDeleteModal();
    router.push({ name: 'QuestionList' });
  } catch (error) {
    console.error('Ошибка удаления вопроса:', error);
  }
};

const showAnswerDeleteModal = ref(false);
const selectedAnswer = ref(null);
const openAnswerDeleteModal = (answer) => {
  selectedAnswer.value = answer;
  showAnswerDeleteModal.value = true;
};
const closeAnswerDeleteModal = () => {
  showAnswerDeleteModal.value = false;
};
const confirmAnswerDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/answers/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeAnswerDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
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

    state.canViewQuestion = state.globalPermissionsList.includes('tests.view_question') ||
      (state.objectPermissionsDict['tests.view_question'] &&
      state.objectPermissionsDict['tests.view_question'].includes(Number(id)));
    console.log('Права на просмотр вопросов:', state.canViewQuestion);

    state.canEditQuestion = state.globalPermissionsList.includes('tests.change_question') ||
      (Array.isArray(state.objectPermissionsDict['tests.change_question']) &&
      state.objectPermissionsDict['tests.change_question'].includes(Number(id)));
    console.log('Права на редактирование вопросов:', state.canEditQuestion);

    state.canDeleteQuestion = state.globalPermissionsList.includes('tests.delete_question') ||
      (Array.isArray(state.objectPermissionsDict['tests.delete_question']) &&
      state.objectPermissionsDict['tests.delete_question'].includes(Number(id)));
    console.log('Права на удаление вопросов:', state.canDeleteQuestion);

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
  state.canEditQuestion ? { name: 'answers', label: 'Ответы' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeQuestionTab-${route.params.id}`) || 'details');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeQuestionTab-${route.params.id}`, newTab);
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
