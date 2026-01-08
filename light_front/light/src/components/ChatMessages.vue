
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
            <EditorComponent v-if="msg.isEditing" v-model="msg.editedContent" />
            <div v-else v-html="msg.content" class="tiptap"></div>
            <div>
              <p>
                {{ msg.changed ? formatDateTime(msg.changed) : 'Без даты и времени' }}
              </p>
            </div>
          </div>
          <div class="chat-menu-outer">
            <div class="chat-menu-inner">
              <button class="table-tab-button" v-if="!msg.isEditing" @click="replyOnMessage(msg)">Ответить</button>
              <button class="table-tab-button" v-if="!msg.isEditing && user_id && msg.sender.id == user_id" @click="startEditing(msg)">Редактировать</button>
              <button class="table-tab-button" v-if="msg.isEditing" @click="saveEdit(msg)">Сохранить</button>
              <button v-if="user_id && msg.sender.id == user_id" @click="openMessageDeleteModal(msg)" class="table-tab-button"> Удалить</button>
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
        <EditorComponent ref="editorRef" v-model="form.newMessage"/> <!-- Редактор сообщения -->
        <span v-if="errors.newMessage" class="error">{{ errors.newMessage }}</span> <!-- Ошибка, если сообщение не заполнено -->
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
  chat_id: Number,
});
console.log("Chat ID:", props.chat_id);
const user_id = ref(null); 

const messages = ref([]);
const getMessageClass = (msg) => {
  return msg.sender?.id === user_id.value ? 'message-sent' : 'message-received';
};

const form = reactive({
  newMessage: '', // Содержание нового сообщения
});

const editorRef = ref(null);
let socket = null;

// Функция для подключения к WebSocket
const connectWebSocket = () => {
  if (socket && socket.readyState !== WebSocket.CLOSED) return;

  const roomName = props.chat_id;
  
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);

  if (token && !validToken) {
    router.push({ name: 'Login' });
  } else {
    user_id.value = validToken.user_id;
    console.log('ID пользователя:', user_id.value);
  }

  const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws/chat_rooms/${roomName}/?token=${token}`;// URL WebSocket

  socket = new WebSocket(wsUrl); // Подключаем WebSocket

  // Обработчик при открытии соединения
  socket.onopen = () => {
    console.log("WebSocket подключен");
    requestOldMessages();
  };

  // Обработчик при получении сообщения
  socket.onmessage = (event) => {
    handleIncomingMessage(event);
  };

  // Обработчик ошибок
  socket.onerror = (error) => {
    console.error("WebSocket ошибка:", error); // Лог ошибки
    alert("Ошибка при подключении к чату. Пожалуйста, попробуйте позже."); // Сообщение об ошибке
  };

  // Обработчик закрытия соединения
  socket.onclose = () => {
    console.log("WebSocket отключен"); // Лог при закрытии соединения
  };
};

// Функция для обработки входящих сообщений.
const handleIncomingMessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    
    if (data.action === 'message_edited') {
      const msg = messages.value.find(m => m.id === data.message_id);
      if (msg) {
        msg.content = data.new_content;
        msg.changed = data.changed;
      }
    }

    if (data.action === 'message_deleted') {
      messages.value = messages.value.filter(m => m.id !== data.message_id);
      const totalPages = Math.ceil(messages.value.length / messagesItemsPerPage);
      messagesCurrentPage.value = totalPages > 0 ? totalPages : 1; // Устанавливаем последнюю страницу
    }

    if (data.old_messages) {
      console.log("Загруженные старые сообщения:", data.old_messages);
      messages.value = data.old_messages;
      const totalPages = Math.ceil(messages.value.length / messagesItemsPerPage);
      messagesCurrentPage.value = totalPages > 0 ? totalPages : 1; // Устанавливаем последнюю страницу
    }

    if (data.message) {
      messages.value.push({
        sender: data.sender,
        content: data.message,
        changed: data.changed
      });
      
    }

  } catch (error) {
    console.error("Ошибка при обработке сообщения WebSocket:", error);
  }
};

const errors = reactive({}); // Объект для ошибок формы
// Функция для валидации формы
const validateForm = () => {
  errors.newMessage = form.newMessage.trim() ? '' : 'Содержание обязательно!'; // Проверяем, что сообщение не пустое
  return Object.values(errors).every((error) => !error); // Проверяем, нет ли ошибок
};

const requestOldMessages = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ action: 'load_old_messages' }));
    }
};

// Функция для отправки сообщения
const sendMessage = () => {
  // Если сообщение невалидно, выводим ошибку и выходим
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors); // Лог ошибок
    return;
  }

  // Проверка состояния WebSocket
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    alert("Соединение с чатом потеряно. Пожалуйста, перезагрузите страницу."); // Сообщение о потере соединения
    return;
  }

  // Данные для отправки
  const messageData = { 
    action: 'send_message',
    message: form.newMessage, // Содержание сообщения
  };

  console.log("Отправляемое сообщение:", messageData); // Лог отправляемого сообщения

  // Отправляем сообщение через WebSocket
  socket.send(JSON.stringify(messageData)); 

  // Очищаем поле ввода и редактор после отправки
  editorRef.value.clearContent();
};


const startEditing = (msg) => {
  msg.isEditing = true;
  msg.editedContent = msg.content;
};
const saveEdit = (msg) => {
  if (!msg.editedContent.trim()) return;
  socket.send(JSON.stringify({
    action: 'edit_message',
    message_id: msg.id,
    new_content: msg.editedContent,
  }));
  msg.isEditing = false;
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
  socket.send(JSON.stringify({
    action: 'delete_message', 
    message_id: id, 
  }));
  closeMessageDeleteModal();
};

const replyOnMessage = (msg) => {
  if (!editorRef.value) return;
  console.log("Ответ на сообщение:", msg); 
  editorRef.value.editor.chain().focus().toggleBlockquote().run();
  editorRef.value.insertContent(`${msg.sender.str} - ${formatDateTime(msg.changed)}`);
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

// Монтируем компонент и подключаем WebSocket
onMounted(async () => {
  console.log('Компонент для чата смонтирован, начинаем подключение к WebSocket...');
  await connectWebSocket();
  loading.value = true;
});

// Закрываем WebSocket перед размонтированием компонента
onBeforeUnmount(() => {
  if (socket) {
    socket.close();  // Закрыть WebSocket перед размонтированием компонента
  }
});
</script>

<style scoped>
</style>
