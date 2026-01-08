
<template>

  <div v-if="loading" class="chat">

    <div v-if="messages?.length > 0" class="tab-search-field">
      <input 
        v-model="messagesSearchQuery" 
        type="text" 
        placeholder="Поиск" 
        class="tab-search-input"
      />
    </div>

    <div>

      <div v-if="filteredMessages?.length > 0" class="messages-list">

        <div 
          v-for="msg in paginatedMessages" 
          :key="msg.id" 
          class="message"
          :class="getMessageClass(msg)"
        >
          <div class="message-top">
            <div class="message-title">
              <h2>{{ msg.sender.str ? msg.sender.str : 'Без отправителя' }}</h2>
            </div>
          </div>
          <div class="message-detail">
            <div v-if="currentlyEditingMessageId === msg.id"> 
              <EditorComponent v-model="msg.editedContent" />
              <span v-if="msg.editErrors?.editedContent" class="error">
                {{ msg.editErrors.editedContent }}
              </span>
            </div>
            <div v-else v-html="msg.content" class="tiptap"></div>
            <div>
              <p>
                {{ msg.changed ? formatDateTime(msg.changed) : 'Без даты и времени' }}
              </p>
            </div>
          </div>
          <div class="chat-menu-outer">
            <div class="chat-menu-inner">
              <button class="table-tab-button" v-if="!currentlyEditingMessageId" @click="replyOnMessage(msg)">Ответить</button>
              <button class="table-tab-button" v-if="!currentlyEditingMessageId && user_id && msg.sender.id == user_id" @click="startEditing(msg)">Редактировать</button>
              <button class="table-tab-button" v-if="currentlyEditingMessageId === msg.id" @click="saveEdit(msg)">Сохранить</button>
              <button v-if="user_id && msg.sender.id == user_id" @click="openMessageDeleteModal(msg)" class="table-tab-button"> Удалить</button>
            </div>
          </div>
        </div>

        <div v-if="showMessageDeleteModal" class="modal-overlay">
          <div class="modal">
            <div class="modal-header">
              <h2 class="modal-header-h2">Удаление {{ selectedMessage.sender.str || 'Безымянный исполнитель очереди' }}</h2>
            </div>
            <div class="minibutton-group modal-menu">
              <button @click="confirmMessageDelete(selectedMessage.id)" class="minibutton">Подтвердить</button>
              <button @click="closeMessageDeleteModal" class="minibutton">Отменить</button>
            </div>
          </div>
        </div> 

        <div class="tab-pagination">
          <button 
            :disabled="messagesCurrentPage === 1" 
            @click="messagesCurrentPage--"
            class="tab-settings-button"
          >
            Назад
          </button>
          <span>Страница {{ messagesCurrentPage }} из {{ messagesTotalPages }}</span>
          <button 
            :disabled="messagesCurrentPage === messagesTotalPages" 
            @click="messagesCurrentPage++"
            class="tab-settings-button"
          >
            Вперед
          </button>
        </div>



      </div>

      <div v-else >
        <div class="none-border">Нет сообщений</div>
      </div>

    </div>

    <form @submit.prevent="sendMessage" class="form" id="form">
      <div class="form-field form-field-full_width">
        <label for="desc" class="form-label">Сообщение:</label>
        <EditorComponent ref="editorRef" v-model="form.newMessage"/>
        <span v-if="errors.newMessage" class="error">{{ errors.newMessage }}</span>
      </div>
    </form>

    <div class="tab-menu minibutton-group">
      <button type="submit" class="minibutton" form="form">Отправить</button> <!-- Кнопка отправки сообщения -->
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
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
  topic_id: Number,
});
console.log("Topic ID:", props.topic_id);
const user_id = ref(null);
const currentlyEditingMessageId = ref(null);

const getMessageClass = (msg) => {
  return msg.sender?.id === user_id.value ? 'message-sent' : 'message-received';
};

const form = reactive({
  newMessage: '', // Содержание нового сообщения
});


const editorRef = ref(null);

const messages = ref([]);
const loadMessages = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
  user_id.value = validToken.user_id;
  console.log('ID пользователя:', user_id.value);

  try {
    const response = await axios.get(`${baseUrl}/topics/${props.topic_id}/comments/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    messages.value = response.data || [];
    console.log('Все сообщения загружены:', messages.value);
    const totalPages = Math.ceil(messages.value.length / messagesItemsPerPage);
    messagesCurrentPage.value = totalPages > 0 ? totalPages : 1;

  } catch (error) {
    console.error('Ошибка при загрузке всех сообщений:', error.response ? error.response.data : error.message);
  }
};
const loadNewMessages = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) {
    router.push({ name: 'Login' });
    return;
  }

  const lastId = messages.value.length ? Math.max(...messages.value.map(m => m.id)) : 0;

  try {
    const response = await axios.get(`${baseUrl}/topics/${props.topic_id}/comments/`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { last_id: lastId },
    });
    if (response.data && response.data.length) {
      messages.value = messages.value.concat(response.data);
      console.log('Новые сообщения загружены:', response.data);
    } else {
      console.log('Новых сообщений нет');
    }
  } catch (error) {
    console.error('Ошибка при загрузке новых сообщений:', error.response ? error.response.data : error.message);
  }
};


const errors = reactive({});
const validateSendForm = () => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(form.newMessage || '', 'text/html');
  const textContent = doc.body.textContent?.trim();
  errors.newMessage = textContent ? '' : 'Содержание обязательно!';
  return Object.values(errors).every(error => !error);
};
const sendMessage = async () => {
  if (!validateSendForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    console.log('Отправляем данные для создания объекта:', form);
    const jsonData = {
      topic: props.topic_id,
      content: form.newMessage,
      sender: validToken.user_id,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.post(`${baseUrl}/comments/create/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Комментарий создан:', jsonResponse.data);
    editorRef.value.clearContent();
    loadNewMessages();

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании комментария:', error.response.data);
    } else {
      console.error('Ошибка при создании комментария:', error.message);
    }
  }
};


const startEditing = (msg) => {
  currentlyEditingMessageId.value = msg.id ;
  msg.editedContent = msg.content;
};
const validateEditForm = (msg) => {
  msg.editErrors = {};
  const parser = new DOMParser();
  const doc = parser.parseFromString(msg.editedContent || '', 'text/html');
  const textContent = doc.body.textContent?.trim();
  msg.editErrors.editedContent = textContent ? '' : 'Содержание обязательно!';
  return Object.values(msg.editErrors).every(error => !error);
};

const saveEdit = async (msg) => {

  if (!validateEditForm(msg)) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }
    console.log('Отправляем данные для редактирования комментария:', form);
    const jsonData = {
      topic: props.topic_id,
      content: msg.editedContent,
      sender: validToken.user_id,
    };
    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.patch(`${baseUrl}/comments/${msg.id}/update/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('Комментарий отредактирован:', jsonResponse.data);

    const found = messages.value.find(m => m.id === msg.id);
    if (found) {
      found.content = jsonResponse.data.content;
      found.changed = jsonResponse.data.changed;
    }
    console.log('Комментарий обновлен:', found);
    currentlyEditingMessageId.value = null;
    loadNewMessages();

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }

};

const showMessageDeleteModal = ref(false);
const selectedMessage = ref(null);
const openMessageDeleteModal = (msg) => {
  selectedMessage.value = msg;
  showMessageDeleteModal.value = true;
};
const closeMessageDeleteModal = () => {
  showMessageDeleteModal.value = false;
};

const confirmMessageDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
  try {
    await axios.delete(`${baseUrl}/comments/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    messages.value = messages.value.filter(msg => msg.id !== id);
    closeMessageDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления комментария:', error);
  }

};

const replyOnMessage = (msg) => {
  if (!editorRef.value) return;
  console.log("Ответ на сообщение:", msg); 
  editorRef.value.editor.chain().focus().toggleBlockquote().run();
  editorRef.value.insertContent(`${msg.sender.str} - ${formatDateTime(msg.created)}`);
  editorRef.value.insertContent(msg.content);
  editorRef.value.editor.chain().focus().splitBlock().run();
  editorRef.value.editor.chain().focus().setParagraph().run();
};

const messagesSearchQuery = ref('');
const messagesCurrentPage = ref(1);
const messagesItemsPerPage = 10;
const filteredMessages = computed(() => {
  if (!messagesSearchQuery.value) return messages.value;
  return messages.value.filter(msg => 
    msg.sender?.str?.toLowerCase().includes(messagesSearchQuery.value.toLowerCase()) ||
    msg.content?.toLowerCase().includes(messagesSearchQuery.value.toLowerCase())
  );
});
const messagesTotalPages = computed(() => Math.ceil(filteredMessages.value.length / messagesItemsPerPage));
const paginatedMessages = computed(() => {
  const start = (messagesCurrentPage.value - 1) * messagesItemsPerPage;
  const end = start + messagesItemsPerPage;
  return filteredMessages.value.slice(start, end);
});
watch(messagesSearchQuery, () => {
  messagesCurrentPage.value = 1;
});

const isTypingNewMessage = ref(null)

watch(() => form.newMessage, (newVal) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(newVal, 'text/html');
  const textContent = doc.body.textContent?.trim();
  isTypingNewMessage.value = !!textContent;
});

let intervalId = null;
const startAutoReload = () => {
  intervalId = setInterval(() => {
    if (!currentlyEditingMessageId.value && !isTypingNewMessage.value) {
      loadNewMessages();
      console.log('Запрос на обновление сообщений отправлен:', new Date().toLocaleTimeString());
    } else {
      console.log('Пропуск автообновления (редактирование или набор нового сообщения)');
    }
  }, 10000);
};

const stopAutoReload = () => {
  if (intervalId) clearInterval(intervalId);
}

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  await loadMessages();
  loading.value = true;
  startAutoReload();
});

onBeforeUnmount(() => {
  stopAutoReload();
});

</script>

<style scoped>
</style>
