from django.shortcuts import render

# Create your views here.

from django.utils import timezone
from django.http import JsonResponse
import zipfile
from django.views.decorators.csrf import csrf_exempt
import json
import shutil
from rest_framework.exceptions import APIException
from .filters import *
from .serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from core.permissions import ObjectPermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from django.http import FileResponse
import mimetypes
from bpms.serializers import *
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
import os
from django.conf import settings

import logging
logger = logging.getLogger('project')

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = CourseFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return CourseEditSerializer
        elif self.action == 'partial_update':
            return CourseEditSerializer
        return CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        try:
            # Курс.
            course = serializer.save()

            # Проверяем, был ли загружен новый файл.
            if 'upload_file' in serializer.validated_data:

                # Путь распаковки.
                extract_path = os.path.join(settings.MEDIA_ROOT, 'scorm_packages', str(course.id))

                # Удаляем старое содержимое, если оно существует.
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)

                # Создаем директорию.
                os.makedirs(extract_path, exist_ok=True)

                # Логирование: начало распаковки.
                logger.info(f"Начало распаковки SCORM-пакета {course.id}")

                # Распаковываем SCORM-пакет.
                with zipfile.ZipFile(course.upload_file.path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                # Логирование: успешная распаковка.
                logger.info(f"Успешная распаковка SCORM-пакета {course.id} в {extract_path}")

        except Exception as e:
            logger.error(f"Ошибка при распаковке SCORM-пакета {course.id}: {e}")
            if settings.DEBUG:
                raise
            else:
                raise APIException(f"Ошибка при распаковке SCORM-пакета: {str(e)}")

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

@api_view(['GET'])
@permission_classes([AllowAny])
def download_scorm(request, course_id):
    try:
        logger.debug(f"Запрос на скачивание файла. course_id: {course_id}")

        course = get_object_or_404(Course, id=course_id)
        logger.debug(f"Файл найден в базе: {course.name}, путь: {course.upload_file.path}")

        user = request.user if request.user.is_authenticated else get_anonymous_user()
        logger.debug(f"Пользователь: {user} (аутентифицирован: {request.user.is_authenticated})")

        if not (user.has_perm('courses.view_course') or user.has_perm('courses.view_course', course)):
            logger.warning(f"Пользователь {user} не имеет прав на просмотр файла {course_id}")
            return Response({"error": "Нет доступа"}, status=403)

        course_path = course.upload_file.path
        if not os.path.exists(course_path):
            logger.error(f"Файл не найден по пути: {course_path}")
            return Response({"error": "Файл не найден"}, status=404)

        coursename = os.path.basename(course.upload_file.name)
        mime_type, _ = mimetypes.guess_type(course_path)
        logger.debug(f"Имя файла: {coursename}")
        logger.debug(f"MIME-тип: {mime_type}")

        response = FileResponse(
            open(course_path, 'rb'),
            content_type=mime_type or 'application/octet-stream',
            as_attachment=True,
            filename=coursename
        )
        logger.debug(f"Заголовок Content-Disposition: {response['Content-Disposition']}")
        logger.debug(f"Content-Type: {response['Content-Type']}")

        return response

    except Exception as e:
        logger.exception(f"Ошибка при скачивании файла ID={course_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def scorm_content(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id)
        result = task.course_result

        executor = result.task.executor == request.user
        close = result.status == 'failed' or result.status == 'canceled'

        if not executor or close:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        if request.method == 'GET':

            return JsonResponse({
                'task_id': task.id,
                'type': task.course.constructor_type,
                'title': task.course.name,
                'course_id': task.course.id,
                'user_id': task.executor.id,
                'status': result.status,
            })

    except Exception as e:
        logger.exception(f"Ошибка при просмотре курса по задаче ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

# Запуск SCORM.
@csrf_exempt
def scorm_initialize(request):
    # Выводим отладочную информацию о запросе.
    logger.info(f'scorm_initialize: {request}, {request.body}')

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Ловим ошибки.
    try:
        # Разджисониваем.
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        if settings.DEBUG:
            logger.info(f'Данные запроса на запись данных: {data}')

        # Получаем объект CourseResult для отслеживания прогресса пользователя.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result

        # Если курс назначен - ставим отметку начала.
        if result.status == 'assigned':
            result.start_time = timezone.now()
            result.status = 'in_progress'
            result.save()

        # Возвращаем успешный JSON-ответ с информацией о процессе инициализации.
        logger.info(f'Результат курса: {result}')
        return JsonResponse({'status': 'initialize_success'})

    # Ловим ошибки декодирования JSON.
    except json.JSONDecodeError as e:
        logger.info(f'JSON Decode Error in scorm_initialize: {e}')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Обрабатываем другие исключения, выводим ошибку.
    except Exception as e:
        logger.info(f'Error in scorm_initialize: {e}')
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)


# Получение значения из базы.
@csrf_exempt
def scorm_get_value(request):

    # Проверка корректности метода.
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Ловим ошибки.
    try:
        # Получаем значения из квери.
        task_id = request.GET.get('task_id')
        user_id = request.GET.get('user_id')
        element = request.GET.get('element')

        # Выводим информацию о полученном элементе.
        if settings.DEBUG:
            logger.info(f'task_id: {task_id}')
            logger.info(f'user_id: {user_id}')
            logger.info(f'Запрашиваемый элемент: {element}')

        # Проверяем, что элемент был передан.
        if not element:
            return JsonResponse({'status': 'error', 'message': 'Element not specified'}, status=400)

        # Если запрашивается режим работы.
        if element == 'cmi.mode':
            # Установка режима работы для передачи пакету.
            scorm_mode = 'normal'
            return JsonResponse({'cmi.mode': scorm_mode})

        # Если запрашивается ID пользователя Django.
        if element == 'cmi.learner_id':
            # Возврат ID пользователя Django.
            return JsonResponse({'cmi.learner_id': request.user.id})

        # Если запрашивается имя пользователя Django.
        if element == 'cmi.learner_name':
            # Возврат имени пользователя Django.
            return JsonResponse({'cmi.learner_name': request.user.username})

        # Получаем последний объект CourseResult из базы данных.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result

        # Преобразование строки JSON в словарь Python.
        progress_data = json.loads(result.progress)

        # Если запрашивается номер взаимодействия.
        if element == 'cmi.interactions._count':
            # Возврат количества взаимодействий
            interaction_count = str(len(progress_data.get('cmi.interactions', [])))
            if settings.DEBUG:
                logger.info(f'Номер взаимодействия: {interaction_count}')
            return JsonResponse({'cmi.interactions._count': interaction_count})

        # Если запрашивается конкретное взаимодействие.
        elif element.startswith('cmi.interactions[') and element.endswith(']'):
            # Извлекаем индекс из строки элемента.
            index = int(element.split('[')[1].split(']')[0])
            # Извлекаем данные об интеракциях из прогресса.
            interaction_data = progress_data.get('cmi.interactions', [])
            # Проверяем, существует ли интеракция с запрошенным индексом.
            if index < len(interaction_data):
                # Возвращаем данные по конкретной интеракции.
                return JsonResponse(interaction_data[index])
            else:
                # Если индекс выходит за пределы существующих интеракций, возвращаем ошибку.
                return JsonResponse({'status': 'error', 'message': 'Invalid interaction index'}, status=404)

        # Возврат других элементов.
        elif element in progress_data:
            return JsonResponse({element: progress_data[element]})

        # Если нужного элемента нет - выдаем ошибку.
        else:
            return JsonResponse({'status': 'error', 'message': 'Element not found'}, status=404)

    # Если результата нет - выдаем ошибку.
    except CourseResult.DoesNotExist:
        return JsonResponse({'status': 'progress_not_found'}, status=404)

    # Отрабатываем другие ошибки.
    except Exception as e:
        # Выводим информацию об ошибке в консоль.
        logger.info(f'Error in scorm_get_value: {e}')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Установка значения в базе.
@csrf_exempt
def scorm_set_value(request):

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Ловим ошибки.
    try:
        # Разджисониваем.
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        if settings.DEBUG:
            logger.info(f'Данные запроса на запись данных: {data}')

        # Получение данных о прогрессе пользователя.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result
        progress_data = json.loads(result.progress)

        # Инициализация, если отсутствует.
        progress_data.setdefault('cmi.interactions', [])

        check_status = False

        # Разбираем словарь.
        for key, value in data.items():

            # Если нужно записать результат взаимодействия.
            if 'cmi.interactions' in key:

                # Делим результат взаимодействия на уже выделенные точками части.
                parts = key.split('.')
                # Получение индекса взаимодействия.
                interaction_index = int(parts[2])
                # Получение свойства взаимодействия.
                interaction_property = parts[3]

                # Убедитесь, что у вас достаточно элементов в массиве.
                while len(progress_data['cmi.interactions']) <= interaction_index:
                    progress_data['cmi.interactions'].append({})

                # Обновление или добавление данных взаимодействия.
                progress_data['cmi.interactions'][interaction_index][interaction_property] = value

                # Печать результата
                if settings.DEBUG:
                    logger.info(f"Итог запроса на запись данных: cmi.interactions[{interaction_index}].{interaction_property} = {value}")

            # Если нужно записать что-то иное.
            else:

                # Обновление обычных ключей.
                progress_data[key] = value
                if settings.DEBUG:
                    logger.info(f"Итог запроса на запись данных: {key} = {value}")

                # Если нужно записать результат курса.
                if key == 'cmi.completion_status' or key == 'cmi.success_status':
                    check_status = True

        # Сохранение обновленных данных
        result.progress = json.dumps(progress_data)
        result.save()

        # Если нужно проверить статус:
        if check_status:

            # Если курс еще не пройден или не провален.
            if result.status != 'completed':

                # Преобразуем текущий прогресс в словарь.
                progress_data = json.loads(result.progress)

                # Забираем данные.
                success_status = progress_data.get('cmi.success_status', 'Статус выполнения не определен')
                if settings.DEBUG:
                    logger.info(f'Статус выполнения: {success_status}')
                completion_status = progress_data.get('cmi.completion_status', 'Статус прохождения не определен')
                if settings.DEBUG:
                    logger.info(f'Статус прохождения: {completion_status}')

                # Устанавливаем статус.
                if success_status in ['completed', 'passed']:
                    result.status = 'completed'
                    result.end_time = timezone.now()
                elif completion_status == 'completed' and success_status == 'unknown':
                    result.status = 'completed'
                    result.score_scaled = 100
                    result.end_time = timezone.now()
                elif completion_status == 'completed' and success_status == 'failed':
                    result.status = 'failed'
                    result.end_time = timezone.now()
                if settings.DEBUG:
                    logger.info(f'Статус курса: {result.status}')

                # Забираем %.
                score_scaled = progress_data.get('cmi.score.scaled', False)
                if score_scaled:
                    result.score_scaled = round(float(score_scaled) * 100)
                    if settings.DEBUG:
                        logger.info(f'Полученный балл в %: {result.score_scaled}')

                # Сохранение обновленных данных.
                result.save()

        # Возвращаем ответ об успехе.
        return JsonResponse({'status': 'set_value_success'})

    # Отрабатываем отсутствие результата.
    except CourseResult.DoesNotExist:
        return JsonResponse({'status': 'progress_not_found'}, status=404)

    # Ловим ошибки декодирования JSON.
    except json.JSONDecodeError as e:
        logger.info(f'JSON Decode Error in scorm_set_value: {e}')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Обработка ошибок.
    except Exception as e:
        logger.info(f'Error in scorm_set_value: {e}')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Сохранение данных.
@csrf_exempt
def scorm_commit(request):

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Ловим ошибки.
    try:
        # Разджисониваем.
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        if settings.DEBUG:
            logger.info(f'Данные запроса на запись данных: {data}')

        # Получение данных о прогрессе пользователя.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result

        # Преобразуем текущий прогресс в словарь.
        progress_data = json.loads(result.progress)

        # Объединяем новые данные с текущими данными о прогрессе.
        for key, value in data.items():
            progress_data[key] = value
        if settings.DEBUG:
            logger.info(f'Итоговые данные для сохранения: {progress_data}')

        # Сохранение обновленных данных.
        result.progress = json.dumps(progress_data)
        result.save()

        # Выдаем сообщение что сохранение выполнено.
        return JsonResponse({'status': 'commit_success'})

    # Отрабатываем отсутствие результата.
    except CourseResult.DoesNotExist:
        return JsonResponse({'status': 'progress_not_found'}, status=404)

    # Отрабатываем ошибки декодирования.
    except json.JSONDecodeError as e:
        logger.info(f'JSON Decode Error in scorm_commit: {e}')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Отрабатываем другие ошибки.
    except Exception as e:
        logger.info(f'Error in scorm_commit: {e}')
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)


# Завершение курса.
@csrf_exempt
def scorm_finish(request):

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Ловим ошибки.
    try:
        # Разджисониваем.
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        if settings.DEBUG:
            logger.info(f'Данные запроса на запись данных: {data}')

        # Получение данных о прогрессе пользователя.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result

        # Устанавливаем время завершения.
        result.end_time = timezone.now()

        # Cохраняем данные.
        result.save()

        # Отдаем ответ об успешном завершении.
        return JsonResponse({'status': 'finish_success'})

    # Отрабатываем отсутствие результата.
    except CourseResult.DoesNotExist:
        return JsonResponse({'status': 'progress_not_found'}, status=404)

    # Отрабатываем ошибки декодирования.
    except json.JSONDecodeError as e:
        logger.info(f'JSON Decode Error in scorm_finish: {e}')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Отрабатываем другие ошибки.
    except Exception as e:
        logger.info(f'Error in scorm_finish: {e}')
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)


# Отработчики ошибок.

def scorm_get_last_error(request):
    try:
        # Получаем значения из квери.
        task_id = request.GET.get('task_id')
        user_id = request.GET.get('user_id')
        if settings.DEBUG:
            logger.info(f'task_id: {task_id}')
            logger.info(f'user_id: {user_id}')


        # Получение данных о прогрессе пользователя.
        task = get_object_or_404(Task, id=task_id)
        result = task.course_result

        # Преобразование строки JSON в словарь Python.
        progress_data = json.loads(result.progress)
        error_code = progress_data.get('cmi.error_code', "0")

        return JsonResponse({'error_code': error_code})
    except Exception as e:
        logger.info(f'Error in scorm_get_last_error: {e}')
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

def scorm_get_error_string(request):
    error_code = request.GET.get('error_code', "0")

    error_strings = {
        "0": "No error",
        "101": "General exception",
        "102": "General initialization failure",
        "103": "Already initialized",
        "104": "Content instance terminated",
        "201": "Invalid argument error",
        "202": "Element cannot have children",
        "203": "Element not an array – cannot have count",
        "301": "Not initialized",
        "401": "Not implemented error",
        "402": "Invalid set value, element is a keyword",
        "403": "Element is read only",
        "404": "Element is write only",
        "405": "Incorrect data type",
        # Дополнительные коды ошибок по стандарту SCORM
    }

    error_string = error_strings.get(error_code, "Unknown error")
    return JsonResponse({'error_string': error_string})

def scorm_get_diagnostic(request):
    error_code = request.GET.get('error_code', "0")

    # Расширенное сопоставление кодов ошибок с диагностической информацией
    diagnostic_info = {
        "0": "No diagnostic information",
        "101": "General exception, no specific diagnostic information.",
        "102": "Initialization failed for an unknown reason.",
        "103": "Attempted to re-initialize.",
        "104": "Content terminated without proper initialization.",
        "201": "Invalid argument error, details provided in diagnostic information.",
        "202": "Element cannot have children, violating SCORM data model.",
        "203": "Element not an array, count function is invalid.",
        "301": "SCORM API not initialized.",
        "401": "SCORM API function not implemented.",
        "402": "Invalid set value, element is a keyword and is read-only.",
        "403": "Element is read-only and cannot be modified.",
        "404": "Element is write-only and cannot be read.",
        "405": "Incorrect data type used for value.",
        # Дополнительные коды ошибок и диагностика
    }

    diagnostic = diagnostic_info.get(error_code, "No specific diagnostic information available.")
    return JsonResponse({'diagnostic_info': diagnostic})

