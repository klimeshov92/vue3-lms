<template>

  <div v-if="props.state.canViewAccountObjectPermission">
    <div v-if="props.state.object.account_object_permissions && props.state.object.account_object_permissions.length > 0" class="table-tab-table-outer">
      <div class="table-tab-table-inner">
        <table>
          <thead>
              <tr>
                  <th>Владелец</th>
                  <th>Право</th>
                  <th>Тип контента</th>
                  <th>Объект</th>
                  <th>Действия</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="account_object_permission in props.state.object.account_object_permissions" :key="account_object_permission.id">
              <td>{{ account_object_permission.user.str ? account_object_permission.user.str : 'Нет данных' }}</td>
              <td>{{ account_object_permission.permission.name ? account_object_permission.permission.name : 'Нет данных' }}</td>
              <td>{{ account_object_permission.permission.content_type.str ? account_object_permission.permission.content_type.str : 'Нет данных' }}</td>
              <td>{{ account_object_permission.content_object ? account_object_permission.content_object : 'Нет данных' }}</td>
              <td>
                <div v-if="props.state.canDeleteAccountObjectPermission">
                  <div class="table-tab-menu">
                    <button 
                      v-if="props.state.canDeleteAccountObjectPermission" 
                      @click="openAccountObjectPermissionDeleteModal(account_object_permission)"
                      class="table-tab-button"
                    >
                      Удалить
                    </button>
                    <div v-if="showAccountObjectPermissionDeleteModal" class="modal-overlay">
                      <div class="modal">
                        <div class="modal-header">
                          <h2 class="modal-header-h2">Удаление {{ selectedAccountObjectPermission.content_object || 'Объектное право без пользователя' }} {{ selectedAccountObjectPermission.permission.name || 'Безымянное объектное право' }}</h2>
                        </div>
                        <div class="minibutton-group modal-menu">
                          <button @click="confirmAccountObjectPermissionDelete(selectedAccountObjectPermission.id)" class="minibutton">Подтвердить</button>
                          <button @click="closeAccountObjectPermissionDeleteModal" class="minibutton">Отменить</button>
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
      <div class="none-border">Нет объектных прав</div>
    </div>
  </div>

  <div v-if="props.state.canAddAccountObjectPermission" class="tab-menu minibutton-group">
    <router-link
      v-if="props.state.canAddAccountObjectPermission"
      :to="{ name: 'CreateAccountObjectPermission', query: { contentTypeModel: props.contentTypeModel, objectPk: props.state.object.id } }"
      class="minibutton"
    >
      Добавить
    </router-link>
  </div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, reactive, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router'; // Работа с роутингом
import { formatDate, formatDateTime, baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import axios from 'axios'; // Импорт axios для запросов
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute(); // Получение информации о текущем маршруте
const router = useRouter(); // Использование маршрутизатора

const loading = ref(false);

const props = defineProps({
  contentTypeModel: String,
  state: Object,
  fetchObject: Function,
});
console.log("contentTypeModel:", props.contentTypeModel);
console.log("State:", props.state);
console.log("fetchObject:", props.fetchObject);


const showAccountObjectPermissionDeleteModal = ref(false);
const selectedAccountObjectPermission = ref(null);
const openAccountObjectPermissionDeleteModal = (account_object_permission) => {
  selectedAccountObjectPermission.value = account_object_permission;
  showAccountObjectPermissionDeleteModal.value = true;
};
const closeAccountObjectPermissionDeleteModal = () => {
  showAccountObjectPermissionDeleteModal.value = false;
};
const confirmAccountObjectPermissionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/account_object_permissions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await props.fetchObject();
    closeAccountObjectPermissionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления объектного права пользователя:', error);
  }
};


</script>

<style scoped>
</style>
