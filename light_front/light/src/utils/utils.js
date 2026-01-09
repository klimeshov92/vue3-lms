import { ref } from 'vue';

export const auth_user_id = ref(localStorage.getItem('auth_user_id') || null);
export function setUserId(id) {
  auth_user_id.value = id;
  localStorage.setItem('auth_user_id', id);
}
export function clearUserId() {
  auth_user_id.value = null;
  localStorage.removeItem('auth_user_id');
}

//export const coreUrl = 'http://127.0.0.1:8000';
//export const baseUrl = 'http://127.0.0.1:8000/api';
//export const staticUrl = 'http://127.0.0.1:8000/static';
//export const mediaUrl = 'http://127.0.0.1:8000/media';
//export const frontendUrl = 'http://localhost:5173';

export const coreUrl = '';
export const baseUrl = '/api';
export const staticUrl = '/static';
export const mediaUrl = '/media';
export const frontendUrl = 'https://light-lms.ru';

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const formatDateTime = (dateTimeString) => {
  const date = new Date(dateTimeString);
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  });
};

export const isTokenValid = (token) => {
  try {
    if (!token) {
      console.log('Токен отсутствует');
      return null;
    }

    const parts = token.split('.');
    if (parts.length < 2) {
      //console.log('Токен имеет неправильную структуру (меньше двух частей)');
      return null;
    }
    
    //console.log('Токен разбит на части:', parts);

    const payload = atob(parts[1]);
    //console.log('Декодированный payload:', payload);

    const decoded = JSON.parse(payload);
    console.log('Расшифрованный объект токена:', decoded);
    console.log('ID пользователя в токене:', decoded.user_id);

    const expirationTime = decoded.exp * 1000;
    console.log('Время истечения токена:', new Date(expirationTime).toLocaleString());

    if (expirationTime > Date.now()) {
      //console.log('Токен валиден');
      return decoded;
    } else {
      console.log('Токен истек');
      return null;
    }
  } catch (error) {
    console.error('Ошибка при проверке токена:', error);
    return null;
  }
};
