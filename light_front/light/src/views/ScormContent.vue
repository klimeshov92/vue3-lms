<template>
  <div v-if="loading">
    <div v-if="state.canPerform" class="detail-page">
      <div v-if="state.object.course_id">
        <button @click="enterFullscreen" class="fullscreen-btn"> На весь экран </button>
        <div class="scorm-player">
          <iframe
            ref="scormIframe"
            class="scorm-player-iframe"
            :src="wrapperUrl"
            allowfullscreen
            webkitallowfullscreen
          ></iframe>
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
import { formatDate, formatDateTime, staticUrl, baseUrl, isTokenValid } from '../utils/utils'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canPerform: false,
});

const scormIframe = ref(null)
const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/scorm_content/${id}/`, {
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
const wrapperUrl = computed(() => {
  if (!state.object) return ''

  // Кодируем параметры, которые wrapper.html может прочитать из URL
  const taskId = encodeURIComponent(state.object.task_id);
  const courseId = encodeURIComponent(state.object.course_id);
  const userId = encodeURIComponent(state.object.user_id);
  const packageType = encodeURIComponent(state.object.type);

  return `${staticUrl}/scorm_wrapper.html?task_id=${taskId}&course_id=${courseId}&user_id=${userId}&type=${packageType}`
});

const enterFullscreen = () => {
  if (!scormIframe.value) {
    console.warn('Элемент iframe не найден');
    return;
  }

  if (scormIframe.value.requestFullscreen) {
    console.log('Вызван requestFullscreen (стандартный)');
    scormIframe.value.requestFullscreen();
  } else if (scormIframe.value.mozRequestFullScreen) {
    console.log('Вызван mozRequestFullScreen (Firefox)');
    scormIframe.value.mozRequestFullScreen();
  } else if (scormIframe.value.webkitRequestFullscreen) {
    console.log('Вызван webkitRequestFullscreen (Chrome, Safari, Opera)');
    scormIframe.value.webkitRequestFullscreen();
  } else if (scormIframe.value.msRequestFullscreen) {
    console.log('Вызван msRequestFullscreen (IE/Edge)');
    scormIframe.value.msRequestFullscreen();
  } else {
    console.warn('Полноэкранный режим не поддерживается этим браузером');
  }
};

const back = () => {
  router.back();
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
      state.canPerform = state.object.user_id == validToken.user_id
    }
    console.log('Редактирование результата:', state.canPerform);

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
