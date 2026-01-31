<template>
  <div v-if="loading">
    <div v-if="state.canViewPolicyPage" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.title || 'Безымянный материал' }}</h1>
              </div>
            </div>
            <div class="material-content">
              <div v-html="state.object.content" class="tiptap"></div>
            </div>
            <div v-if="state.canEditPolicyPage" class="detail-menu button-group">

              <router-link
                v-if="state.canEditPolicyPage"  
                :to="{ name: 'PolicyPageEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>

            </div>
            <div></div>
          </div>
        </div>
        
      </div>
      <div v-else-if="!state.object.id" class="none-container">

        <div class="none-card">
          <div>Объект не найден.</div>
        </div>

        <div v-if="state.canAddPolicyPage" class="detail-menu button-group none-menu-padding">

          <router-link
            :to="{ name: 'PolicyPageCreate' }"
            class="button"
          >
            Создать
          </router-link>

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
import { formatDate, formatDateTime, baseUrl, isTokenValid , goBackSmart } from '../utils/utils'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewPolicyPage: false,
  canEditPolicyPage: false,
  canAddPolicyPage: false,
});

const fetchObject = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/policy_page_content/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные результата:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных страницы:', error);
  }
};

const back = () => {
  goBackSmart(router);
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
    router.push({ name: 'Login' });
    return;
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

    state.canViewPolicyPage = true

    state.canAddPolicyPage = state.globalPermissionsList.includes('core.add_policy_page');
    console.log('Права на добавление страницы:', state.canAddPolicyPage);

    state.canEditPolicyPage = state.globalPermissionsList.includes('core.change_policy_page') ||
      (Array.isArray(state.objectPermissionsDict['core.change_policy_page']) &&
      state.objectPermissionsDict['core.change_policy_page'].includes(Number(id)));
    console.log('Права на редактирование страницы:', state.canEditPolicyPage);

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

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
