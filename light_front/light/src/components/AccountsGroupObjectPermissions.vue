<template>

  <div v-if="props.state.canViewAccountsGroupObjectPermission">
    <div v-if="props.state.object.accounts_group_object_permissions && props.state.object.accounts_group_object_permissions.length > 0" class="table-tab-table-outer">
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
            <tr v-for="accounts_group_object_permission in props.state.object.accounts_group_object_permissions" :key="accounts_group_object_permission.id">
              <td>{{ accounts_group_object_permission.group.name ? accounts_group_object_permission.group.name : 'Нет данных' }}</td>
              <td>{{ accounts_group_object_permission.permission.name ? accounts_group_object_permission.permission.name : 'Нет данных' }}</td>
              <td>{{ accounts_group_object_permission.permission.content_type.str ? accounts_group_object_permission.permission.content_type.str : 'Нет данных' }}</td>
              <td>{{ accounts_group_object_permission.content_object ? accounts_group_object_permission.content_object : 'Нет данных' }}</td>
              <td>
                <div v-if="props.state.canDeleteAccountsGroupObjectPermission">
                  <div class="table-tab-menu">
                    <button 
                      v-if="props.state.canDeleteAccountsGroupObjectPermission" 
                      @click="openAccountsGroupObjectPermissionDeleteModal(accounts_group_object_permission)"
                      class="table-tab-button"
                    >
                      Удалить
                    </button>
                    <div v-if="showAccountsGroupObjectPermissionDeleteModal" class="modal-overlay">
                      <div class="modal">
                        <div class="modal-header">
                          <h2 class="modal-header-h2">Удаление {{ selectedAccountsGroupObjectPermission.content_object || 'Объектное право без пользователя' }} {{ selectedAccountsGroupObjectPermission.permission.name || 'Безымянное объектное право' }}</h2>
                        </div>
                        <div class="minibutton-group modal-menu">
                          <button @click="confirmAccountsGroupObjectPermissionDelete(selectedAccountsGroupObjectPermission.id)" class="minibutton">Подтвердить</button>
                          <button @click="closeAccountsGroupObjectPermissionDeleteModal" class="minibutton">Отменить</button>
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

  <div v-if="props.state.canAddAccountsGroupObjectPermission" class="tab-menu minibutton-group">
    <router-link
      v-if="props.state.canAddAccountsGroupObjectPermission"
      :to="{ name: 'CreateAccountsGroupObjectPermission', query: { contentTypeModel: props.contentTypeModel, objectPk: props.state.object.id } }"
      class="minibutton"
    >
      Добавить
    </router-link>
  </div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, reactive, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router'; // Работа с роутингом
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils';
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

const showAccountsGroupObjectPermissionDeleteModal = ref(false);
const selectedAccountsGroupObjectPermission = ref(null);
const openAccountsGroupObjectPermissionDeleteModal = (accounts_group_object_permission) => {
  selectedAccountsGroupObjectPermission.value = accounts_group_object_permission;
  showAccountsGroupObjectPermissionDeleteModal.value = true;
};
const closeAccountsGroupObjectPermissionDeleteModal = () => {
  showAccountsGroupObjectPermissionDeleteModal.value = false;
};
const confirmAccountsGroupObjectPermissionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/accounts_group_object_permissions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await  props.fetchObject();
    closeAccountsGroupObjectPermissionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления объектного права группы:', error);
  }
};

</script>

<style scoped>
</style>
