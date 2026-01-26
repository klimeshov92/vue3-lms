<template>
  <div v-if="loading">
    <div v-if="state.canViewTask" class="detail-page">
      <div v-if="state.object.id">
        <div class="detail-card"> 
          <div class="detail-card-info">
            <div class="detail-header"> 
              <div class="detail-header-title">
                <h1>{{ state.object.name || 'Безымянная задача' }}</h1>
              </div>
            </div>
            <div class="detail-card-text">
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Статус:</span> {{ state.object.result ? state.object.result.status_display : 'Нет статуса' }}
              </div>
              <div v-if="state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Итог:</span> {{ state.object.result?.outcome ? state.object.result.outcome.str : 'Нет итога' }}
              </div>
              <div v-if="state.object.result?.start_time" class="detail-card-text-elem">
                <span class="detail-card-text-label">Начало:</span> {{ state.object.result?.start_time ? formatDateTime(state.object.result.start_time) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.result?.end_time" class="detail-card-text-elem">
                <span class="detail-card-text-label">Завершение:</span> {{ state.object.result?.end_time ? formatDateTime(state.object.result.end_time) : 'Нет данных о завершении' }}
              </div>
              <div v-if="state.object.is_child" class="detail-card-text-elem">
                <span class="detail-card-text-label">План:</span> {{ state.object.plan ? state.object.plan.name : 'Нет плана' }}
              </div>
              <div v-if="state.object.is_child" class="detail-card-text-elem">
                <span class="detail-card-text-label">Пункт:</span> {{ state.object.item|| 'Нет пункта' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Тип задачи:</span> {{ state.object.task_type_display || 'Нет типа задачи' }}
              </div>
              <div v-if="state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Требуется проверка:</span> {{ state.object.require_review ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Итог задачи:</span> {{ state.object.task_outcome ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.task_type == 'news_reading'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Новость:</span> {{ state.object.new.str || 'Нет новости' }}
              </div>
              <div v-if="state.object.task_type == 'material_review'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Материал:</span> {{ state.object.material.str || 'Нет материала' }}
              </div>
              <div v-if="state.object.task_type == 'course_study'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Курс:</span> {{ state.object.course.str || 'Нет курса' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Тест:</span> {{ state.object.test.str || 'Нет теста' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Проходной балл:</span> {{ state.object.test.passing_score|| 'Нет проходного балла' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Время на выполнение (минут):</span> {{ state.object.test.time_to_complete|| 'Нет времени на выполнение' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Попытки:</span> {{ state.object.test.attempts|| 'Нет попыток' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Мероприятие:</span> {{ state.object.event_template.str || 'Нет мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Слот мероприятия:</span> {{ state.object.event_slot?.str || 'Нет выбранного слота мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation' && ( state.object.event_template?.format == 'face_to_face' || state.object.event_template?.format == 'mixed') " class="detail-card-text-elem">
                <span class="detail-card-text-label">Локация:</span> {{ state.object.event_template.location || 'Нет локации' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation' && ( state.object.event_template?.format == 'webinar' || state.object.event_template?.format == 'mixed') " class="detail-card-text-elem">
                <span class="detail-card-text-label">Ссылка:</span> {{ state.object.event_template.link || 'Нет ссылки' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Ведущие:</span>
                {{ state.object.event_template?.admins?.length > 0 ? state.object.event_template?.admins.map(admin => admin.str).join(', ') : 'Нет ведущих' }}
              </div> 
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Начало по плану:</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.deadline" class="detail-card-text-elem">
                <span class="detail-card-text-label">Завершение по плану:</span> {{ state.object.planned_end ? formatDateTime(state.object.planned_end) : 'Нет данных о завершении' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Исполнитель:</span> {{ state.object.executor ? state.object.executor.str : 'Нет исполнителя' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Соисполнители:</span>
                {{ state.object.co_executor_group && state.object.co_executor_group.user_set.length > 0 ? state.object.co_executor_group.user_set.map(item => item.str).join(', ') : 'Нет соисполнителей' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Контролеры:</span>
                {{ state.object.controller_group && state.object.controller_group.user_set.length > 0 ? state.object.controller_group.user_set.map(item => item.str).join(', ') : 'Нет контролеров' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Наблюдатели:</span>
                {{ state.object.observer_group && state.object.observer_group.user_set.length > 0 ? state.object.observer_group.user_set.map(item => item.str).join(', ') : 'Нет наблюдателей' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Взаимодействие:</span> {{ state.object.interaction ? state.object.interaction.str : 'Нет взаимодействия' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
            </div>

            <div class="manual">
              <div v-html="state.object.manual" class="tiptap close" :class="{ expanded: isExpanded }"></div>
              <div v-if="state.object.manual.length > 150" class="expand-container">
                <button class="expand-button" @click="isExpanded = !isExpanded">
                  {{ isExpanded ? 'Свернуть' : 'Развернуть' }}
                </button>
              </div>
            </div>
            <div class="detail-menu button-group">

              <router-link
                v-if="state.object?.task_type == 'common_task' && state.canPerform" 
                :to="{ name: 'TaskResultUpdate', params: { id: state.object.id } }"
                class="button"
              >
                Выполнить
              </router-link>

              <router-link
                v-if="state.object?.task_type == 'plan_implementation' && state.canPerform" 
                :to="{ name: 'PlanResultUpdate', params: { id: state.object.id } }"
                class="button"
              >
                Выполнить
              </router-link>

              <router-link
                v-if="state.object?.task_type == 'news_reading' && state.canPerform" 
                :to="{ name: 'NewContent', params: { id: state.object.id } }"
                class="button"
              >
                Ознакомиться
              </router-link>

              <router-link
                v-if="state.object?.task_type == 'material_review' && state.canPerform" 
                :to="{ name: 'MaterialContent', params: { id: state.object.id } }"
                class="button"
              >
                Ознакомиться
              </router-link>

              <router-link
                v-if="state.object?.task_type == 'course_study' && state.canPerform"
                :to="{ name: 'ScormContent', params: { id: state.object.id } }"
                target="_blank"
                rel="noopener noreferrer"
                class="button"
              >
                Пройти
              </router-link>

              <router-link
                v-if="state.object?.task_type == 'test_taking' && state.canPerform" 
                :to="{ name: 'TestAttempt', params: { id: state.object.id } }"
                class="button"
              >
                Пройти
              </router-link>

              <a
                v-if="state.object?.task_type == 'event_participation' && state.canPerform && state.object.event_slot && state.object.event_template?.link"
                :href="state.object.event_template.link"
                target="_blank"
                rel="noopener noreferrer"
                class="button"
              >
                Открыть слот
              </a>

              <router-link
                v-if="state.object?.task_type == 'event_participation' && state.canPerform && state.object.slot_select && !state.object.event_slot"
                :to="{ name: 'EventSlotSelect', params: { id: state.object.id } }"
                class="button"
              >
                Выбрать слот
              </router-link>

              <button 
                v-if="state.object?.task_type == 'event_participation' && state.canPerform && state.object.event_slot" 
                @click="confirmParticipation"
                class="button"
              >
                {{ state.object.result.confirmed ? 'Отменить участие' : 'Подтвердить участие' }} 
              </button>

              <router-link
                v-if="state.object?.task_type == 'event_participation' && state.canPerform && state.object.slot_select && state.object.event_slot"
                :to="{ name: 'EventSlotSelect', params: { id: state.object.id } }"
                class="button"
              >
                Изменить слот
              </router-link>

              <router-link 
                v-if="state.canEditTask" 
                :to="{ name: 'TaskEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
               
              <button 
                v-if="state.canDeleteTask" 
                @click="openTaskDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>

            </div>

            <div v-if="showTaskDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный задача' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmTaskDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeTaskDeleteModal" class="minibutton">Отменить</button>
                </div>
              </div>
            </div>

          </div>
        </div>


        <div class="detail-tabs">
          <div class="tabs-header">
            <button 
              v-for="tab in tabs" 
              :key="tab.name" 
              :class="{ active: activeTab === tab.name }"
              @click="activeTab = tab.name"
              class="tab-button"
            >
              {{ tab.label }}
            </button>
          </div>

          <div v-if="activeTab" class="tabs-content">

            <div v-if="activeTab === 'desc'" class="desc-tab">
              <div v-if="state.object.desc">
                {{ state.object.desc }}
              </div>
              <div v-else>
                <div class="none-border">Описание отсуствует</div>
              </div>
            </div>

            <div v-if="activeTab === 'details'" class="detail-tab">
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Статус:</span> {{ state.object.result?.status_display ? state.object.result.status_display : 'Нет статуса' }}
              </div>
              <div v-if="state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation'" class="detail-tab-elem">
                <span class="detail-tab-label">Итог:</span> {{ state.object.result?.outcome ? state.object.result.outcome.str : 'Нет итога' }}
              </div>
              <div v-if="state.object.result?.start_time" class="detail-tab-elem">
                <span class="detail-tab-label">Начало:</span> {{ state.object.result?.start_time ? formatDateTime(state.object.result.start_time) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.result?.end_time" class="detail-tab-elem">
                <span class="detail-card-text-label">Завершение:</span> {{ state.object.result?.end_time ? formatDateTime(state.object.result.end_time) : 'Нет данных о завершении' }}
              </div>
              <div v-if="state.object.is_child" class="detail-tab-elem">
                <span class="detail-tab-label">План:</span> {{ state.object.plan ? state.object.plan.name : 'Нет плана' }}
              </div>
              <div v-if="state.object.is_child" class="detail-tab-elem">
                <span class="detail-tab-label">Пункт:</span> {{ state.object.item|| 'Нет пункта' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Тип задачи:</span> {{ state.object.task_type_display || 'Нет типа задачи' }}
              </div>
              <div v-if="state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation'" class="detail-tab-elem">
                <span class="detail-tab-label">Требуется проверка:</span> {{ state.object.require_review ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Итог задачи:</span> {{ state.object.task_outcome ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.task_type == 'news_reading'" class="detail-tab-elem">
                <span class="detail-tab-label">Новость:</span> {{ state.object.new.str || 'Нет новости' }}
              </div>
              <div v-if="state.object.task_type == 'material_review'" class="detail-tab-elem">
                <span class="detail-tab-label">Материал:</span> {{ state.object.material.str || 'Нет материала' }}
              </div>
              <div v-if="state.object.task_type == 'course_study'" class="detail-tab-elem">
                <span class="detail-tab-label">Курс:</span> {{ state.object.course.str || 'Нет курса' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-tab-elem">
                <span class="detail-tab-label">Тест:</span> {{ state.object.test.str || 'Нет теста' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-tab-elem">
                <span class="detail-tab-label">Проходной балл:</span> {{ state.object.test.passing_score|| 'Нет проходного балла' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-tab-elem">
                <span class="detail-tab-label">Время на выполнение (минут):</span> {{ state.object.test.time_to_complete|| 'Нет времени на выполнение' }}
              </div>
              <div v-if="state.object.task_type == 'test_taking'" class="detail-tab-elem">
                <span class="detail-tab-label">Попытки:</span> {{ state.object.test.attempts|| 'Нет попыток' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-tab-elem">
                <span class="detail-tab-label">Мероприятие:</span> {{ state.object.event_template.str || 'Нет мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-tab-elem">
                <span class="detail-tab-label">Слот мероприятия:</span> {{ state.object.event_slot.str || 'Нет выбранного слота мероприятия' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation' && ( state.object.event_template?.format == 'face_to_face' || state.object.event_template?.format == 'mixed') " class="detail-tab-elem">
                <span class="detail-tab-label">Локация:</span> {{ state.object.event_template.location || 'Нет локации' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation' && ( state.object.event_template?.format == 'webinar' || state.object.event_template?.format == 'mixed') " class="detail-tab-elem">
                <span class="detail-tab-label">Ссылка:</span> {{ state.object.event_template.link || 'Нет ссылки' }}
              </div>
              <div v-if="state.object.task_type == 'event_participation'" class="detail-tab-elem">
                <span class="detail-tab-label">Ведущие:</span>
                {{ state.object.event_template?.admins?.length > 0 ? state.object.event_template?.admins.map(admin => admin.str).join(', ') : 'Нет ведущих' }}
              </div> 
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Сроки:</span> {{ state.object.deadline ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Начало по плану:</span> {{ state.object.planned_start ? formatDateTime(state.object.planned_start) : 'Нет данных о начале' }}
              </div>
              <div v-if="state.object.deadline" class="detail-tab-elem">
                <span class="detail-tab-label">Завершение по плану:</span> {{ state.object.planned_end ? formatDateTime(state.object.planned_end) : 'Нет данных о завершении' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Ожидает активации:</span> {{ state.object.waiting ? 'Да' : 'Нет' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Исполнитель:</span> {{ state.object.executor ? state.object.executor.str : 'Нет исполнителя' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Соисполнители:</span>
                {{ state.object.co_executor_group && state.object.co_executor_group.user_set.length > 0 ? state.object.co_executor_group.user_set.map(item => item.str).join(', ') : 'Нет соисполнителей' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Контролеры:</span>
                {{ state.object.controller_group && state.object.controller_group.user_set.length > 0 ? state.object.controller_group.user_set.map(item => item.str).join(', ') : 'Нет контролеров' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Наблюдатели:</span>
                {{ state.object.observer_group && state.object.observer_group.user_set.length > 0 ? state.object.observer_group.user_set.map(item => item.str).join(', ') : 'Нет наблюдателей' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Взаимодействие:</span> {{ state.object.interaction ? state.object.interaction.str : 'Нет взаимодействия' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Создан:</span> {{ state.object.created ? formatDateTime(state.object.created) : 'Нет данных о создании' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Создатель:</span> {{ state.object.creator ? state.object.creator : 'Нет создателя' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Изменён:</span> {{ state.object.changed ? formatDateTime(state.object.changed) : 'Нет данных об изменениях' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Редактор:</span> {{ state.object.editor ? state.object.editor : 'Нет редактора' }}
              </div>
            </div>

            <div v-if="activeTab === 'child_tasks'" class="table-tab">
              <div v-if="state.canViewTask">
                <div v-if="state.object.child_tasks && state.object.child_tasks.length > 0" class="table-tab-table-outer">
                  <div class="table-tab-table-inner">
                    <table>
                      <thead>
                          <tr>
                              <th>Пункт</th>
                              <th>Тип задачи</th>
                              <th>Название</th>
                              <th>Срок начала</th>
                              <th>Срок завершения</th>
                              <th>Исполнитель</th>
                              <th>
                                Действия
                              </th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="task in state.object.child_tasks" :key="task.id">
                          <td>{{ task.item ? task.item : '-' }}</td>
                          <td>{{ task.task_type_display ? task.task_type_display : '-' }}</td>
                          <td>{{ task.name ? task.name : '-' }}</td>
                          <td>{{ task.planned_start ? formatDate(task.planned_start) : '-' }}</td>
                          <td>{{ task.planned_end ? formatDate(task.planned_end) : '-' }}</td>
                          <td>{{ task.executor ? task.executor.str : 'Нет данных' }}</td>
                          <td>
                            <div v-if="state.canViewTaskGlobal || state.canViewTaskIds.includes(task.id)">
                              <div class="table-tab-menu">
                                <router-link 
                                  :to="{ name: 'TaskDetail', params: { id: task.id } }"
                                  class="table-tab-button"
                                >
                                  Открыть
                                </router-link>
                                <router-link 
                                  v-if="state.canEditTaskGlobal || state.canEditTaskIds.includes(task.id)" 
                                  :to="{ name: 'TaskEdit', params: { id: task.id }, query: { planId: state.object.id }  }"
                                  class="table-tab-button"
                                >
                                  Изменить
                                </router-link>
                                <button 
                                  v-if="state.canDeleteTaskGlobal || state.canDeleteTaskIds.includes(task.id)" 
                                  @click="openChildTaskDeleteModal(task)"
                                  class="table-tab-button"
                                >
                                  Удалить
                                </button>                           
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
                  <div v-if="showChildTaskDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedChildTask.str || 'Безымянная подзадача' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmChildTaskDelete(selectedChildTask.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeChildTaskDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div> 
                </div>
                <div v-else >
                  <div class="none-border">Нет подзадач</div>
                </div>
              </div>

              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>

              <div v-if="state.canAddTask" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canAddTask"
                  :to="{ name: 'TaskCreate', query: { planId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'messages'" class="topic-tab">
              
              <TopicMessages :topic_id="state.object?.topic.id" />

            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'task'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'task'" />

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
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid } from '../utils/utils'; 
import TaskResultUpdate from './TaskResultUpdate.vue';
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 
import TopicMessages from '../components/TopicMessages.vue';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const task_id = route.params.id;

const isExpanded = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canAddTask: false,
  canViewTaskGlobal: false,
  canViewTask: false,
  canViewTaskIds: [],
  canEditTask: false,
  canEditTaskGlobal: false,
  canEditTaskIds: [],
  canDeleteTask: false,
  canDeleteTaskGlobal: false,
  canDeleteTaskIds: [],
  canPerform: false,
  canViewTopic: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
});

function openScormInNewTab() {
  const url = router.resolve({ name: 'ScormContent', params: { id: state.object.id } }).href
  window.open(url, '_blank')
}

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
  }
 
  try {
    const response = await axios.get(`${baseUrl}/tasks/${id}/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    console.log('Данные задачи:', response.data); 
    state.object = response.data;
  } catch (error) {
    console.error('Ошибка при получении данных задачи:', error);
  }
};

const showTaskDeleteModal = ref(false);
const openTaskDeleteModal = () => {
  showTaskDeleteModal.value = true;
};
const closeTaskDeleteModal = () => {
  showTaskDeleteModal.value = false;
};
const confirmTaskDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/tasks/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeTaskDeleteModal();
    router.push({ name: 'TaskList' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
  }
};

const showChildTaskDeleteModal = ref(false);
const selectedChildTask = ref(null);
const openChildTaskDeleteModal = (task) => {
  selectedChildTask.value = task;
  showChildTaskDeleteModal.value = true;
};
const closeChildTaskDeleteModal = () => {
  showChildTaskDeleteModal.value = false;
};
const confirmChildTaskDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/tasks/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeChildTaskDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const confirmParticipation = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }
  const id = route.params.id;
  try {
    const response = await axios.patch(`${baseUrl}/confirm_participation/${id}/`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('Ответ об отметки об участии:', response.data);
    state.object.result.confirmed = response.data.confirmed;

  } catch (error) {
    console.error('При отметке об участии:', error);
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
    localStorage.removeItem('access_token');
    console.log('Токен удален из localStorage и очищен в переменной');
    token = null;
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

    state.canAddTask = state.globalPermissionsList.includes('bpms.add_task');
    console.log('Права на добавление задач:', state.canAddTask);

    state.canViewTask = state.globalPermissionsList.includes('bpms.view_task') ||
      (state.objectPermissionsDict['bpms.view_task'] &&
      state.objectPermissionsDict['bpms.view_task'].includes(Number(id)));
    console.log('Права на просмотр задачи:', state.canViewTask);

    state.canViewTaskGlobal = state.globalPermissionsList.includes('bpms.view_task');
    console.log('Глобальные права на просмотр задачи:', state.canViewTask);

    state.canViewTaskIds = (state.objectPermissionsDict['bpms.view_task'] || []).map(Number);
    if (!state.canViewTaskGlobal) {
      state.object.child_tasks = state.object.child_tasks.filter(child_task => state.canViewTaskIds.includes(child_task.id));
    }
    console.log('Доступные задачи:', state.object.child_tasks);

    state.canEditTask = state.globalPermissionsList.includes('bpms.change_task') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_task']) &&
      state.objectPermissionsDict['bpms.change_task'].includes(Number(id)));
    console.log('Права на редактирование задачи:', state.canEditTask);

    state.canEditTaskGlobal = state.globalPermissionsList.includes('bpms.change_task');

    state.canEditTaskIds = (state.objectPermissionsDict['bpms.change_task'] || []).map(Number);
    console.log('Доступные для изменения задачи:', state.canEditTaskIds);

    state.canDeleteTask = state.globalPermissionsList.includes('bpms.delete_task') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_task']) &&
      state.objectPermissionsDict['bpms.delete_task'].includes(Number(id)));
    console.log('Права на удаление задачи:', state.canDeleteTask);

    state.canDeleteTaskGlobal = state.globalPermissionsList.includes('bpms.delete_task');

    state.canDeleteTaskIds = (state.objectPermissionsDict['bpms.delete_task'] || []).map(Number);
    console.log('Доступные для удаления задачи:', state.canDeleteTaskIds);

    state.canViewAccountObjectPermission = state.globalPermissionsList.includes('core.view_account_object_permission');
    console.log('Права на просмотр объектных прав аккаунтов:', state.canViewAccountObjectPermission);

    state.canAddAccountObjectPermission = state.globalPermissionsList.includes('core.add_account_object_permission');
    console.log('Права на добавление объектных прав аккаунтов:', state.canAddAccountObjectPermission);

    state.canDeleteAccountObjectPermission = state.globalPermissionsList.includes('core.delete_account_object_permission');
    console.log('Права на удаление объектных прав аккаунтов:', state.canDeleteAccountObjectPermission);

    state.canViewAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.view_accounts_group_object_permission');
    console.log('Права на просмотр объектных прав групп:', state.canViewAccountsGroupObjectPermission);

    state.canAddAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.add_accounts_group_object_permission');
    console.log('Права на добавление объектных прав групп:', state.canAddAccountsGroupObjectPermission);

    state.canDeleteAccountsGroupObjectPermission = state.globalPermissionsList.includes('core.delete_accounts_group_object_permission');
    console.log('Права на удаление объектных прав групп:', state.canDeleteAccountsGroupObjectPermission);

    if (state.object.task_type == 'common_task' || state.object.task_type == 'plan_implementation') {
      state.canPerform = state.object.executor.id == validToken.user_id ||
      state.object.co_executors.some(user => user.id == validToken.user_id) ||
      state.object.controllers.some(user => user.id == validToken.user_id);
    }
    if (state.object.task_type == 'news_reading' 
      && (state.object.result.status !=  'failed' && state.object.result.status !=  'canceled') 
    ) {
      state.canPerform = state.object.executor.id == validToken.user_id
    }
    if (state.object.task_type == 'material_review' 
      && (state.object.result.status !=  'failed' && state.object.result.status !=  'canceled') 
    ) {
      state.canPerform = state.object.executor.id == validToken.user_id
    }
    if (state.object.task_type == 'course_study' 
      && (state.object.result.status !=  'failed' && state.object.result.status !=  'canceled') 
    ) {
      state.canPerform = state.object.executor.id == validToken.user_id
    }
    if (state.object.task_type == 'test_taking' 
      //&& (!state.object.result.finished) 
    ) {
      state.canPerform = state.object.executor.id == validToken.user_id
    }
    if (state.object.task_type == 'event_participation' 
      && (state.object.result.status !=  'failed' && state.object.result.status !=  'canceled') 
    ) {
      state.canPerform = state.object.executor.id == validToken.user_id
    }
    console.log('Редактирование результата:', state.canPerform);

    if (state.object.topic) {
      state.canViewTopic = state.globalPermissionsList.includes('comments.view_topic') ||
      (state.objectPermissionsDict['comments.view_topic'] && state.objectPermissionsDict['comments.view_topic'].includes(Number(state.object.topic.id)));
      console.log('Права на просмотр топика:', state.canViewTopic);
    }
    
  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  router.back();
};

const tabs = computed(() => [
  { name: 'desc', label: 'Описание' },
  { name: 'details', label: 'Детали' },
  state.canViewTopic ? { name: 'messages', label: 'Комментарии' } : null,
  state.object.task_type == 'plan_implementation' ? { name: 'child_tasks', label: 'Подзадачи' } : null,
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeTaskTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeTaskTab-${route.params.id}`, newTab);
  router.push({ query: { tab: newTab } });
  console.log('Загружен таб:', newTab);
});

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

watch(
  () => route.params.id,
  async (newId) => {
    console.log('Параметр id изменился на:', newId);
    await fetchObject();
  }
);

</script>

<style scoped>

</style>
