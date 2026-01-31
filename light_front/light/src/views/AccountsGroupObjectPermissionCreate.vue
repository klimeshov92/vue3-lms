<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание объектных прав</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label for="content_type" class="form-label">Тип контента:</label>
          <multiselect
            v-model="form.content_type"
            :options="content_types"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите тип контента"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :disabled="!!contentTypeModel"
          >
          <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.content_type" class="error">{{ errors.content_type }}</span>
        </div>

        <div class="form-field">
          <label for="object_pk" class="form-label">Идентификатор:</label>
          <input 
          v-model="form.object_pk" 
          id="object_pk" 
          type="number" 
          class="form-input" 
          placeholder="Введите иднетификатор объекта" 
          :disabled="!!objectPk"  
          required 
          />
          <span v-if="errors.object_pk" class="error">{{ errors.object_pk }}</span>
        </div>

        <div class="form-field">
          <label for="group" class="form-label">Группа:</label>
          <multiselect
            v-model="form.group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу"
            label="name"
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

        <div class="form-field">
          <label for="permission" class="form-label">Право:</label>
          <multiselect
            v-model="form.permission"
            :options="filteredPermissions"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            :placeholder="!form.content_type || !form.object_pk ? 'Сначала выберите тип контента и идентификатор' : 'Выберите право'"
            label="name"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!form.content_type"
          >
          <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.permission" class="error">{{ errors.permission }}</span>
        </div>
      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

  </div>

</template>

<script setup>
import { reactive, computed, watch, onMounted, ref } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const router = useRouter();
const route = useRoute();

const loading = ref(false);

const form = reactive({
  content_type: null,
  object_pk: null,
  group: null,
  permission: null,
});
const errors = reactive({});

const content_types = ref([]);
const loadContentTypes = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/content_types/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    content_types.value = response.data.results || [];
    console.log('Типы контента загружены:', content_types.value);
  } catch (error) {
    console.error('Ошибка при загрузке типов контента:', error.response ? error.response.data : error.message);
  }
};

const contentTypeModel = route.query.contentTypeModel || '';
const loadContentTypeByModel = () => {
  if (contentTypeModel) {
    console.log('Тип контента объекта:', contentTypeModel);
    const content_type = content_types.value.find(content_type => content_type.model === contentTypeModel);
    if (content_type) {
      form.content_type = content_type;
    } else {
      console.error('Тип контента объекта не найден.');
    }
  } else {
    console.log('Тип контента объекта не найден.');
  }
};

const objectPk = route.query.objectPk || '';
const loadObjectPk = () => {
  if (objectPk) {
    console.log('Идентификатор объета:', objectPk);
    const object_pk = objectPk;
    if (object_pk) {
      form.object_pk = parseInt(object_pk, 10);
    } else {
      console.error('Идентификатор объета не найден.');
    }
  } else {
    console.log('Идентификатор объета не найден.');
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

const permissions = ref([]);
const loadPermissions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/permissions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    permissions.value = response.data.results || [];
    console.log('Разрешения загружены:', permissions.value);
  } catch (error) {
    console.error('Ошибка при загрузке разрешений:', error.response ? error.response.data : error.message);
  }
};

const filteredPermissions = computed(() => {
  if (!form.content_type || !form.content_type.model) {
    return [];
  }
  return permissions.value.filter(permission => 
    permission.content_type.model === form.content_type.model &&
    !permission.codename.startsWith('add')
  );
});

watch(() => form.content_type, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    form.permission = null;
    console.log('Смена типа контента: очищаем выбранное право');
  }
});

const validateForm = () => {
  errors.content_type = form.content_type ? '' : 'Тип контента обязателен!';
  errors.object_pk = form.object_pk ? '' : 'ID объекта обязателен!';
  errors.group = form.group ? '' : 'Группа обязательна!';
  errors.permission = form.permission ? '' : 'Право обязательно!';
  return Object.values(errors).every((error) => !error);
};

const createObject = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    console.log('Отправляем данные для создания объекта:', form);
    const jsonData = {
      content_type: form.content_type.id,
      object_pk: form.object_pk,
      group: form.group.id,
      permission: form.permission.id,
    };


    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/accounts_group_object_permissions/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    if (form.content_type.model === 'interaction') {
      const interactionId = form.object_pk;
      router.push({ name: 'InteractionDetail', params: { id: interactionId }  });
    } else if (form.content_type.model === 'account') {
      const accountId = form.object_pk;
      router.push({ name: 'AccountDetail', params: { id: accountId }  });
    } else if (form.content_type.model === 'accountsgroup') {
      const groupId = form.object_pk;
      router.push({ name: 'AccountGroupDetail', params: { id: groupId }  });
    } else if (form.content_type.model === 'category') {
      const categoryId = form.object_pk;
      router.push({ name: 'CategoryDetail', params: { id: categoryId }  });
    } else if (form.content_type.model === 'organization') {
      const organizationId = form.object_pk;
      router.push({ name: 'OrganizationDetail', params: { id: organizationId }  });
    } else if (form.content_type.model === 'subdivision') {
      const subdivisionId = form.object_pk;
      router.push({ name: 'SubdivisionDetail', params: { id: subdivisionId }  });
    } else if (form.content_type.model === 'position') {
      const positionId = form.object_pk;
      router.push({ name: 'PositionDetail', params: { id: positionId }  });
    } else if (form.content_type.model === 'tasktemplate') {
      const taskTemplateId = form.object_pk;
      router.push({ name: 'TaskTemplateDetail', params: { id: taskTemplateId }  });
    } else if (form.content_type.model === 'task') {
      const taskId = form.object_pk;
      router.push({ name: 'TaskDetail', params: { id: taskId }  });
    } else if (form.content_type.model === 'queue') {
      const queueId = form.object_pk;
      router.push({ name: 'QueueDetail', params: { id: queueId }  });
    } else if (form.content_type.model === 'controlelement') {
      const controlelementId = form.object_pk;
      router.push({ name: 'ControlElementDetail', params: { id: controlelementId }  });
    } else if (form.content_type.model === 'file') {
      const fileId = form.object_pk;
      router.push({ name: 'FileDetail', params: { id: fileId }  });
    } else if (form.content_type.model === 'material') {
      const materialId = form.object_pk;
      router.push({ name: 'MaterialDetail', params: { id: materialId }  });
    } else if (form.content_type.model === 'new') {
      const newId = form.object_pk;
      router.push({ name: 'NewDetail', params: { id: newId }  });
    } else if (form.content_type.model === 'course') {
      const courseId = form.object_pk;
      router.push({ name: 'CourseDetail', params: { id: courseId }  });
    } else if (form.content_type.model === 'test') {
      const testId = form.object_pk;
      router.push({ name: 'TestDetail', params: { id: testId }  });
    } else if (form.content_type.model === 'question') {
      const questionId = form.object_pk;
      router.push({ name: 'QuestionDetail', params: { id: questionId }  });
    } else if (form.content_type.model === 'eventtemplate') {
      const eventTemplateId = form.object_pk;
      router.push({ name: 'EventTemplateDetail', params: { id: eventTemplateId }  });
    } else if (form.content_type.model === 'eventslot') {
      const eventSlotId = form.object_pk;
      router.push({ name: 'EventSlotDetail', params: { id: eventSlotId }  });
    } else if (form.content_type.model === 'topic') {
      const topicId = form.object_pk;
      router.push({ name: 'TopicDetail', params: { id: topicId }  });
    } else if (form.content_type.model === 'chat') {
      const chatId = form.object_pk;
      router.push({ name: 'ChatDetail', params: { id: chatId }  });
    }
   

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }
};

const cancelEdit = () => {
  goBackSmart(router);
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadContentTypes();
    await loadContentTypeByModel();
    await loadObjectPk();
    await loadGroups();
    await loadPermissions();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>
