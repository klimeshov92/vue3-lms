<template>
  <div v-if="loading">
    <div v-if="state.canPerform" class="detail-page">
      <div v-if="state.object.id">
        <div class="testing">



          <div class="testing-area">

            <div v-if="activeQuestionResult" class="question-area">
                
                <div v-if="activeQuestionResult.question?.picture" class="question-image-outer">
                  <div class="question-image-inner">
                    <img :src="activeQuestionResult.question.picture || '/default-avatar.png'" alt="Картинка" />
                  </div>
                </div>

                <div class="question-text">
                  <h1>{{activeQuestionResult.question.text}}</h1>
                </div>

                <div class="question-manual">
                  {{activeQuestionResult.question.manual}}
                </div>

                <div v-if="activeQuestionResult?.status == 'completed'" class="feedback_for_correct">
                    {{activeQuestionResult.question.feedback_for_correct}}
                </div>

                <div v-if="activeQuestionResult?.status == 'failed'" class="feedback_for_incorrect">
                    {{activeQuestionResult.question.feedback_for_incorrect}}
                </div>

                <div v-if="activeQuestionResult.question.question_type === 'single_selection'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <label class="answer-field">
                      <input
                        type="radio"
                        class="answer-input"
                        :name="'single_'+activeQuestionResult.id"
                        :value="answer_result.id"
                        v-model="activeQuestionResultForm.selectedAnswerId"
                        :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                      />
                      <span>{{ answer_result.answer.text }}</span>
                    </label>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>

                </div>

                <div v-if="activeQuestionResult.question.question_type === 'multiple_choice'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <label class="answer-field">
                      <input
                        class="answer-input"
                        type="checkbox"
                        v-model="activeQuestionResultForm[answer_result.id]"
                        :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                      />
                      <span>{{ answer_result.answer.text }}</span>
                    </label>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>
                </div>

                <div v-if="activeQuestionResult.question.question_type === 'sorting'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <div>{{ answer_result.answer.text }}</div>
                    <label>
                        <input
                          class="answer-input"
                          type="number"
                          placeholder="Введите правильный порядок"
                          v-model="activeQuestionResultForm[answer_result.id]"
                          :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                        />
                    </label>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>
                </div>

                <div v-if="activeQuestionResult.question.question_type === 'compliance'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <label>{{ answer_result.answer.text }}</label>
                    <multiselect
                      v-model="activeQuestionResultForm[answer_result.id]"
                      :options="relevant_points"
                      :multiple="false"
                      :close-on-select="true"
                      :clear-on-select="false"
                      :preserve-search="true"
                      placeholder="Выберите план"
                      label="text"
                      track-by="id"
                      :preselect-first="false"
                      :select-label="``"
                      :deselect-label="``"
                      :selected-label="``"
                      :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                    >
                      <template #noOptions>
                        <span>Список пуст</span>
                      </template>
                      <template #noResult>
                        <span>Ничего не найдено</span>
                      </template>
                    </multiselect>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>
                </div>

                <div v-if="activeQuestionResult.question.question_type === 'text_input'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <div>{{ answer_result.answer.text }}</div>
                    <label>
                      <input
                        class="answer-input"
                        type="text"
                        placeholder="Введите правильный ответ"
                        v-model="activeQuestionResultForm[answer_result.id]"
                        :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                      />
                    </label>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>
                </div>

                <div v-if="activeQuestionResult.question.question_type === 'numeric_input'" class="answers">
                  <div v-for="answer_result in activeQuestionResult.answer_results" :key="answer_result.id" class="answer">
                    <div v-if="answer_result.answer?.picture" class="answer-image-outer">
                      <div class="answer-image-inner">
                        <img :src="answer_result.answer.picture || '/default-avatar.png'" alt="Картинка" />
                      </div>
                    </div>
                    <div>{{ answer_result.answer.text }}</div>
                    <label>
                        <input
                          class="answer-input"
                          type="number"
                          placeholder="Введите правильный ответ"
                          v-model="activeQuestionResultForm[answer_result.id]"
                          :disabled="activeQuestionResult.status == 'completed' || activeQuestionResult.status == 'failed'"
                        />
                    </label>
                    <div v-if="answer_result.status == 'completed'" class="feedback_for_correct">
                        {{answer_result.answer.feedback_for_correct}}
                    </div>
                    <div v-if="answer_result.status == 'failed'" class="feedback_for_incorrect">
                        {{answer_result.answer.feedback_for_incorrect}}
                    </div>
                  </div>
                </div>

                <div class="question-index">Вопрос {{ activeQuestionIndex + 1 }} из {{ state.object.question_results.length }}</div>

                <div class="question-menu">
                  <button type="button" @click="goToPreviousQuestion" :disabled="activeQuestionIndex === 0" class="test-nav-button">
                    Назад
                  </button>

                  <button
                    v-if="activeQuestionResult.status != 'completed' && activeQuestionResult.status != 'failed'"
                    type="button"
                    @click="sendAnswers"
                    class="button"
                    
                  >
                    Ответить
                  </button>
                  
                  <button type="button" @click="goToNextQuestion" :disabled="activeQuestionIndex === state.object.question_results.length - 1" class="test-nav-button">
                    Далее
                  </button>
                </div>

            </div>

            <div class="test-info-area">

              <div class="test-info-container">

                <div class="test-header"> 
                  <h2>Выполнение теста "{{state.object.test_name}}"</h2>
                </div>

                <div class="test-manual">
                  <span>Ответье на вопрсоы теста за отведенное время</span>
                </div>

                <div class="test-info-text">
                  <div class="test-info-text-elem">
                    <span class="test-info-text-label">Номер попытки:</span> {{ state.object.number ? state.object.number : 'Нет номера попытки' }} из {{ state.object.test_attempts ? state.object.test_attempts : 'Нет числа попыток' }}
                  </div>
                  <div class="test-info-text-elem">
                    <span class="test-info-text-label">Статус попытки:</span> {{ state.object.status_display ? state.object.status_display : 'Нет статуса' }}
                  </div>
                  <div v-if="countdown_minutes && countdown_seconds && !state.object?.end_time" class="test-info-text-elem countdown-timer">
                    <span class="test-info-text-label">Время попытки:</span> {{ countdown_minutes }} : {{ countdown_seconds }}
                  </div>
                  <div v-else class="test-info-text-elem countdown-timer">
                    <span class="test-info-text-label">Попытка завершена:</span> {{ state.object.test_result.end_time ? formatDateTime(state.object.test_result.end_time) : 'Нет данных' }}
                  </div>
                </div>

              </div>

                <div v-if="(state.object.status == 'completed' || state.object.status == 'failed') && !state.object.test_result.finished" class="test-info-menu button-group">

                  <button 
                    type="button"
                    @click="restart()"
                    class="button"
                  >
                    Начать заново
                  </button>
                  
                </div>

              <div class="test-info-container test-info-container-gray-light">

                <div v-if="state.object.question_results.length !== 0" class="test-info-table-outer">
                  <div class="test-info-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Вопрос</th>
                              <th>Статус</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="question_result in paginatedQuestionResults" :key="question_result.id">

                          <td>{{ question_result.question.text ? question_result.question.text : '-' }}</td>
                          <td>{{ question_result.status_display ? question_result.status_display : '-' }}</td>

                          <td>
                            <div class="test-info-table-menu">
                              <button type="button" @click="selectQuestion(question_result)" class="test-info-button">
                                Открыть
                              </button>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div v-else >
                  <div class="none-border-mini">Нет вопросов теста</div>
                </div>
                <div class="tab-pagination">
                  <button 
                    :disabled="questionResultsCurrentPage === 1" 
                    @click="questionResultsCurrentPage--"
                    class="tab-settings-button"
                  >
                    Назад
                  </button>
                  <span>Страница {{ questionResultsCurrentPage }} из {{ questionResultsTotalPages }}</span>
                  <button 
                    :disabled="questionResultsCurrentPage === questionResultsTotalPages" 
                    @click="questionResultsCurrentPage++"
                    class="tab-settings-button"
                  >
                    Вперед
                  </button>
                </div>

              </div>

            </div>

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
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils'; 
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';

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

const questionResultsCurrentPage = ref(1);
const questionResultsItemsPerPage = 10;

const attemptOpen = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/test_attempt_open/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные открытой попытки:', response.data); 
    state.object = response.data;
    const totalPages = Math.ceil(state.object.question_results.length / questionResultsItemsPerPage);
    questionResultsCurrentPage.value = totalPages > 0 ? totalPages : 1;
  } catch (error) {
    console.error('Ошибка при получении данных попытки:', error);
  }
};

const attemptCreate = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
 
  try {
    const response = await axios.post(`${baseUrl}/test_attempt_create/${id}/`, {}, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные созданной попытки:', response.data); 
    state.object = response.data;
    const totalPages = Math.ceil(state.object.question_results.length / questionResultsItemsPerPage);
    questionResultsCurrentPage.value = totalPages > 0 ? totalPages : 1;
  } catch (error) {
    console.error('Ошибка при получении данных попытки:', error);
  }
};

const questionResultsTotalPages = computed(() => Math.ceil(state.object.question_results.length / questionResultsItemsPerPage));
const paginatedQuestionResults = computed(() => {
  const start = (questionResultsCurrentPage.value - 1) * questionResultsItemsPerPage;
  const end = start + questionResultsItemsPerPage;
  return state.object.question_results.slice(start, end);
});

const countdown_minutes = ref('');
const countdown_seconds = ref('');
let timerInterval = null;

const startCountdown = async () => {
  if (!state.object?.plan_end_time) return;

  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }

  countdown_minutes.value = '';
  countdown_seconds.value = '';

  console.log('Старт таймера'); 
  const endTime = new Date(state.object.plan_end_time).getTime();
  timerInterval = setInterval(() => {
    const now = new Date().getTime();
    const diff = endTime - now;

    if (diff <= 0) {
      clearInterval(timerInterval);
      console.log('⏰ Время вышло!');
      testFinish(); 
      return;
    }

    const minutes = String(Math.floor(diff / (1000 * 60))).padStart(2, '0');
    const seconds = String(Math.floor((diff % (1000 * 60)) / 1000)).padStart(2, '0');

    countdown_minutes.value = `${minutes}`;
    countdown_seconds.value = `${seconds}`;
  }, 1000);

};

const activeQuestionResult = ref(null);

const fetchFirstQuestionResult = async () => {
  const questionResults = state.object.question_results || [];
  console.log('Результаты вопросов:',questionResults);

  let firstQuestionResult = questionResults.find(
    question_result => question_result.status !== 'completed' && question_result.status !== 'failed'
  );
  console.log('Первый незавершенный вопрос:',questionResults);

  if (!firstQuestionResult && questionResults.length) {
    firstQuestionResult = questionResults[0];
    console.log('Первый вопрос по порядку:',questionResults);
  }

  activeQuestionResult.value = firstQuestionResult || null;
  if (firstQuestionResult) {
    console.log('Выбран текущий вопрос:', firstQuestionResult);
    startActiveQuestionResultForm(firstQuestionResult);
  }
};

const setActiveQuestionResult = (question_result) => {
  activeQuestionResult.value = question_result;
  startActiveQuestionResultForm(question_result);
  console.log('Выбран текущий вопрос:', activeQuestionResult.value);
};

const activeQuestionResultForm = reactive({});

const relevant_points = ref([])

const startActiveQuestionResultForm = (questionResult) => {
  for (const key in activeQuestionResultForm) {
    delete activeQuestionResultForm[key];
  }

  if (questionResult.question.question_type === 'single_selection') {
    const selectedAnswer = questionResult.answer_results.find(answer_result => answer_result.selected_answer);
    activeQuestionResultForm.selectedAnswerId = selectedAnswer ? selectedAnswer.id : null;
  } else if (questionResult.question.question_type === 'multiple_choice') {
    questionResult.answer_results.forEach(answer_result => {
      activeQuestionResultForm[answer_result.id] = answer_result.selected_answer || false;
    });
  } else if (questionResult.question.question_type === 'sorting') {
    questionResult.answer_results.forEach(answer_result => {
      activeQuestionResultForm[answer_result.id] = answer_result.selected_position || 0;
    });
  } else if (questionResult.question.question_type === 'text_input') {
    questionResult.answer_results.forEach(answer_result => {
      activeQuestionResultForm[answer_result.id] = answer_result.selected_text_input || '';
    });
  } else if (questionResult.question.question_type === 'numeric_input') {
    questionResult.answer_results.forEach(answer_result => {
      activeQuestionResultForm[answer_result.id] = answer_result.selected_numeric_input || 0;
    });
  } else if (questionResult.question.question_type === 'compliance') {
    const rawRelevantPoints = questionResult.question.answers
      .map(answer => answer.relevant_point)
      .filter(Boolean);
    console.log('Создан список всех соотвествующих пунктов:', rawRelevantPoints);

    const uniqueRelevantPoints = Array.from(
      new Map(rawRelevantPoints.map(p => [p.id, p])).values()
    );
    console.log('Создан список соотвествующих пунктов:', uniqueRelevantPoints);

    relevant_points.value = uniqueRelevantPoints;
    console.log('Получено значение соотвествующих пунктов:', relevant_points.value );

    questionResult.answer_results.forEach(answer_result => {
      activeQuestionResultForm[answer_result.id] = relevant_points.value.find(relevant_point => relevant_point.id === answer_result.selected_relevant_point) || null;
    });

  }
  console.log('Создана форма:', activeQuestionResultForm);
};

const activeQuestionIndex = ref(0);

watch(activeQuestionResult, () => {
  if (!activeQuestionResult.value) return;
  const index = state.object.question_results.findIndex(q => q.id === activeQuestionResult.value.id);
  if (index !== -1) activeQuestionIndex.value = index;
});

const goToNextQuestion = () => {
  const nextIndex = activeQuestionIndex.value + 1;
  if (nextIndex < state.object.question_results.length) {
    setActiveQuestionResult(state.object.question_results[nextIndex]);
  }
  console.log('Следующий вопрос:', state.object.question_results[nextIndex]);
};

const goToPreviousQuestion = () => {
  const prevIndex = activeQuestionIndex.value - 1;
  if (prevIndex >= 0) {
    setActiveQuestionResult(state.object.question_results[prevIndex]);
  }
  console.log('Предидущий вопрос:', state.object.question_results[prevIndex]);
};

const selectQuestion = (question_result) => {
  setActiveQuestionResult(question_result);
  console.log('Выбранный вопрос:', question_result);
};

const back = () => {
  router.back();
};


const sendAnswers = async () => {

  if (!activeQuestionResult.value) return;

  try {

    const id = activeQuestionResult.value.id;
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    let jsonData = {};

    if (activeQuestionResult.value.question.question_type === 'single_selection') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_answer: activeQuestionResultForm.selectedAnswerId == answer_result.id, 
        })),
      };
      
    } else if (activeQuestionResult.value.question.question_type === 'multiple_choice') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_answer: !!activeQuestionResultForm[answer_result.id],
        })),
      };
      
    } else if (activeQuestionResult.value.question.question_type === 'sorting') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_position: activeQuestionResultForm[answer_result.id],
        })),
      };
    } else if (activeQuestionResult.value.question.question_type === 'text_input') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_text_input: activeQuestionResultForm[answer_result.id],
        })),
      };
    } else if (activeQuestionResult.value.question.question_type === 'numeric_input') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_numeric_input: activeQuestionResultForm[answer_result.id],
        })),
      };
    } else if (activeQuestionResult.value.question.question_type === 'compliance') {
      jsonData = {
        answer_results: activeQuestionResult.value.answer_results.map(answer_result => ({
          id: answer_result.id,
          selected_relevant_point: activeQuestionResultForm[answer_result.id].id,
        })),
      };
    }

    console.log('JSON данные перед отправкой:', jsonData);
    

    const jsonResponse = await axios.patch(`${baseUrl}/send_answers/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    if (jsonResponse.data.type === 'question_result') {
      const question_result = jsonResponse.data.data;
      const question_result_id = state.object.question_results.findIndex(q => q.id === question_result.id);
      if (question_result_id !== -1) {
        state.object.question_results.splice(question_result_id, 1, question_result);
      }
      if (activeQuestionResult.value.id === question_result.id) {
        setActiveQuestionResult(question_result);
      }

    } else if (jsonResponse.data.type === 'test_attempt') {
      const fullAttempt = jsonResponse.data.data;
      Object.assign(state.object, fullAttempt);
      const question_result = fullAttempt.question_results.find(q => q.id === activeQuestionResult.value.id);
      setActiveQuestionResult(question_result);
    }

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при сохранении изменений:', error.response.data);
    } else {
      console.error('Ошибка при сохранении изменений:', error.message);
    }
  }
};

const testFinish = async () => {

  if (!state.object) return;

  try {

    const id = state.object.id;
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/test_finish/${id}/`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Тест завершен:', jsonResponse.data);

    const fullAttempt = jsonResponse.data.data;
    Object.assign(state.object, fullAttempt);
    const question_result = fullAttempt.question_results.find(q => q.id === activeQuestionResult.value.id);
    setActiveQuestionResult(question_result);

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при сохранении изменений:', error.response.data);
    } else {
      console.error('Ошибка при сохранении изменений:', error.message);
    }
  }
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

    const id = route.params.id;
    console.log('ID объекта:', id);

     state.canPerform = true


  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const restart = async () => {
  await attemptCreate();
  await startCountdown();
  await fetchFirstQuestionResult();
}

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await attemptOpen();
    await fetchFirstQuestionResult();
    await startCountdown();
    await checkPermissionsVersion();
    await loadUserPermissions();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval);
});

</script>

<style scoped>

</style>
