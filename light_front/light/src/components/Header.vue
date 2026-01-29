<template>
  <!-- Шапка компонента -->

  <header class="header-outer">

    <div class="header-inner">
  
      <div class="header-submenu headerbutton-group">

        <button class="headerbutton" 
          @click="toggleMenu" 
          title="Меню"
          type="button">
          <i class="fa-solid fa-bars"></i>
        </button>

      </div>

      <div class="header-submenu headerbutton-group">

        <button class="headerbutton"
          v-if="auth_user_id"
          @click="openNotificationsModal()" 
          title="Открыть уведомления"
          type="button">
          <i class="fa-solid fa-bell"></i>
        </button>

        <router-link :to="{ name: 'Cabinet' }"
          v-if="auth_user_id" 
          class="headerbutton"
          title="Кабинет">
          <i class="fa-solid fa-circle-user"></i>
        </router-link>

        <router-link :to="{ name: 'Login' }" 
          v-if="!auth_user_id" 
          class="headerbutton"
          title="Вход">
          <i class="fa-solid fa-door-open"></i>
        </router-link>

      </div>

    </div>

  </header>

  <!-- Контейнер навигационного меню с затемнением фона при открытии -->
  <nav v-if="isVisible" class="header-overlay" @click="toggleMenu">
    <!-- Контейнер для навигационных ссылок -->
    <div class="header-menu-inner" @click.stop>
      
      <div class="header-menu-close_button-inner">
        <button @click="toggleMenu" class="header-close_button">
          ×
        </button>
      </div>

      <div v-if="state.canViewPlaning" class="header-menu_title">
        <i class="fa-solid fa-calendar"></i>
        Планирование
      </div>

      <router-link :to="{ name: 'InteractionList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewInteraction">
        <div class="header-menu_link-items-inner">
          <div>
            Взаимодействия
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TaskTemplateList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTaskTemplate">
        <div class="header-menu_link-items-inner">
          <div>
            Шаблоны задач
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TaskList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTask">
        <div class="header-menu_link-items-inner">
          <div>
            Задачи
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TaskTemplateAssignmentList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTaskTemplateAssignment">
        <div class="header-menu_link-items-inner">
          <div>
            Назначение шаблона задачи
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'QueueList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewQueue">
        <div class="header-menu_link-items-inner">
          <div>
            Очереди
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'ControlElementList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewControlElement">
        <div class="header-menu_link-items-inner">
          <div>
            Управляющий элемент
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TaskAnalytics' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTaskAnalytics">
        <div class="header-menu_link-items-inner">
          <div>
            Аналитика
          </div>
        </div>
      </router-link>

      <div v-if="state.canViewContent"  class="header-menu_title">
        <i class="fa-solid fa-photo-film"></i>
        Контент
      </div>

      <router-link :to="{ name: 'PublicPlanList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewPublicPlan">
        <div class="header-menu_link-items-inner">
          <div>
            Планы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'PublicTaskList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewPublicTask">
        <div class="header-menu_link-items-inner">
          <div>
            Задания
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'FileList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewFile">
        <div class="header-menu_link-items-inner">
          <div>
            Файлы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'NewList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewNew">
        <div class="header-menu_link-items-inner">
          <div>
            Новости
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'MaterialList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewMaterial">
        <div class="header-menu_link-items-inner">
          <div>
            Материалы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'CourseList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewCourse">
        <div class="header-menu_link-items-inner">
          <div>
            Курсы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TestList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTest">
        <div class="header-menu_link-items-inner">
          <div>
            Тесты
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'QuestionList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewQuestion">
        <div class="header-menu_link-items-inner">
          <div>
            Вопросы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'EventTemplateList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewEventTemplate">
        <div class="header-menu_link-items-inner">
          <div>
            Мероприятия
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'EventSlotList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewEventSlot">
        <div class="header-menu_link-items-inner">
          <div>
             Слоты
          </div>
        </div>
      </router-link>

      <div v-if="state.canViewTalking" class="header-menu_title">
        <i class="fa-solid fa-comment"></i>
        Общение
      </div>

      <router-link :to="{ name: 'ChatList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewChat">
        <div class="header-menu_link-items-inner">
          <div>
            Чаты
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'TopicList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewTopic">
        <div class="header-menu_link-items-inner">
          <div>
            Топики
          </div>
        </div>
      </router-link>

      <div v-if="state.canViewUsers" class="header-menu_title">
        <i class="fa-solid fa-users"></i>
        Пользователи
      </div>

      <router-link :to="{ name: 'ClientList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewClient">
        <div class="header-menu_link-items-inner">
          <div>
            Клиенты
          </div>
        </div>
      </router-link>
      
      <router-link :to="{ name: 'AccountList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewAccount">
        <div class="header-menu_link-items-inner">
          <div>
            Аккаунты
          </div>
        </div>
      </router-link>
      
      <router-link :to="{ name: 'AccountGroupList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewAccountGroup">
        <div class="header-menu_link-items-inner">
          <div>
            Группы
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'OrganizationList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewSubdivision">
        <div class="header-menu_link-items-inner">
          <div>
            Организации
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'SubdivisionList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewSubdivision">
        <div class="header-menu_link-items-inner">
          <div>
            Подразделения
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'PositionList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewPosition">
        <div class="header-menu_link-items-inner">
          <div>
            Должности
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'AccountPermissionList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewAccountPermission">
        <div class="header-menu_link-items-inner">
          <div>
             Права пользователей
          </div>
        </div>
      </router-link>

      <div v-if="state.canViewSettings" class="header-menu_title">
        <i class="fa-solid fa-gear"></i>
        Настройки
      </div>

      <router-link :to="{ name: 'HomePage' }" 
        @click="toggleMenu" 
        class="header-menu_link">
        <div class="header-menu_link-items-inner">
          <div>
            Главная страница
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'CategoryList' }" 
        @click="toggleMenu" 
        class="header-menu_link"
        v-if="state.canViewCategory">
        <div class="header-menu_link-items-inner">
          <div>
            Категории
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'LegalPage' }" 
        @click="toggleMenu" 
        class="header-menu_link">
        <div class="header-menu_link-items-inner">
          <div>
            Пользовательское соглашение
          </div>
        </div>
      </router-link>

      <router-link :to="{ name: 'PolicyPage' }" 
        @click="toggleMenu" 
        class="header-menu_link">
        <div class="header-menu_link-items-inner">
          <div>
            Политика конфиденциальности
          </div>
        </div>
      </router-link>
      
    </div>
  </nav>

  <!-- Контейнер навигационного меню с затемнением фона при открытии -->
  <nav v-if="showNotificationsModal" class="header-overlay" @click="closeNotificationsModal">
    <!-- Контейнер для навигационных ссылок -->
    <div class="header-list-outer" @click.stop>
      
      <div class="header-list-close_button-inner">
        <button @click="closeNotificationsModal" class="header-close_button">
          ×
        </button>
      </div>
    
      <div v-if="auth_user_id" class="header-list-inner">

        <div v-if="notifications?.length > 0" class="header-list-search-field">
          <input 
            v-model="notificationsSearchQuery" 
            type="text" 
            placeholder="Поиск"
            class="header-search-input"
          />
        </div>

        <div v-if="paginatedNotifications && paginatedNotifications.length > 0" class="header-list-flex">
          
          <div v-for="notification in paginatedNotifications" :key="notification.id" class="header-list-item">

            <div class="header-list-item-header">
              <div class="header-list-item-title">
                <h2>
                  {{ notification.task ? notification.task.name  : 'Нет данных о задаче' }}
                </h2>
              </div>

            </div>

            <div class="header-list-item-text">
              <div class="header-list-item-text-elem"><span class="header-list-item-text-label">Тип оповещения:</span> {{ notification.notification_type_display || 'Нет типа напоминания' }}</div>
              <div class="header-list-item-text-elem"><span class="header-list-item-text-label">Создано:</span> {{ notification.created ? formatDateTime(notification.created) : 'Нет данных о создании' }}</div>
            </div>

            <div class="header-list-item-menu minibutton-group">

              <router-link  
                :to="{ name: 'TaskDetail', params: { id: notification.task.id } }"
                class="minibutton"
                @click="closeNotificationsModal"
              >
                Открыть
              </router-link>

              <button
                v-if="!notification.read"
                @click="notificationRead(notification.id)"
                class="minibutton"
              >
                Ознакомление
              </button>
                        
            </div>

          </div>

          <div class="list-pagination">
            <button 
              :disabled="notificationsCurrentPage === 1" 
              @click="notificationsCurrentPage--"
              class="list-settings-button"
            >
              Назад
            </button>
            <span>Страница {{ notificationsCurrentPage }} из {{ notificationsTotalPages }}</span>
            <button 
              :disabled="notificationsCurrentPage === notificationsTotalPages" 
              @click="notificationsCurrentPage++"
              class="list-settings-button"
            >
              Вперед
            </button>
          </div>

        </div>

        <div v-else class="none-card">
          <div>Список пуст</div>
        </div>
        
      </div>

      <div v-else class="loading">
        <div>Пользователь не авторизован</div>
      </div>

    </div>
  </nav>

</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid, auth_user_id, setUserId, clearUserId } from '../utils/utils'; 
const route = useRoute();
const router = useRouter();
import '@fortawesome/fontawesome-free/css/all.css';

const state = reactive({
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewInteraction: false,
  canViewTaskTemplate: false,
  canViewTask: false,
  canViewTaskTemplateAssignment: false,
  canViewQueue: false,
  canViewControlElement: false,
  canViewTaskAnalytics: false,
  canViewPlaning: false,
  canViewPublicTask: false,
  canViewPublicPlan: false,
  canViewFile: false,
  canViewNew: false,
  canViewMaterial: false,
  canViewCourse: false,
  canViewTest: false,
  canViewQuestion: false,
  canViewEventTemplate: false,
  canViewEventSlot: false,
  canViewContent: false,
  canViewChat: false,
  canViewTopic: false,
  canViewTalking: false,
  canViewClient: false,
  canViewAccount: false,
  canViewAccountGroup: false,
  canViewOrganization: false,
  canViewSubdivision: false,
  canViewPosition: false,
  canViewAccountPermission: false,
  canViewUsers: false,
  canViewCategory: false,
  canViewSettings: false,
});


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

    state.canViewInteraction = state.globalPermissionsList.includes('bpms.view_interaction') ||
      (state.objectPermissionsDict['bpms.view_interaction'] &&
      state.objectPermissionsDict['bpms.view_interaction']?.length > 0);
    console.log('Права на просмотр взаимодействий:', state.canViewInteraction);

    state.canViewTaskTemplate = state.globalPermissionsList.includes('bpms.view_task_template') ||
      (state.objectPermissionsDict['bpms.view_task_template'] &&
      state.objectPermissionsDict['bpms.view_task_template']?.length > 0);
    console.log('Права на просмотр шаблона задач:', state.canViewTaskTemplate);

    state.canViewTask = state.globalPermissionsList.includes('bpms.view_task') ||
      (state.objectPermissionsDict['bpms.view_task'] &&
      state.objectPermissionsDict['bpms.view_task']?.length > 0);
    console.log('Права на просмотр задачи:', state.canViewTask);

    state.canViewTaskTemplateAssignment = state.globalPermissionsList.includes('bpms.view_task_template_assignment') ||
      (state.objectPermissionsDict['bpms.view_task_template_assignment'] &&
      state.objectPermissionsDict['bpms.view_task_template_assignment']?.length > 0);
    console.log('Права на просмотр назначений задач:', state.canViewTaskTemplateAssignment);

    state.canViewQueue = state.globalPermissionsList.includes('bpms.view_queue') ||
      (state.objectPermissionsDict['bpms.view_queue'] &&
      state.objectPermissionsDict['bpms.view_queue']?.length > 0);
    console.log('Права на просмотр очередей:', state.canViewQueue);

    state.canViewControlElement = state.globalPermissionsList.includes('bpms.view_control_element') ||
      (state.objectPermissionsDict['bpms.view_control_element'] &&
      state.objectPermissionsDict['bpms.view_control_element']?.length > 0);
    console.log('Права на просмотр управляющих элементов:', state.canViewControlElement);

    state.canViewTaskAnalytics = state.globalPermissionsList.includes('bpms.view_analytics') ||
      (state.objectPermissionsDict['bpms.view_analytics'] &&
      state.objectPermissionsDict['bpms.view_analytics']?.length > 0);
    console.log('Права на просмотр аналитики по задачам:', state.canViewTaskAnalytics);

    state.canViewPlaning = (
      state.canViewInteraction ||
      state.canViewTaskTemplate || 
      state.canViewTask ||
      state.canViewTaskTemplateAssignment ||
      state.canViewQueue ||
      state.canViewControlElement ||
      state.canViewTaskAnalytics
    )
    console.log('Права на просмотр планирования:', state.canViewPlaning);
    
    state.canViewPublicPlan = state.globalPermissionsList.includes('bpms.view_public_plan') ||
      (state.objectPermissionsDict['bpms.view_public_plan'] &&
      state.objectPermissionsDict['bpms.view_public_plan']?.length > 0);
    console.log('Права на просмотр планов:', state.canViewPublicPlan)

    state.canViewPublicTask = state.globalPermissionsList.includes('bpms.view_public_task') ||
      (state.objectPermissionsDict['bpms.view_public_task'] &&
      state.objectPermissionsDict['bpms.view_public_task']?.length > 0);
    console.log('Права на просмотр заданий:', state.canViewPublicTask);

    state.canViewFile = state.globalPermissionsList.includes('files.view_file') ||
      (state.objectPermissionsDict['files.view_file'] &&
      state.objectPermissionsDict['files.view_file']?.length > 0);
    console.log('Права на просмотр файлов:', state.canViewFile);

    state.canViewNew = state.globalPermissionsList.includes('news.view_new') ||
      (state.objectPermissionsDict['news.view_new'] &&
      state.objectPermissionsDict['news.view_new']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewNew);

    state.canViewMaterial = state.globalPermissionsList.includes('materials.view_material') ||
      (state.objectPermissionsDict['materials.view_material'] &&
      state.objectPermissionsDict['materials.view_material']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewMaterial);

    state.canViewCourse = state.globalPermissionsList.includes('courses.view_course') ||
      (state.objectPermissionsDict['courses.view_course'] &&
      state.objectPermissionsDict['courses.view_course']?.length > 0);
    console.log('Права на просмотр курсов:', state.canViewCourse);

    state.canViewTest = state.globalPermissionsList.includes('tests.view_test') ||
      (state.objectPermissionsDict['tests.view_test'] &&
      state.objectPermissionsDict['tests.view_test']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewTest);

    state.canViewQuestion = state.globalPermissionsList.includes('tests.view_question') ||
      (state.objectPermissionsDict['tests.view_question'] &&
      state.objectPermissionsDict['tests.view_question']?.length > 0);
    console.log('Права на просмотр вопросов:', state.canViewQuestion);

    state.canViewEventTemplate = state.globalPermissionsList.includes('events.view_event_template') ||
      (state.objectPermissionsDict['events.view_event_template'] &&
      state.objectPermissionsDict['events.view_event_template']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewEventTemplate);

    state.canViewEventSlot = state.globalPermissionsList.includes('events.view_event_slot') ||
      (state.objectPermissionsDict['events.view_event_slot'] &&
      state.objectPermissionsDict['events.view_event_slot']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewEventSlot);

    state.canViewContent = (
      state.canViewPublicPlan || 
      state.canViewPublicTask || 
      state.canViewNew || 
      state.canViewMaterial ||
      state.canViewCourse ||
      state.canViewTest ||
      state.canViewEventTemplate ||
      state.canViewEventSlot
    )
    console.log('Права на просмотр контента:', state.canViewContent);

    state.canViewChat = state.globalPermissionsList.includes('chats.view_chat') ||
      (state.objectPermissionsDict['chats.view_chat'] &&
      state.objectPermissionsDict['chats.view_chat']?.length > 0);
    console.log('Права на просмотр чата:', state.canViewChat);

    state.canViewTopic = state.globalPermissionsList.includes('comments.view_topic') ||
      (state.objectPermissionsDict['comments.view_topic'] &&
      state.objectPermissionsDict['comments.view_topic']?.length > 0);
    console.log('Права на просмотр топика:', state.canViewTopic);

    state.canViewTalking = (
      state.canViewChat || 
      state.canViewTopic
    )
    console.log('Права на просмотр общения:', state.canViewTalking);

    state.canViewClient = state.globalPermissionsList.includes('core.view_client') ||
      (state.objectPermissionsDict['core.view_client'] &&
      state.objectPermissionsDict['core.view_client']?.length > 0);
    console.log('Права на просмотр клиент:', state.canViewClient);

    state.canViewAccount = state.globalPermissionsList.includes('core.view_account') ||
      (state.objectPermissionsDict['core.view_account'] &&
      state.objectPermissionsDict['core.view_account']?.length > 0);
    console.log('Права на просмотр аккаунтов:', state.canViewAccount);

    state.canViewAccountGroup = state.globalPermissionsList.includes('core.view_accounts_group') ||
      (state.objectPermissionsDict['core.view_accounts_group'] &&
      state.objectPermissionsDict['core.view_accounts_group']?.length > 0);
    console.log('Права на просмотр групп:', state.canViewAccountGroup);

    state.canViewOrganization = state.globalPermissionsList.includes('core.view_organization') ||
      (state.objectPermissionsDict['core.view_organization'] &&
      state.objectPermissionsDict['core.view_organization']?.length > 0);
    console.log('Права на просмотр организаций:', state.canViewOrganization);

    state.canViewSubdivision = state.globalPermissionsList.includes('core.view_subdivision') ||
      (state.objectPermissionsDict['core.view_subdivision'] &&
      state.objectPermissionsDict['core.view_subdivision']?.length > 0);
    console.log('Права на просмотр подразделений:', state.canViewSubdivision);

    state.canViewPosition = state.globalPermissionsList.includes('core.view_position') ||
      (state.objectPermissionsDict['core.view_position'] &&
      state.objectPermissionsDict['core.view_position']?.length > 0);
    console.log('Права на просмотр должностей:', state.canViewPosition);

    state.canViewAccountPermission = state.globalPermissionsList.includes('auth.view_permission') || !!state.objectPermissionsDict['auth.view_permission'];
    console.log('Права на просмотр прав:', state.canViewAccountPermission);

    state.canViewUsers = (
      state.canViewClient ||
      state.canViewAccount || 
      state.canViewAccountGroup ||
      state.canViewOrganization ||
      state.canViewSubdivision ||
      state.canViewPosition ||
      state.canViewAccountPermission
    )
    console.log('Права на просмотр пользователей:', state.canViewUsers);

    state.canViewCategory = state.globalPermissionsList.includes('core.view_category') ||
      (state.objectPermissionsDict['core.view_category'] &&
      state.objectPermissionsDict['core.view_category']?.length > 0);
    console.log('Права на просмотр категорий:', state.canViewCategory);

    state.canViewSettings = true
    console.log('Права на просмотр настроек:', state.canViewUsers);

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

// Для меню
const isVisible = ref(false);
function toggleMenu() {
  isVisible.value = !isVisible.value;
}

// Для оповещений
const showNotificationsModal = ref(false);
const openNotificationsModal = () => {
  showNotificationsModal.value = true;
};
const closeNotificationsModal = () => {
  showNotificationsModal.value = false;
};

const number_notifications = ref(null);

watch(auth_user_id, (val) => {
  if (val) {
    loadUserPermissions();
    loadNotifications();
  }
});

const notifications = ref([]);
const loadNotifications = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (!token || !validToken) {
    clearUserId();
  }
  if (auth_user_id.value) {
    try {
      const response = await axios.get(`${baseUrl}/accounts/${auth_user_id.value }/task_notifications/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      notifications.value = response.data || [];
      number_notifications.value = notifications.value.length
      console.log('Все сообщения загружены:', notifications.value);
      const totalPages = Math.ceil(number_notifications.value / notificationsItemsPerPage);
      notificationsCurrentPage.value = totalPages > 0 ? totalPages : 1;

    } catch (error) {
      console.error('Ошибка при загрузке всех сообщений:', error.response ? error.response.data : error.notification);
    }
  }

};

const notificationsSearchQuery = ref('');
const notificationsCurrentPage = ref(1);
const notificationsItemsPerPage = 10;
const filteredNotifications = computed(() => {
  if (!notificationsSearchQuery.value) return notifications.value;
  return notifications.value.filter(notification => 
    notification.task?.str?.toLowerCase().includes(notificationsSearchQuery.value.toLowerCase())
  );
});
const notificationsTotalPages = computed(() => Math.ceil(filteredNotifications.value.length / notificationsItemsPerPage));
const paginatedNotifications = computed(() => {
  const start = (notificationsCurrentPage.value - 1) * notificationsItemsPerPage;
  const end = start + notificationsItemsPerPage;
  return filteredNotifications.value.slice(start, end);
});
watch(notificationsSearchQuery, () => {
  notificationsCurrentPage.value = 1;
});

const loadNewNotifications = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (!token || !validToken) { 
    localStorage.removeItem('access_token');
    token = null;
    clearUserId();
    console.log('Токен и auth_user_id очищены');
  } 

  if (auth_user_id.value) {
    const lastId = notifications.value.length ? Math.max(...notifications.value.map(n => n.id)) : 0;

    try {
      const response = await axios.get(`${baseUrl}/accounts/${auth_user_id.value }/task_notifications/`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { last_id: lastId },
      });
      if (response.data && response.data.length) {
        notifications.value = notifications.value.concat(response.data);
        console.log('Новые сообщения загружены:', response.data);
      } else {
        console.log('Новых сообщений нет');
      }
    } catch (error) {
      console.error('Ошибка при загрузке новых сообщений:', error.response ? error.response.data : error.notification);
    }
  }

};

const checkTokenValidity = () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (!token || !validToken) {
    localStorage.removeItem('access_token');
    token = null;
    clearUserId();
    console.log('Токен и auth_user_id очищены');
  }
};

let intervalId = null;
const startAutoReload = () => {
  intervalId = setInterval(() => {
    if (auth_user_id.value) {
      checkTokenValidity();
      loadNewNotifications();
    }
    console.log('Запрос на обновление сообщений отправлен:', new Date().toLocaleTimeString());
  }, 60000);
};

const stopAutoReload = () => {
  if (intervalId) clearInterval(intervalId);
}

const notificationRead = async (task_notification_id) => {
  const id = task_notification_id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (!token || !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.patch(`${baseUrl}/task_notifications/${id}/read/`, {}, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Результат ознакомления:', response.data); 

    if (response.data.task_notification_read == true) {
      const notification = notifications.value.find(n => n.id === task_notification_id);
      if (notification) notification.read = true;
    }

  } catch (error) {
    console.error('Ошибка при получении данных результата:', error);
  }

};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await checkPermissionsVersion();
    await loadUserPermissions();
    await loadNotifications();
    startAutoReload();
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

onBeforeUnmount(() => {
  stopAutoReload();
});

</script>

<style scoped>

/* Стили для заголовка */


</style>
