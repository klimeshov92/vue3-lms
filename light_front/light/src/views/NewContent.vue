<template>
  <div v-if="loading">
    <div v-if="state.canPerform" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.task.new.name || 'Безымянная новость' }}</h1>
              </div>
            </div>
            <div class="material-content">
              <div v-html="state.object.task.new.content" class="tiptap"></div>
            </div>
            <div class="detail-menu button-group">

              <button
                v-if="state.canCompleted"
                @click="newReview"
                class="button"
              >
                Подтвердить ознакомление
              </button>

              <button type="button" @click="back" class="button">Назад</button>

            </div>
            <div></div>
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

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canPerform: false,
  canCompleted: false,
});

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/new_content/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные результата:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных результата:', error);
  }
};

const back = () => {
  router.back();
};

const newReview = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.patch(`${baseUrl}/new_review/${id}/`, {}, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Результат ознакомления:', response.data);
    state.canCompleted = false;
  } catch (error) {
    console.error('Ошибка при получении данных результата:', error);
  }
};

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

    const id = route.params.id;
    console.log('ID объекта:', id);

    if (
      state.object.status !=  'failed' && state.object.status !=  'canceled'
    ) {
      state.canPerform = state.object.task.executor == validToken.user_id
    }
    console.log('Просмотр результата:', state.canPerform);
    if (
      state.object.status !=  'completed' && state.object.status !=  'failed' && state.object.status !=  'canceled'
    ) {
      state.canCompleted = state.object.task.executor == validToken.user_id
    } 
    console.log('Редактирование результата:', state.canCompleted);

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

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
