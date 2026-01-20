// Импортируем необходимые функции и компоненты для маршрутизации
import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';
import { baseUrl } from '../utils/utils';


// Определяем массив маршрутов
const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: () => import('../views/HomePage.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/home_page/create',
    name: 'HomePageCreate',
    component: () => import('../views/HomePageCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/home_page/:id/edit',
    name: 'HomePageEdit',
    component: () => import('../views/HomePageEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/legal_page',
    name: 'LegalPage',
    component: () => import('../views/LegalPage.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/legal_page/create',
    name: 'LegalPageCreate',
    component: () => import('../views/LegalPageCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/legal_page/:id/edit',
    name: 'LegalPageEdit',
    component: () => import('../views/LegalPageEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/policy_page',
    name: 'PolicyPage',
    component: () => import('../views/PolicyPage.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/policy_page/create',
    name: 'PolicyPageCreate',
    component: () => import('../views/PolicyPageCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/policy_page/:id/edit',
    name: 'PolicyPageEdit',
    component: () => import('../views/PolicyPageEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    //meta: { requiresAuth: true }
  },
  {
    path: '/post_register',
    name: 'PostRegister',
    component: () => import('../views/PostRegister.vue'),
    //meta: { requiresAuth: true }
  },
  {
    path: '/activate/:uid/:token',
    name: 'Activate',
    component: () => import('../views/Activate.vue'),
    // meta: { requiresAuth: false } 
  },
  {
    path: '/password_reset_request',
    name: 'PasswordResetRequest',
    component: () => import('../views/PasswordResetRequest.vue'),
    //meta: { requiresAuth: true }
  },
  {
    path: '/post_password_reset_request',
    name: 'PostPasswordResetRequest',
    component: () => import('../views/PostPasswordResetRequest.vue'),
    //meta: { requiresAuth: true }
  },
  {
    path: '/password_reset_confirm/:uid/:token',
    name: 'PasswordResetConfirm',
    component: () => import('../views/PasswordResetConfirm.vue'),
    // meta: { requiresAuth: false } 
  },
  {
    path: '/post_password_reset_confirm',
    name: 'PostPasswordResetConfirm',
    component: () => import('../views/PostPasswordResetConfirm.vue'),
    //meta: { requiresAuth: true }
  },
  {
    path: '/cabinet',
    name: 'Cabinet',
    component: () => import('../views/Cabinet.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/notification_settings/:id/edit',
    name: 'NotificationSettingsEdit',
    component: () => import('../views/NotificationSettingsEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/accounts',
    name: 'AccountList',
    component: () => import('../views/AccountList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        username: route.query.username || '',
        email: route.query.email || '',
        last_name: route.query.last_name || '',
        is_active: route.query.is_active || '',
        self_registration: route.query.self_registration || '',
        user_permissions: route.query.user_permissions
          ? route.query.user_permissions.map(permission => ({ id: parseInt(permission, 10) }))
          : [],
        order: route.query.order || 'last_name',
      }
    }),
  },
  {
    path: '/accounts/create',
    name: 'AccountCreate',
    component: () => import('../views/AccountCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/accounts/:id',
    name: 'AccountDetail',
    component: () => import('../views/AccountDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/accounts/:id/edit',
    name: 'AccountEdit',
    component: () => import('../views/AccountEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/clients',
    name: 'ClientList',
    component: () => import('../views/ClientList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'id',
      }
    }),
  },
  {
    path: '/clients/create',
    name: 'ClientCreate',
    component: () => import('../views/ClientCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/clients/:id',
    name: 'ClientDetail',
    component: () => import('../views/ClientDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/clients/:id/edit',
    name: 'ClientEdit',
    component: () => import('../views/ClientEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/placements/create/',
    name: 'CreatePlacement',
    component: () => import('../views/PlacementCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ accountId: route.query.accountId })
  },
  {
    path: '/placements/:id/edit',
    name: 'PlacementEdit',
    component: () => import('../views/PlacementEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ accountId: route.query.accountId })
  },
  {
    path: '/categories',
    name: 'CategoryList',
    component: () => import('../views/CategoryList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.username || '',
        parent_category: route.query.parent_category || null,
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/categories/create',
    name: 'CategoryCreate',
    component: () => import('../views/CategoryCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/categories/:id',
    name: 'CategoryDetail',
    component: () => import('../views/CategoryDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'desc' })
  },
  {
    path: '/categories/:id/edit',
    name: 'CategoryEdit',
    component: () => import('../views/CategoryEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/account_groups',
    name: 'AccountGroupList',
    component: () => import('../views/AccountGroupList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        type: route.query.type || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        accounts: route.query.accounts
        ? route.query.accounts.map(account => ({ id: parseInt(account, 10) }))
        : [],
        group_permissions: route.query.group_permissions
          ? route.query.group_permissions.map(permission => ({ id: parseInt(permission, 10) }))
          : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/account_groups/create',
    name: 'AccountGroupCreate',
    component: () => import('../views/AccountGroupCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/account_groups/:id',
    name: 'AccountGroupDetail',
    component: () => import('../views/AccountGroupDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/accounts_groups/:id/edit',
    name: 'AccountGroupEdit',
    component: () => import('../views/AccountGroupEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/accounts_group_generator/create/',
    name: 'CreateAccountGroupGenerator',
    component: () => import('../views/AccountGroupGeneratorCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ groupId: route.query.groupId })
  },
  {
    path: '/accounts_group_generator/:id/edit',
    name: 'AccountGroupGeneratorEdit',
    component: () => import('../views/AccountGroupGeneratorEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ groupId: route.query.groupId })
  },
  {
    path: '/accounts_group_object_permissions/create/',
    name: 'CreateAccountsGroupObjectPermission',
    component: () => import('../views/AccountsGroupObjectPermissionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ contentTypeModel: route.query.contentTypeId, objectPk: route.query.objectPk })
  },
  {
    path: '/account_object_permissions/create/',
    name: 'CreateAccountObjectPermission',
    component: () => import('../views/AccountObjectPermissionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ contentTypeModel: route.query.contentTypeId, objectPk: route.query.objectPk })
  },
  {
    path: '/organizations',
    name: 'OrganizationList',
    component: () => import('../views/OrganizationList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        legal_name: route.query.legal_name || '',
        tin: route.query.tin || null,
        order: route.query.order || 'legal_name',
      }
    }),
  },
  {
    path: '/organizations/create',
    name: 'OrganizationCreate',
    component: () => import('../views/OrganizationCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/organizations/:id',
    name: 'OrganizationDetail',
    component: () => import('../views/OrganizationDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/organizations/:id/edit',
    name: 'OrganizationEdit',
    component: () => import('../views/OrganizationEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/subdivisions',
    name: 'SubdivisionList',
    component: () => import('../views/SubdivisionList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        organization: route.query.organization || null,
        parent_subdivision: route.query.parent_subdivision || null,
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/subdivisions/create',
    name: 'SubdivisionCreate',
    component: () => import('../views/SubdivisionCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/subdivisions/:id',
    name: 'SubdivisionDetail',
    component: () => import('../views/SubdivisionDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/subdivisions/:id/edit',
    name: 'SubdivisionEdit',
    component: () => import('../views/SubdivisionEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/positions',
    name: 'PositionList',
    component: () => import('../views/PositionList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        subdivision: route.query.subdivision || null,
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/positions/create',
    name: 'PositionCreate',
    component: () => import('../views/PositionCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/positions/:id',
    name: 'PositionDetail',
    component: () => import('../views/PositionDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/positions/:id/edit',
    name: 'PositionEdit',
    component: () => import('../views/PositionEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/interactions',
    name: 'InteractionList',
    component: () => import('../views/InteractionList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        id: route.query.id || null,
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'id',
      }
    }),
  },
  {
    path: '/interactions/create',
    name: 'InteractionCreate',
    component: () => import('../views/InteractionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/interactions/:id',
    name: 'InteractionDetail',
    component: () => import('../views/InteractionDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/interactions/:id/edit',
    name: 'InteractionEdit',
    component: () => import('../views/InteractionEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/task_templates',
    name: 'TaskTemplateList',
    component: () => import('../views/TaskTemplateList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'plan__name',
      }
    }),
  },
  {
    path: '/task_templates/create',
    name: 'TaskTemplateCreate',
    component: () => import('../views/TaskTemplateCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/task_templates/:id',
    name: 'TaskTemplateDetail',
    component: () => import('../views/TaskTemplateDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/task_templates/:id/edit',
    name: 'TaskTemplateEdit',
    component: () => import('../views/TaskTemplateEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/public_tasks',
    name: 'PublicTaskList',
    component: () => import('../views/PublicTaskList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/public_tasks/create',
    name: 'PublicTaskCreate',
    component: () => import('../views/PublicTaskCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/public_tasks/:id',
    name: 'PublicTaskDetail',
    component: () => import('../views/PublicTaskDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/public_tasks/:id/edit',
    name: 'PublicTaskEdit',
    component: () => import('../views/PublicTaskEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/public_plans',
    name: 'PublicPlanList',
    component: () => import('../views/PublicPlanList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/public_plans/create',
    name: 'PublicPlanCreate',
    component: () => import('../views/PublicPlanCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/public_plans/:id',
    name: 'PublicPlanDetail',
    component: () => import('../views/PublicPlanDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/public_plans/:id/edit',
    name: 'PublicPlanEdit',
    component: () => import('../views/PublicPlanEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: () => import('../views/TaskList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'plan__name',
      }
    }),
  },
  {
    path: '/tasks/create',
    name: 'TaskCreate',
    component: () => import('../views/TaskCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/tasks/:id',
    name: 'TaskDetail',
    component: () => import('../views/TaskDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/tasks/:id/edit',
    name: 'TaskEdit',
    component: () => import('../views/TaskEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/tasks/:id/task_result_update',
    name: 'TaskResultUpdate',
    component: () => import('../views/TaskResultUpdate.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tasks/:id/plan_result_update',
    name: 'PlanResultUpdate',
    component: () => import('../views/PlanResultUpdate.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/task_template_assignments',
    name: 'TaskTemplateAssignmentList',
    component: () => import('../views/TaskTemplateAssignmentList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/task_template_assignments/create',
    name: 'TaskTemplateAssignmentCreate',
    component: () => import('../views/TaskTemplateAssignmentCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/task_template_assignments/:id',
    name: 'TaskTemplateAssignmentDetail',
    component: () => import('../views/TaskTemplateAssignmentDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/queues',
    name: 'QueueList',
    component: () => import('../views/QueueList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'planned_end',
      }
    }),
  },
  {
    path: '/queues/create',
    name: 'QueueCreate',
    component: () => import('../views/QueueCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/queues/:id',
    name: 'QueueDetail',
    component: () => import('../views/QueueDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/queues/:id/edit',
    name: 'QueueEdit',
    component: () => import('../views/QueueEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/queue_executors/create/',
    name: 'CreateQueueExecutor',
    component: () => import('../views/QueueExecutorCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ queueId: route.query.queueId })
  },
  {
    path: '/queue_executors/:id/edit',
    name: 'QueueExecutorEdit',
    component: () => import('../views/QueueExecutorEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ queueId: route.query.queueId })
  },
  {
    path: '/queue_tasks/create/',
    name: 'CreateQueueTask',
    component: () => import('../views/QueueTaskCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ queueId: route.query.queueId })
  },
  {
    path: '/control_elements',
    name: 'ControlElementList',
    component: () => import('../views/ControlElementList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
      }
    }),
  },
  {
    path: '/control_elements/create',
    name: 'ControlElementCreate',
    component: () => import('../views/ControlElementCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId })
  },
  {
    path: '/control_elements/:id',
    name: 'ControlElementDetail',
    component: () => import('../views/ControlElementDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/control_elements/:id/edit',
    name: 'ControlElementEdit',
    component: () => import('../views/ControlElementEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId })
  },
  {
    path: '/control_element_events/create/',
    name: 'CreateControlElementEvent',
    component: () => import('../views/ControlElementEventCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/control_element_events/:id/edit',
    name: 'ControlElementEventEdit',
    component: () => import('../views/ControlElementEventEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/control_element_conditions/create/',
    name: 'CreateControlElementCondition',
    component: () => import('../views/ControlElementConditionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/control_element_conditions/:id/edit',
    name: 'ControlElementConditionEdit',
    component: () => import('../views/ControlElementConditionEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/control_element_actions/create/',
    name: 'CreateControlElementAction',
    component: () => import('../views/ControlElementActionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/control_element_actions/:id/edit',
    name: 'ControlElementActionEdit',
    component: () => import('../views/ControlElementActionEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ control_elementId: route.query.control_elementId })
  },
  {
    path: '/task_analytics',
    name: 'TaskAnalytics',
    component: () => import('../views/TaskAnalytics.vue'),
    //meta: { requiresAuth: true },
  },
  {
    path: '/chats',
    name: 'ChatList',
    component: () => import('../views/ChatList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/chats/create',
    name: 'ChatCreate',
    component: () => import('../views/ChatCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId, queueId: route.query.queueId })
  },
  {
    path: '/chats/:id',
    name: 'ChatDetail',
    component: () => import('../views/ChatDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'desc' })
  },
  {
    path: '/chats/:id/edit',
    name: 'ChatEdit',
    component: () => import('../views/ChatEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId, queueId: route.query.queueId })
  },
  {
    path: '/topics',
    name: 'TopicList',
    component: () => import('../views/TopicList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/topics/create',
    name: 'TopicCreate',
    component: () => import('../views/TopicCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId, queueId: route.query.queueId })
  },
  {
    path: '/topics/:id',
    name: 'TopicDetail',
    component: () => import('../views/TopicDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'desc' })
  },
  {
    path: '/topics/:id/edit',
    name: 'TopicEdit',
    component: () => import('../views/TopicEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ taskId: route.query.taskId, queueId: route.query.queueId })
  },
  {
    path: '/files',
    name: 'FileList',
    component: () => import('../views/FileList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/files/create',
    name: 'FileCreate',
    component: () => import('../views/FileCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/files/:id',
    name: 'FileDetail',
    component: () => import('../views/FileDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/files/:id/edit',
    name: 'FileEdit',
    component: () => import('../views/FileEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/news',
    name: 'NewList',
    component: () => import('../views/NewList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'created',
      }
    }),
  },
  {
    path: '/news/create',
    name: 'NewCreate',
    component: () => import('../views/NewCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/news/:id',
    name: 'NewDetail',
    component: () => import('../views/NewDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/news/:id/edit',
    name: 'NewEdit',
    component: () => import('../views/NewEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/new_content/:id',
    name: 'NewContent',
    component: () => import('../views/NewContent.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/materials',
    name: 'MaterialList',
    component: () => import('../views/MaterialList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/materials/create',
    name: 'MaterialCreate',
    component: () => import('../views/MaterialCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/materials/:id',
    name: 'MaterialDetail',
    component: () => import('../views/MaterialDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/materials/:id/edit',
    name: 'MaterialEdit',
    component: () => import('../views/MaterialEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/material_content/:id',
    name: 'MaterialContent',
    component: () => import('../views/MaterialContent.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/course',
    name: 'CourseList',
    component: () => import('../views/CourseList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/course/create',
    name: 'CourseCreate',
    component: () => import('../views/CourseCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/course/:id',
    name: 'CourseDetail',
    component: () => import('../views/CourseDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/course/:id/edit',
    name: 'CourseEdit',
    component: () => import('../views/CourseEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/scorm_content/:id',
    name: 'ScormContent',
    component: () => import('../views/ScormContent.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/test',
    name: 'TestList',
    component: () => import('../views/TestList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/test/create',
    name: 'TestCreate',
    component: () => import('../views/TestCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/test/:id',
    name: 'TestDetail',
    component: () => import('../views/TestDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/test/:id/edit',
    name: 'TestEdit',
    component: () => import('../views/TestEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/test_sections/create',
    name: 'TestSectionCreate',
    component: () => import('../views/TestSectionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ testId: route.query.testId })
  },
  {
    path: '/test_sections/:id/edit',
    name: 'TestSectionEdit',
    component: () => import('../views/TestSectionEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ testId: route.query.testId })
  },
  {
    path: '/test_section_questions/create',
    name: 'TestSectionQuestionCreate',
    component: () => import('../views/TestSectionQuestionCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ testId: route.query.testId, testSectionId: route.query.testSectionId })
  },
  {
    path: '/test_section_questions/:id/edit',
    name: 'TestSectionQuestionEdit',
    component: () => import('../views/TestSectionQuestionEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ testId: route.query.testId, testSectionId: route.query.testSectionId })
  },
  {
    path: '/question',
    name: 'QuestionList',
    component: () => import('../views/QuestionList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        text: route.query.text || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'text',
      }
    }),
  },
  {
    path: '/question/create',
    name: 'QuestionCreate',
    component: () => import('../views/QuestionCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/question/:id',
    name: 'QuestionDetail',
    component: () => import('../views/QuestionDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/question/:id/edit',
    name: 'QuestionEdit',
    component: () => import('../views/QuestionEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/answers/create',
    name: 'AnswerCreate',
    component: () => import('../views/AnswerCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ questionId: route.query.questionId })
  },
  {
    path: '/answers/:id/edit',
    name: 'AnswerEdit',
    component: () => import('../views/AnswerEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ questionId: route.query.questionId })
  },
    {
    path: '/relevant_points/create',
    name: 'RelevantPointCreate',
    component: () => import('../views/RelevantPointCreate.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ answerId: route.query.answerId, questionId: route.query.questionId })
  },
  {
    path: '/relevant_points/:id/edit',
    name: 'RelevantPointEdit',
    component: () => import('../views/RelevantPointEdit.vue'),
    meta: { requiresAuth: true },
    props: (route) => ({ answerId: route.query.answerId, questionId: route.query.questionId })
  },
  {
    path: '/test_attempt/:id',
    name: 'TestAttempt',
    component: () => import('../views/TestAttempt.vue'),
    //meta: { requiresAuth: true },
    //props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/event_template',
    name: 'EventTemplateList',
    component: () => import('../views/EventTemplateList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        categories: route.query.categories
        ? route.query.categories.map(category => ({ id: parseInt(category, 10) }))
        : [],
        order: route.query.order || 'name',
      }
    }),
  },
  {
    path: '/event_template/create',
    name: 'EventTemplateCreate',
    component: () => import('../views/EventTemplateCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/event_template/:id',
    name: 'EventTemplateDetail',
    component: () => import('../views/EventTemplateDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/event_template/:id/edit',
    name: 'EventTemplateEdit',
    component: () => import('../views/EventTemplateEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/event_slot',
    name: 'EventSlotList',
    component: () => import('../views/EventSlotList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        order: route.query.order || 'planned_start',
      }
    }),
  },
  {
    path: '/event_slot/create',
    name: 'EventSlotCreate',
    component: () => import('../views/EventSlotCreate.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/event_slot/:id',
    name: 'EventSlotDetail',
    component: () => import('../views/EventSlotDetail.vue'),
    //meta: { requiresAuth: true },
    props: (route) => ({ activeTab: route.query.tab || 'details' })
  },
  {
    path: '/event_slot/:id/edit',
    name: 'EventSlotEdit',
    component: () => import('../views/EventSlotEdit.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/event_slot_select/:id',
    name: 'EventSlotSelect',
    component: () => import('../views/EventSlotSelect.vue'),
    meta: { requiresAuth: true },
    //props: (route) => ({ planId: route.query.planId })
  },
  {
    path: '/account_permission',
    name: 'AccountPermissionList',
    component: () => import('../views/AccountPermissionList.vue'),
    //meta: { requiresAuth: true },
    props: route => ({
      page: parseInt(route.query.page, 10) || 1,
      filters: {
        name: route.query.name || '',
        account: route.query.account || null,
        order: route.query.order || 'name',
      }
    }),
  },
];

// Создаем маршрутизатор
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Глобальный навигационный guard
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.error('Token is empty, redirecting to login');
      next({
        name: 'Login',
        query: { redirect: to.fullPath } // Сохраняем текущий путь в параметр redirect
      });
    } else {
      try {
        // Проверка действительности токена
        const response = await axios.get(`${baseUrl}/check-token/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        console.log('Token is valid:', response.data); // Токен действителен
        next(); // Переходим на защищенный маршрут
      } catch (error) {
        console.error('Token is invalid, redirecting to login', error.response.data); // Токен недействителен
        localStorage.removeItem('access_token'); // Удаляем старый токен
        next({
          name: 'Login',
          query: { redirect: to.fullPath } // Сохраняем текущий путь
        });
      }
    }
  } else {
    next(); // Переход к незащищённым маршрутам
  }
});

// Экспортируем маршрутизатор
export default router;
