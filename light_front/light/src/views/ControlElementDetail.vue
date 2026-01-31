<template>
  <div v-if="loading">
    <div v-if="state.canViewControlElement" class="detail-page">
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
                <span class="detail-card-text-label">Тип работы:</span> {{ state.object.type_of_work_display || 'Нет типа работы' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Многократное срабатывание:</span> {{ state.object.repeat ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.type_of_work == 'task_outcome'" class="detail-card-text-elem">
                <span class="detail-card-text-label">Шаблон задачи:</span> {{ state.object.task_template ? state.object.task_template.str : 'Нет шаблона задачи' }}
              </div>
              <div class="detail-card-text-elem">
                <span class="detail-card-text-label">Категории:</span>
                {{ state.object.categories.length > 0 ? state.object.categories.map(category => category.name).join(', ') : 'Нет категорий' }}
              </div>

            </div>
            <div class="detail-menu button-group">
              <router-link 
                v-if="state.canEditControlElement" 
                :to="{ name: 'ControlElementEdit', params: { id: state.object.id } }"
                class="button"
              >
                Изменить
              </router-link>
              <button 
                v-if="state.canDeleteControlElement" 
                @click="openControlElementDeleteModal"
                class="button"
              >
                Удалить
              </button>

              <button type="button" @click="back" class="button">Назад</button>
            </div>
            <div v-if="showControlElementDeleteModal" class="modal-overlay">
              <div class="modal">
                <div class="modal-header">
                  <h2 class="modal-header-h2">Удаление {{ state.object.name || 'Безымянный задача' }}</h2>
                </div>
                <div class="minibutton-group modal-menu">
                  <button @click="confirmControlElementDelete()" class="minibutton">Подтвердить</button>
                  <button @click="closeControlElementDeleteModal" class="minibutton">Отменить</button>
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
                <span class="detail-tab-label">Тип работы:</span> {{ state.object.type_of_work_display || 'Нет типа работы' }}
              </div>
              <div class="detail-tab-elem">
                <span class="detail-tab-label">Многократное срабатывание:</span> {{ state.object.repeat ? 'Да' : 'Нет' }}
              </div>
              <div v-if="state.object.type_of_work == 'task_outcome'" class="detail-tab-elem">
                <span class="detail-tab-label">Шаблон задачи:</span> {{ state.object.task_template ? state.object.task_template.str : 'Нет шаблона задачи' }}
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

            <div v-if="activeTab === 'control_element_events'" class="chips-tab-outer">
              
              <div v-if="state.canViewControlElement">
                
                <div v-if="state.object.control_element_events && state.object.control_element_events.length > 0" class="chips-tab-inner">
                  
                  <div v-for="control_element_event in state.object.control_element_events" :key="control_element_event.id" class="chips-tab-item">

                    <div class="chips-tab-item-top">

                      <div class="chips-tab-item-title">
                        <h2>
                          {{ control_element_event.event_type_display ? control_element_event.event_type_display : 'Нет данных' }}
                        </h2>
                      </div>

                    </div>
                    
                    <div v-if="
                    control_element_event.event_type == 'task_created' || 
                    control_element_event.event_type == 'child_task_status_changed' || 
                    control_element_event.event_type == 'task_status_changed' || 
                    control_element_event.event_type == 'task_outcome_changed' ||
                    control_element_event.event_type == 'periodic_event' 
                    " class="chips-tab-item-detail">
                      
                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_event.task_template ? control_element_event.task_template.str : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_event.event_type == 'trigger_fired'" class="chips-tab-item-detail">
                      
                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Сработавший триггер:</span> {{ control_element_event.fired_trigger ? control_element_event.fired_trigger.str : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_event.event_type == 'periodic_event'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Период:</span> {{ control_element_event.period_display || 'Нет периода' }}
                      </div>
                      
                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Начало:</span>  {{ control_element_event.start_time ? formatDateTime(control_element_event.start_time) : 'Нет данных о начале' }}
                      </div>

                    </div>

                    <div v-if="state.canEditControlElement || state.canDeleteControlElement" class="chips-tab-item-menu-outer">
                      <div class="chips-tab-item-menu-inner">
                        <router-link 
                          v-if="state.canEditControlElement" 
                          :to="{ name: 'ControlElementEventEdit', params: { id: control_element_event.id }, query: { control_elementId: state.object.id }  }"
                          class="table-tab-button"
                        >
                          Изменить
                        </router-link>
                        <button 
                          v-if="state.canDeleteControlElement" 
                          @click="openControlElementEventDeleteModal(control_element_event)"
                          class="table-tab-button"
                        >
                          Удалить
                        </button>                           
                      </div>
                    </div>
                    <div v-else> 
                      -
                    </div>

                  </div>

                  <div v-if="showControlElementEventDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedControlElementEvent.str || 'Безымянный исполнитель очереди' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmControlElementEventDelete(selectedControlElementEvent.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeControlElementEventDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div> 

                </div>
                
                <div v-else >
                  <div class="none-border">Нет событий</div>
                </div>
              </div>
              
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
              
              <div v-if="state.canEditControlElement" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canEditControlElement"
                  :to="{ name: 'CreateControlElementEvent', query: { control_elementId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'control_element_conditions'" class="chips-tab-outer">
              
              <div v-if="state.canViewControlElement">
                
                <div v-if="state.object.control_element_conditions && state.object.control_element_conditions.length > 0" class="chips-tab-inner">
                  
                  <div v-for="control_element_condition in state.object.control_element_conditions" :key="control_element_condition.id" class="chips-tab-item">

                    <div class="chips-tab-item-top">

                      <div class="chips-tab-item-title">
                        <h2>
                          {{ control_element_condition.item ? control_element_condition.item : 'Нет данных' }} - {{ control_element_condition.condition_type_display ? control_element_condition.condition_type_display : 'Нет данных' }}
                        </h2>
                      </div>

                    </div>

                    <div v-if="control_element_condition.condition_type == 'task_exists'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_condition.task_template ? control_element_condition.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_condition.target_task_display ? control_element_condition.target_task_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Оператор сравнения:</span> {{ control_element_condition.boolean_operator ? 'Да' : 'Нет' }}
                      </div>

                    </div>
                    
                    <div v-if="control_element_condition.condition_type == 'child_tasks_status' || control_element_condition.condition_type == 'task_status'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_condition.task_template ? control_element_condition.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_condition.target_task_display ? control_element_condition.target_task_display : 'Нет данных' }}
                      </div>

                      <div v-if="control_element_condition.item != 1" class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Логический оператор:</span> {{ control_element_condition.logic_operator_display ? control_element_condition.logic_operator_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Оператор сравнения:</span> {{ control_element_condition.comparison_operator_display ? control_element_condition.comparison_operator_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Статус задачи:</span> {{ control_element_condition.task_status_display ? control_element_condition.task_status_display : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_condition.condition_type == 'task_outcome'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_condition.task_template ? control_element_condition.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_condition.target_task_display ? control_element_condition.target_task_display : 'Нет данных' }}
                      </div>

                      <div v-if="control_element_condition.item != 1" class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Логический оператор:</span> {{ control_element_condition.logic_operator_display ? control_element_condition.logic_operator_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Оператор сравнения:</span> {{ control_element_condition.comparison_operator_display ? control_element_condition.comparison_operator_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Итог задачи:</span> {{ control_element_condition.task_outcome ? control_element_condition.task_outcome.str : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_condition.condition_type == 'days_worked'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Оператор сравнения:</span> {{ control_element_condition.order_operator_display ? control_element_condition.order_operator_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Дни стажа:</span> {{ control_element_condition.days_worked ? control_element_condition.days_worked : 'Нет данных' }}
                      </div>

                    </div>


                    <div v-if="state.canEditControlElement || state.canDeleteControlElement" class="chips-tab-item-menu-outer">
                      <div class="chips-tab-item-menu-inner">
                        <router-link 
                          v-if="state.canEditControlElement" 
                          :to="{ name: 'ControlElementConditionEdit', params: { id: control_element_condition.id }, query: { control_elementId: state.object.id }  }"
                          class="table-tab-button"
                        >
                          Изменить
                        </router-link>
                        <button 
                          v-if="state.canDeleteControlElement" 
                          @click="openControlElementConditionDeleteModal(control_element_condition)"
                          class="table-tab-button"
                        >
                          Удалить
                        </button>                           
                      </div>
                    </div>
                    <div v-else> 
                      -
                    </div>

                  </div>

                  <div v-if="showControlElementConditionDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedControlElementCondition.str || 'Безымянный исполнитель очереди' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmControlElementConditionDelete(selectedControlElementCondition.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeControlElementConditionDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div> 

                </div>
                
                <div v-else >
                  <div class="none-border">Нет условий</div>
                </div>
              </div>
              
              
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
                            
              <div v-if="state.canEditControlElement" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canEditControlElement"
                  :to="{ name: 'CreateControlElementCondition', query: { control_elementId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'control_element_actions'" class="chips-tab-outer">
              
              <div v-if="state.canViewControlElement">
                
                <div v-if="state.object.control_element_actions && state.object.control_element_actions.length > 0" class="chips-tab-inner">
                  
                  <div v-for="control_element_action in state.object.control_element_actions" :key="control_element_action.id" class="chips-tab-item">

                    <div class="chips-tab-item-top">

                      <div class="chips-tab-item-title">
                        <h2>
                          {{ control_element_action.item ? control_element_action.item : 'Нет данных' }} - {{ control_element_action.action_type_display ? control_element_action.action_type_display : 'Нет данных' }}
                        </h2>
                      </div>

                    </div>
                    
                    <div v-if="control_element_action.action_type == 'change_task_status'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_action.task_template ? control_element_action.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_action.target_task_display ? control_element_action.target_task_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Статус задачи:</span> {{ control_element_action.task_status_display ? control_element_action.task_status_display : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_action.action_type == 'change_task_outcome'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_action.task_template ? control_element_action.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_action.target_task_display ? control_element_action.target_task_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Итог задачи:</span> {{ control_element_action.task_outcome ? control_element_action.task_outcome.str : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_action.action_type == 'assign_task'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_action.task_template ? control_element_action.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевое взаимодействие:</span> {{ control_element_action.target_interaction_display ? control_element_action.target_interaction_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Тип исполнителя:</span> {{ control_element_action.executor_type_display ? control_element_action.executor_type_display : 'Нет данных' }}
                      </div>

                      <div v-if="control_element_action.executor_type == 'selected_executor'" class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Исполнитель:</span> {{ control_element_action.executor ? control_element_action.executor.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Контроль руководителей:</span> {{ state.object.manager_control ? 'Да' : 'Нет' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Группа контролеров:</span> {{ control_element_action.controller_group ? control_element_action.controller_group.str : 'Нет группы контролеров' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Группа наблюдателей:</span> {{ control_element_action.observer_group ? control_element_action.observer_group.str : 'Нет группы наблюдателей' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Тип задержки:</span> {{ control_element_action.delay_type_display ? control_element_action.delay_type_display : 'Нет данных' }}
                      </div>

                      <div v-if="control_element_action.delay_type != 'no_delay'" class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Задержка:</span> {{ control_element_action.delay_value ? control_element_action.delay_value : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_action.action_type == 'add_task_to_queue'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Шаблон задачи:</span> {{ control_element_action.task_template ? control_element_action.task_template.str : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая задача:</span> {{ control_element_action.target_task_display ? control_element_action.target_task_display : 'Нет данных' }}
                      </div>

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Очередь:</span> {{ control_element_action.queue ? control_element_action.queue.str : 'Нет данных' }}
                      </div>

                    </div>

                    <div v-if="control_element_action.action_type == 'add_to_group' || control_element_action.action_type == 'remove_from_group'" class="chips-tab-item-detail">

                      <div class="chips-tab-item-detail-elem">
                        <span class="chips-tab-item-detail-label">Целевая группа:</span> {{ control_element_action.target_group ? control_element_action.target_group.str : 'Нет целевой группы' }}
                      </div>

                    </div>

                    <div v-if="control_element_action.action_type == 'new_interaction'" class="chips-tab-item-detail">

                    </div>

                    <div v-if="state.canEditControlElement || state.canDeleteControlElement" class="chips-tab-item-menu-outer">
                      <div class="chips-tab-item-menu-inner">
                        <router-link 
                          v-if="state.canEditControlElement" 
                          :to="{ name: 'ControlElementActionEdit', params: { id: control_element_action.id }, query: { control_elementId: state.object.id }  }"
                          class="table-tab-button"
                        >
                          Изменить
                        </router-link>
                        <button 
                          v-if="state.canDeleteControlElement" 
                          @click="openControlElementActionDeleteModal(control_element_action)"
                          class="table-tab-button"
                        >
                          Удалить
                        </button>                         
                      </div>
                    </div>
                    <div v-else> 
                      -
                    </div>

                  </div>

                  <div v-if="showControlElementActionDeleteModal" class="modal-overlay">
                    <div class="modal">
                      <div class="modal-header">
                        <h2 class="modal-header-h2">Удаление {{ selectedControlElementAction.str || 'Безымянный исполнитель очереди' }}</h2>
                      </div>
                      <div class="minibutton-group modal-menu">
                        <button @click="confirmControlElementActionDelete(selectedControlElementAction.id)" class="minibutton">Подтвердить</button>
                        <button @click="closeControlElementActionDeleteModal" class="minibutton">Отменить</button>
                      </div>
                    </div>
                  </div>   

                </div>
                
                <div v-else >
                  <div class="none-border">Нет действий</div>
                </div>
              </div>
              
              
              <div v-else>
                <div class="none-border">У вас нет разрешения на просмотр</div>
              </div>
                            
              <div v-if="state.canEditControlElement" class="tab-menu minibutton-group">
                <router-link
                  v-if="state.canEditControlElement"
                  :to="{ name: 'CreateControlElementAction', query: { control_elementId: state.object.id } }"
                  class="minibutton"
                >
                  Создать
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'accountsGroupObjectPermissions'" class="table-tab">

              <AccountsGroupObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'controlelement'" />

            </div>

            <div v-if="activeTab === 'accountObjectPermissions'" class="table-tab">

              <AccountObjectPermissions :state="state" :fetchObject="fetchObject" :contentTypeModel="'controlelement'" />

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
import { ref, reactive, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { formatDate, formatDateTime, baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import AccountObjectPermissions from '../components/AccountObjectPermissions.vue';
import AccountsGroupObjectPermissions from '../components/AccountsGroupObjectPermissions.vue'; 

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const state = reactive({
  object: null,
  globalPermissionsList: [],
  objectPermissionsDict: {},
  canViewControlElement: false,
  canEditControlElement: false,
  canDeleteControlElement: false,
  canViewAccountObjectPermission: false,
  canAddAccountObjectPermission: false,
  canDeleteAccountObjectPermission: false,
  canViewAccountsGroupObjectPermission: false,
  canAddAccountsGroupObjectPermission: false,
  canDeleteAccountsGroupObjectPermission: false,
});

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
    const response = await axios.get(`${baseUrl}/control_elements/${id}/`, {
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

const showControlElementDeleteModal = ref(false);
const openControlElementDeleteModal = () => {
  showControlElementDeleteModal.value = true;
};
const closeControlElementDeleteModal = () => {
  showControlElementDeleteModal.value = false;
};
const confirmControlElementDelete = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  const id = route.params.id;
  try {
    await axios.delete(`${baseUrl}/control_elements/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    closeControlElementDeleteModal();
    router.push({ name: 'ControlElementList' });
  } catch (error) {
    console.error('Ошибка удаления задачи:', error);
  }
};


const showControlElementEventDeleteModal = ref(false);
const selectedControlElementEvent = ref(null);
const openControlElementEventDeleteModal = (control_element_event) => {
  selectedControlElementEvent.value = control_element_event;
  showControlElementEventDeleteModal.value = true;
};
const closeControlElementEventDeleteModal = () => {
  showControlElementEventDeleteModal.value = false;
};
const confirmControlElementEventDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/control_element_events/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeControlElementEventDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const showControlElementConditionDeleteModal = ref(false);
const selectedControlElementCondition = ref(null);
const openControlElementConditionDeleteModal = (control_element_condition) => {
  selectedControlElementCondition.value = control_element_condition;
  showControlElementConditionDeleteModal.value = true;
};
const closeControlElementConditionDeleteModal = () => {
  showControlElementConditionDeleteModal.value = false;
};
const confirmControlElementConditionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/control_element_conditions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeControlElementConditionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
  }
};

const showControlElementActionDeleteModal = ref(false);
const selectedControlElementAction = ref(null);
const openControlElementActionDeleteModal = (control_element_action) => {
  selectedControlElementAction.value = control_element_action;
  showControlElementActionDeleteModal.value = true;
};
const closeControlElementActionDeleteModal = () => {
  showControlElementActionDeleteModal.value = false;
};
const confirmControlElementActionDelete = async (id) => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    await axios.delete(`${baseUrl}/control_element_actions/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchObject();
    closeControlElementActionDeleteModal();
  } catch (error) {
    console.error('Ошибка удаления аккаунта:', error);
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

    state.canViewControlElement = state.globalPermissionsList.includes('bpms.view_control_element') ||
      (state.objectPermissionsDict['bpms.view_control_element'] &&
      state.objectPermissionsDict['bpms.view_control_element'].includes(Number(id)));
    console.log('Права на просмотр задач:', state.canViewControlElement);

    state.canEditControlElement = state.globalPermissionsList.includes('bpms.change_control_element') ||
      (Array.isArray(state.objectPermissionsDict['bpms.change_control_element']) &&
      state.objectPermissionsDict['bpms.change_control_element'].includes(Number(id)));
    console.log('Права на редактирование задач:', state.canEditControlElement);

    state.canDeleteControlElement = state.globalPermissionsList.includes('bpms.delete_control_element') ||
      (Array.isArray(state.objectPermissionsDict['bpms.delete_control_element']) &&
      state.objectPermissionsDict['bpms.delete_control_element'].includes(Number(id)));
    console.log('Права на удаление задач:', state.canDeleteControlElement);

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

  } catch (error) {
    console.error('Ошибка при загрузке разрешений пользователя:', error);
  }
};

const back = () => {
  goBackSmart(router);
};

const tabs = computed(() => [
  { name: 'details', label: 'Детали' },
  { name: 'desc', label: 'Описание' },
  { name: 'control_element_events', label: 'События' },
  { name: 'control_element_conditions', label: 'Условия' },
  { name: 'control_element_actions', label: 'Действия' },
  state.canViewAccountsGroupObjectPermission ? { name: 'accountsGroupObjectPermissions', label: 'Объектные права групп' } : null,
  state.canViewAccountObjectPermission ? { name: 'accountObjectPermissions', label: 'Объектные права аккаунтов' } : null,
].filter(Boolean));

const activeTab = ref(route.query.tab || localStorage.getItem(`activeControlElementTab-${route.params.id}`) || 'desc');
watch(activeTab, (newTab) => {
  localStorage.setItem(`activeControlElementTab-${route.params.id}`, newTab);
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

</script>

<style scoped>

</style>
