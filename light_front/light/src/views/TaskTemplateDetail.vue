<template>
  <div v-if="loading">
    <div v-if="state.canViewTaskTemplate" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянный шаблон задачи' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div v-if="state.object.is_child" class="detail-card-text-elem">
                <span class="detail-card-text-label">План:</span> {{ state.object.plan ? state.object.plan.name : 'Нет плана' }}
              </div>
              <div v-if="state.object.is_child" class="detail-card-text-elem">
                <span class="detail-card-text-label">Пункт:</span> {{ state.object.item|| 'Нет пункта' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип задачи:</span> {{ state.object.task_type_display || 'Нет типа задачи' }}
              </div>
              <div v-if="state.object.task_type == 'common_task'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Требуется проверка:</span> {{ state.object.require_review ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.task_type == 'material_review'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Материал:</span> {{ state.object.material.str || 'Нет материала' }}
              </div>
              <div v-if="state.object.task_type == 'course_study'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Курс:</span> {{ state.object.course.str || 'Нет курса' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Тест:</span> {{ state.object.test.str || 'Нет теста' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Мероприятие:</span> {{ state.object.event_template.str || 'Нет мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Слот мероприятия:</span> {{ state.object.event_slot?.str || 'Нет слота мероприятия' }}
              </div>
              <div v-if="state.object.is_child" class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип задержки:</span> {{ state.object.delay_type_display || 'Нет типа задержки' }}
              </div>
              <div v-if="state.object.is_child && state.object.delay_type != 'none'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Задержка:</span> {{ state.object.delay_value|| 'Нет задержки' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип срока:</span> {{ state.object.term_type_display || 'Нет типа срока' }}
              </div>
              <div v-if="state.object.term_type != 'none'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Срок:</span> {{ state.object.term_value|| 'Нет срока' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>
            <div class="manual">
              <div v-html="state.object.manual" class="tiptap close" :class="{ expanded: isExpanded }"></div>
              <div v-if="state.object.manual.length > 150" class="expand-container">
                <button class="expand-button" @click="isExpanded = !isExpanded">
                  {{ isExpanded ? 'Свернуть' : 'Развернуть' }}
                </button>
              </div>
            </div>
            <div class="detail-menu button-group">
              <router-link 
                v-if="state.canEditTaskTemplate" 
                :to="{ name: 'TaskTemplateEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteTaskTemplate" 
                @click="openTaskTemplateDeleteModal"
                class="button"
              >
                Удалить
              </button>
            </div>
            <div v-if="showTaskTemplateDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный задача' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmTaskTemplateDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeTaskTemplateDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Дочерняя:</span> {{ state.object.is_child ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.is_child" class="detail-tab-elem">
                <span class="detail-tab-label">План:</span> {{ state.object.plan ? state.object.plan.name : 'Нет плана' }}
              </div>
              <div v-if="state.object.is_child" class="detail-tab-elem">
                <span class="detail-tab-label">Пункт:</span> {{ state.object.item|| 'Нет пункта' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Тип задачи:</span> {{ state.object.task_type_display || 'Нет типа задачи' }}
              </div>
              <div v-if="state.object.task_type == 'common_task'" class="detail-tab-elem">
                <span class="detail-tab-label">Требуется проверка:</span> {{ state.object.require_review ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.task_type == 'material_review'" class="detail-tab-elem">
                <span class="detail-tab-label">Материал:</span> {{ state.object.material.str || 'Нет материала' }}
              </div>
              <div v-if="state.object.task_type == 'course_study'" class="detail-tab-elem">
                <span class="detail-tab-label">Курс:</span> {{ state.object.course.str || 'Нет курса' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-tab-elem">
                <span class="detail-tab-label">Тест:</span> {{ state.object.test.str || 'Нет теста' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-tab-elem">
                <span class="detail-tab-label">Мероприятие:</span> {{ state.object.event_template.str || 'Нет мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-tab-elem">
                <span class="detail-tab-label">Слот мероприятия:</span> {{ state.object.event_slot?.str || 'Нет слота мероприятия' }}
              </div>
              <div v-if="state.object.is_child" class="detail-tab-elem">
                <span class="detail-tab-label">Тип задержки:</span> {{ state.object.delay_type_display || 'Нет типа задержки' }}
              </div>
              <div v-if="state.object.is_child && state.object.delay_type != 'none'" class="detail-tab-elem">
                <span class="detail-tab-label">Задержка:</span> {{ state.object.delay_value|| 'Нет задержки' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Тип срока:</span> {{ state.object.term_type_display || 'Нет типа срока' }}
              </div>
              <div v-if="state.object.term_type != 'none'" class="detail-tab-elem">
                <span class="detail-tab-label">Срок:</span> {{ state.object.term_value || 'Нет срока' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Ожидает активации:</span> {{ state.object.waiting ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Итог задачи:</span> {{ state.object.task_outcome ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Самоназначение:</span> {{ state.object.self_assignment ? 'Да' : 'Нет' }}
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

            <div v-if="activeTab === 'child_tasks'" class="table-tab">
              <div v-if="state.canViewTaskTemplate">
                <div v-if="state.object.child_task_templates && state.object.child_task_templates.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Пункт</th>
                              <th>Тип задачи</th>
                              <th>Название</th>
                              <th>Тип задежки</th>
                              <th>Задержка</th>
                              <th>Тип срока</th>
                              <th>Срок</th>
                              <th>Исполнитель</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="task_template in state.object.child_task_templates" :key="task_template.id">
                          <td>{{ task_template.item ? task_template.item : '-' }}</td>
                          <td>{{ task_template.task_type_display ? task_template.task_type_display : '-' }}</td>
                          <td>{{ task_template.name ? task_template.name : '-' }}</td>
                          <td>{{ task_template.delay_type_display ? task_template.delay_type_display : '-' }}</td>
                          <td>{{ task_template.delay_value ? task_template.delay_value : '-' }}</td>
                          <td>{{ task_template.term_type_display ? task_template.term_type_display : '-' }}</td>
                          <td>{{ task_template.term_value ? task_template.term_value : '-' }}</td>
                          <td>{{ task_template.executor ? task_template.executor.str : 'Нет данных' }}</td>
                          <td>
                            <div v-if="state.canViewTaskTemplateGlobal || state.canViewTaskTemplateIds.includes(task_template.id)">
                              <div class="table-tab-menu">
                                <router-link  
                                  :to="{ name: 'TaskTemplateDetail', params: { id: task_template.id } }"
                                  class="table-tab-button"
                                >
                                  Открыть
                                </router-link>
                                <router-link 
                                  v-if="state.canEditTaskTemplateGlobal || state.canEditTaskTemplateIds.includes(task_template.id)" 
                                  :to="{ name: 'TaskTemplateEdit', params: { id: task_template.id }, query: { planId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeleteTaskTemplateGlobal || state.canDeleteTaskTemplateIds.includes(task_template.id)" 
                                  @click="openChildTaskTemplateDeleteModal(task_template)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showChildTaskTemplateDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedChildTaskTemplate.str || 'Безымянная подзадача' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmChildTaskTemplateDelete(selectedChildTaskTemplate.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeChildTaskTemplateDeleteModal" class="minibutton">Отменить</button>
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
                  <div class="none-border">Нет подзадач</div>
                </div>
              </div>

              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>

              <div v-if="state.canAddTaskTemplate" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddTaskTemplate"
                  :to="{ name: 'TaskTemplateCreate', query: { planId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'control_elements'" class="table-tab">
              <div v-if="state.canViewTaskTemplate">
                <div v-if="state.object.control_elements && state.object.control_elements.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Название</th>
                              <th>Описание</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="control_element in state.object.control_elements" :key="control_element.id">

                          <td>{{ control_element.name ? control_element.name : '-' }}</td>
                          <td>{{ control_element.desc ? control_element.desc : '-' }}</td>

                          <td>
                            <div v-if="state.canViewControlElementsGlobal || state.canViewControlElementsIds.includes(task_template.id)">
                              <div class="table-tab-menu">
                                <router-link 
                                  v-if="state.canViewControlElementsIds.includes(control_element.id)" 
                                  :to="{ name: 'ControlElementDetail', params: { id: control_element.id } }"
                                  class="table-tab-button"
                                >
                                  Открыть
                                </router-link>
                                <router-link 
                                  v-if="state.canEditControlElementsGlobal || state.canEditControlElementsIds.includes(task_template.id)" 
                                  :to="{ name: 'ControlElementEdit', params: { id: control_element.id }, query: { taskId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeleteControlElementsGlobal || state.canDeleteControlElementsIds.includes(task_template.id)" 
                                  @click="openControlElementsDeleteModal(control_element)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>
                                <div v-if="showControlElementsDeleteModal" class="modal-overlay">
                                  <div class="modal">
                                    <div class="modal-header">
                                      <h2 class="modal-header-h2">Удаление {{ selectedControlElements.str || 'Безымянная подзадача' }}</h2>
                                    </div>
                                    <div class="minibutton-group modal-menu">
                                      <button @click="confirmControlElementsDelete(selectedControlElements.id)" class="minibutton">Подтвердить</button>
                                      <button @click="closeControlElementsDeleteModal" class="minibutton">Отменить</button>
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
                  <div class="none-border">Нет итогов задач</div>
                </div>
              </div>

              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>

              <div v-if="state.canAddControlElements" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddControlElements"
                  :to="{ name: 'ControlElementCreate', query: { taskId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'tasktemplate'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'tasktemplate'" />

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
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue';
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
  canAddTaskTemplate: false,
  canViewTaskTemplate: false,
  canViewTaskTemplateGlobal: false,
  canViewTaskTemplateIds: [],
  canEditTaskTemplate: false,
  canEditTaskTemplateGlobal: false,
  canEditTaskTemplateIds: [],
  canDeleteTaskTemplate: false,
  canDeleteTaskTemplateGlobal: false,
  canDeleteTaskTemplateIds: [],
  canViewControlElementsGlobal: false,
  canViewControlElementsIds: [],
  canEditControlElementsGlobal: false,
  canEditControlElementsIds: [],
  canDeleteControlElementsGlobal: false,
  canDeleteControlElementsIds: [],
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
});

const isExpanded = ref(false);

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
    const response = await axios.get(`${baseUrl}/task_templates/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные шаблона задачи:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных шаблона задачи:', error);
  }
};

const showTaskTemplateDeleteModal = ref(false);
const openTaskTemplateDeleteModal = () => {
  showTaskTemplateDeleteModal.value = true;
};
const closeTaskTemplateDeleteModal = () => {
  showTaskTemplateDeleteModal.value = false;
};
const confirmTaskTemplateDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/task_templates/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeTaskTemplateDeleteModal();
    router.push({ name: 'TaskTemplateList' });
  } catch (error) {
    console.error('Ошибка удаления шаблона задачи:', error);
  }
};

const showChildTaskTemplateDeleteModal = ref(false);
const selectedChildTaskTemplate = ref(null);
const openChildTaskTemplateDeleteModal = (task_template) => {
  selectedChildTaskTemplate.value = task_template;
  showChildTaskTemplateDeleteModal.value = true;
};
const closeChildTaskTemplateDeleteModal = () => {
  showChildTaskTemplateDeleteModal.value = false;
};
const confirmChildTaskTemplateDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/task_templates/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeChildTaskTemplateDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const showControlElementsDeleteModal = ref(false);
const selectedControlElements = ref(null);
const openControlElementsDeleteModal = (control_element) => {
  selectedControlElements.value = control_element;
  showControlElementsDeleteModal.value = true;
};
const closeControlElementsDeleteModal = () => {
  showControlElementsDeleteModal.value = false;
};
const confirmControlElementsDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/control_elements/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeControlElementsDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
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

    state.canAddTaskTemplate = state.globalPermissionsList.includes('bpms.add_task_template');
    console.log('Права на добавление шаблонов задач:', state.canAddTaskTemplate);

    state.canViewTaskTemplate = state.globalPermissionsList.includes('bpms.view_task_template') ||
      (state.objectPermissionsDict['bpms.view_task_template'] &&
      state.objectPermissionsDict['bpms.view_task_template'].includes(Number(id)));
    console.log('Права на просмотр шаблона задач:', state.canViewTaskTemplate);

    state.canViewTaskTemplateGlobal = state.globalPermissionsList.includes('bpms.view_task_template');
    console.log('Глобальные права на просмотр шаблона задач:', state.canViewTaskTemplateGlobal);

    state.canViewTaskTemplateIds = (state.objectPermissionsDict['bpms.view_task_template'] || []).map(Number);
    if (!state.canViewTaskTemplateGlobal) {
    state.object.child_task_templates = state.object.child_task_templates.filter(child_task_template => state.canViewTaskTemplateIds.includes(child_task_template.id));
    }

    console.log('Доступные шаблоны задач:', state.object.child_task_templates);

    state.canEditTaskTemplate = state.globalPermissionsList.includes('bpms.change_task_template') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_task_template']) &&
      state.objectPermissionsDict['bpms.change_task_template'].includes(Number(id)));
    console.log('Права на редактирование шаблона задач:', state.canEditTaskTemplate);

    state.canEditTaskTemplateGlobal = state.globalPermissionsList.includes('bpms.change_task_template');
    console.log('Глобальные права на редактирование шаблона задач:', state.canEditTaskTemplateGlobal);

    state.canEditTaskTemplateIds = (state.objectPermissionsDict['bpms.change_task_template'] || []).map(Number);
    console.log('Доступные для изменения шаблоны задач:', state.canEditTaskTemplateIds);

    state.canDeleteTaskTemplate = state.globalPermissionsList.includes('bpms.delete_task_template') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_task_template']) &&
      state.objectPermissionsDict['bpms.delete_task_template'].includes(Number(id)));
    console.log('Права на удаление шаблонов задач:', state.canDeleteTaskTemplate);

    state.canDeleteTaskTemplateGlobal = state.globalPermissionsList.includes('bpms.delete_task_template');
    console.log('Глобальные права на удаление шаблонов задач:', state.canDeleteTaskTemplateGlobal);

    state.canDeleteTaskTemplateIds = (state.objectPermissionsDict['bpms.delete_task_template'] || []).map(Number);
    console.log('Доступные для удаления шаблоны задач:', state.canDeleteTaskTemplateIds);

    state.canAddControlElements = state.globalPermissionsList.includes('bpms.add_control_element');
    console.log('Права на добавление итогов задач:', state.canAddControlElements);

    state.canViewControlElementsGlobal = state.globalPermissionsList.includes('bpms.view_control_element');
    console.log('Глобальные права на просмотр итога задач:', state.canViewControlElementsGlobal);

    state.canViewControlElementsIds = (state.objectPermissionsDict['bpms.view_control_element'] || []).map(Number);
    if (!state.canViewControlElementsGlobal) {
        state.object.control_elements = state.object.control_elements.filter(control_element => state.canViewControlElementsIds.includes(control_element.id));
    }
    console.log('Доступные итоги задач:', state.object.control_elements);

    state.canEditControlElementsGlobal = state.globalPermissionsList.includes('bpms.change_control_element');
    console.log('Глобальные права на редактирование итога задач:', state.canEditControlElementsGlobal);

    state.canEditControlElementsIds = (state.objectPermissionsDict['bpms.change_control_element'] || []).map(Number);
    console.log('Доступные для изменения итогы задач:', state.canEditControlElementsIds);

    state.canDeleteControlElementsGlobal = state.globalPermissionsList.includes('bpms.delete_control_element');
    console.log('Глобальные права на удаление итогов задач:', state.canDeleteControlElementsGlobal);

    state.canDeleteControlElementsIds = (state.objectPermissionsDict['bpms.delete_control_element'] || []).map(Number);
    console.log('Доступные для удаления итогы задач:', state.canDeleteControlElementsIds);

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
  state.object.task_outcome ? { name: 'control_elements', label: 'Итоги задачи' } : null,
  state.object.task_type == 'plan_implementation' ? { name: 'child_tasks', label: 'Подзадачи' } : null,
  { name: 'details', label: 'Детали' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeTaskTemplateTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeTaskTemplateTab-${route.params.id}`, newTab);
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
