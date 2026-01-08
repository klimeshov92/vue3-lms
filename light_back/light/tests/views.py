from django.shortcuts import render

# Create your views here.

from .models import *
from .filters import *
from .serializers import *
from bpms.serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from core.permissions import ObjectPermission
from guardian.utils import get_anonymous_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
import json
import random
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q

import logging
logger = logging.getLogger('project')

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = TestFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return TestEditSerializer
        elif self.action == 'partial_update':
            return TestEditSerializer
        return TestSerializer

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
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class TestSectionViewSet(viewsets.ModelViewSet):
    queryset = TestSection.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['name']
    ordering = ['name']

    permission_map = {
        'create': 'tests.add_test',
        'retrieve': 'tests.view_test',
        'update': 'tests.change_test',
        'partial_update': 'tests.change_test',
        'destroy': 'tests.delete_test',
        'list': 'tests.view_test',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_test =self._object.test
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            test = None
            if self.action == 'create':
                test_id = self.request.data.get('test')
                if test_id:
                    test = Test.objects.filter(pk=test_id).first()
            elif self.action == 'list':
                test_id = self.request.query_params.get('test')
                if test_id:
                    test = Test.objects.filter(pk=test_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                test = getattr(self, '_related_test', None)

            if test and not self.request.user.has_perm(perm_codename, test):
                self.permission_denied(self.request, message='Недостаточно прав на тест')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для теста {test}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return TestSectionEditSerializer
        elif self.action == 'partial_update':
            return TestSectionEditSerializer
        return TestSectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class TestSectionQuestionViewSet(viewsets.ModelViewSet):
    queryset = TestSectionQuestion.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'tests.add_test',
        'retrieve': 'tests.view_test',
        'update': 'tests.change_test',
        'partial_update': 'tests.change_test',
        'destroy': 'tests.delete_test',
        'list': 'tests.view_test',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_test = self._object.test_section.test
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            test = None
            if self.action == 'create':
                test_section_id = self.request.data.get('test_section')
                if test_section_id:
                    test = TestSection.objects.select_related('test').get(pk=test_section_id).test
            elif self.action == 'list':
                test_section_id = self.request.query_params.get('test_section')
                if test_section_id:
                    test = TestSection.objects.select_related('test').get(pk=test_section_id).test
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                test = getattr(self, '_related_test', None)

            if test and not self.request.user.has_perm(perm_codename, test):
                self.permission_denied(self.request, message='Недостаточно прав на тест')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для теста {test}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return TestSectionQuestionEditSerializer
        elif self.action == 'partial_update':
            return TestSectionQuestionEditSerializer
        return TestSectionQuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = QuestionFilter
    ordering_fields = ['text']
    ordering = ['text']

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionEditSerializer
        elif self.action == 'partial_update':
            return QuestionEditSerializer
        return QuestionSerializer

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
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'tests.add_question',
        'retrieve': 'tests.view_question',
        'update': 'tests.change_question',
        'partial_update': 'tests.change_question',
        'destroy': 'tests.delete_question',
        'list': 'tests.view_question',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_question =self._object.question
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            question = None
            if self.action == 'create':
                question_id = self.request.data.get('question')
                if question_id:
                    question = Question.objects.filter(pk=question_id).first()
            elif self.action == 'list':
                question_id = self.request.query_params.get('question')
                if question_id:
                    question = Question.objects.filter(pk=question_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                question = getattr(self, '_related_question', None)

            if question and not self.request.user.has_perm(perm_codename, question):
                self.permission_denied(self.request, message='Недостаточно прав на вопрос')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для вопроса {question}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerEditSerializer
        elif self.action == 'partial_update':
            return AnswerEditSerializer
        return AnswerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class RelevantPointViewSet(viewsets.ModelViewSet):
    queryset = RelevantPoint.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['text']
    ordering = ['text']

    permission_map = {
        'create': 'tests.add_question',
        'retrieve': 'tests.view_question',
        'update': 'tests.change_question',
        'partial_update': 'tests.change_question',
        'destroy': 'tests.delete_question',
        'list': 'tests.view_question',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_question = self._object.answer.question
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            question = None
            if self.action == 'create':
                answer_id = self.request.data.get('answer')
                if answer_id:
                    question = Answer.objects.select_related('question').get(pk=answer_id).question
            elif self.action == 'list':
                answer_id = self.request.query_params.get('answer')
                if answer_id:
                    question = Answer.objects.select_related('question').get(pk=answer_id).question
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                question = getattr(self, '_related_question', None)

            if question and not self.request.user.has_perm(perm_codename, question):
                self.permission_denied(self.request, message='Недостаточно прав на вопрос')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для вопроса {question}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return RelevantPointEditSerializer
        elif self.action == 'partial_update':
            return RelevantPointEditSerializer
        return RelevantPointSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

@api_view(['GET'])
@permission_classes([AllowAny])
def test_attempt(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        test = task.test
        result = task.test_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        attempt_available = test.attempts > result.attempts
        logger.debug(f"Использовано попыток: {result.attempts} из {test.attempts}. Есть еще попытки: {attempt_available}")

        last_attempt = result.test_attempts.latest('id') if result.test_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        last_attempt_end = last_attempt.end_time if last_attempt else None
        logger.debug(f"Последняя попытка прохождения теста завершена: {last_attempt_end}")

        need_create_attempt = (
            (last_attempt and last_attempt_end and attempt_available) or
            (not last_attempt and attempt_available)
        )
        logger.debug(f"Необходимо создать попытку: {need_create_attempt}")

        if need_create_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not test.test_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not TestSectionQuestion.objects.filter(test_section__in=test.test_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            test_attempt = TestAttempt.objects.create(
                test_result=result,
                number = result.test_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=test.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {test_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {test.attempts}")
            result.save()

            question_sorting = []

            for test_section in test.test_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {test_section}")
                if test_section.test_section_questions.count() > test_section.sample_size:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')[:test_section.sample_size]
                else:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {test_section}")

                for selected_test_section_question in selected_test_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_test_section_question.question}")

                    question_sorting.append(selected_test_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        test_attempt=test_attempt,
                        question=selected_test_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if test.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            test_attempt.question_sorting = json.dumps(question_sorting)
            test_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")
        else:
            test_attempt = last_attempt
            logger.debug(f"Попытка для результата теста получена: {test_attempt}")

        if request.method == 'GET':
            serializer = TestAttemptSerializer(test_attempt, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_attempt_open(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        test = task.test
        result = task.test_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        last_attempt = result.test_attempts.latest('id') if result.test_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        if not last_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not test.test_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not TestSectionQuestion.objects.filter(test_section__in=test.test_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            test_attempt = TestAttempt.objects.create(
                test_result=result,
                number = result.test_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=test.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {test_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {test.attempts}")
            result.save()

            question_sorting = []

            for test_section in test.test_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {test_section}")
                if test_section.test_section_questions.count() > test_section.sample_size:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')[:test_section.sample_size]
                else:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {test_section}")

                for selected_test_section_question in selected_test_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_test_section_question.question}")

                    question_sorting.append(selected_test_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        test_attempt=test_attempt,
                        question=selected_test_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if test.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            test_attempt.question_sorting = json.dumps(question_sorting)
            test_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")
        else:
            test_attempt = last_attempt
            logger.debug(f"Попытка для результата теста получена: {test_attempt}")

        if request.method == 'GET':
            serializer = TestAttemptSerializer(test_attempt, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def test_attempt_create(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        test = task.test
        result = task.test_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        attempt_available = test.attempts > result.attempts
        logger.debug(f"Использовано попыток: {result.attempts} из {test.attempts}. Есть еще попытки: {attempt_available}")

        last_attempt = result.test_attempts.latest('id') if result.test_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        last_attempt_end = last_attempt.end_time if last_attempt else None
        logger.debug(f"Последняя попытка прохождения теста завершена: {last_attempt_end}")

        need_create_attempt = last_attempt and last_attempt_end and attempt_available
        logger.debug(f"Необходимо создать попытку: {need_create_attempt}")

        if need_create_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not test.test_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not TestSectionQuestion.objects.filter(test_section__in=test.test_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            test_attempt = TestAttempt.objects.create(
                test_result=result,
                number = result.test_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=test.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {test_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {test.attempts}")
            result.save()

            question_sorting = []

            for test_section in test.test_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {test_section}")
                if test_section.test_section_questions.count() > test_section.sample_size:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')[:test_section.sample_size]
                else:
                    selected_test_section_questions = test_section.test_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {test_section}")

                for selected_test_section_question in selected_test_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_test_section_question.question}")

                    question_sorting.append(selected_test_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        test_attempt=test_attempt,
                        question=selected_test_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if test.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            test_attempt.question_sorting = json.dumps(question_sorting)
            test_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")

            if request.method == 'POST':
                serializer = TestAttemptSerializer(test_attempt, context={'request': request})
                return Response(serializer.data)

        else:
            logger.debug(f"Нельзя создать попытку прохождения теста")
            return Response({"error": "Нельзя создать попытку прохождения теста"}, status=403)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def send_answers(request, question_result_id):

    # Выводим отладочную информацию о запросе.
    logger.info(f'Ответ на вопрос: {request}, {request.body}')

    # Проверка корректности метода.
    if request.method != 'PATCH':
        return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)

    # Ловим ошибки.
    try:

        question_result = get_object_or_404(QuestionResult, pk=question_result_id)
        logger.debug(f"Результат вопроса: {question_result}")
        test_attempt = question_result.test_attempt
        logger.debug(f"Попытка теста: {test_attempt}")
        test_result = test_attempt.test_result
        logger.debug(f"Результат теста: {test_result}")
        task = test_result.task
        logger.debug(f"Задача: {test_result}")

        executor = task.executor == request.user
        if not executor:
            return Response({"error": "Это тест для другого пользователя"}, status=403)
        logger.debug(f"Тест принадлежит пользователю")

        test_finished = test_result.finished
        if test_finished:
            return Response({"error": "Тест уже завершен"}, status=403)
        logger.debug(f"Тест активен")

        attempt_time_out = test_attempt.plan_end_time and timezone.now() > test_attempt.plan_end_time
        if attempt_time_out:
            return Response(
                {
                    "error": "Время на попытку истекло",
                    "test_attempt_status": test_attempt.status,
                },
                status=403
            )
        logger.debug(f"Время на попытку еще есть")

        if test_attempt.status == 'assigned':
            test_attempt.status = 'in_progress'
            logger.debug(f"Попытка начата")

        question_result_finished = question_result.status in ['completed', 'failed']
        if question_result_finished:
            return Response(
                {
                    "error": "Вопрос завершен",
                    "test_attempt_status": question_result.status,
                },
                status=403
            )
        logger.debug(f"Вопрос активен")

        # Разджисониваем.
        data = json.loads(request.body)
        logger.debug(f'Данные запроса на запись данных: {data}')

        answers = data.get("answer_results", [])
        for answer in answers:
            answer_result_id = answer.get("id")
            selected_answer = answer.get("selected_answer")
            selected_position = answer.get("selected_position")
            selected_text_input = answer.get("selected_text_input")
            selected_numeric_input = answer.get("selected_numeric_input")
            selected_relevant_point = answer.get("selected_relevant_point")

            answer_result = get_object_or_404(AnswerResult, pk=answer_result_id)
            logger.debug(f"Результат ответа до обработки: {answer_result}")

            if answer_result.answer.question.question_type == 'single_selection' or answer_result.answer.question.question_type == 'multiple_choice':
                answer_result.selected_answer = selected_answer
                correct_answer = answer_result.selected_answer == answer_result.answer.correct_answer
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'sorting':
                answer_result.selected_position = selected_position
                correct_answer = answer_result.selected_position == answer_result.answer.correct_item
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'compliance':
                answer_result.selected_relevant_point = get_object_or_404(RelevantPoint, pk=selected_relevant_point)
                correct_answer = answer_result.selected_relevant_point == answer_result.answer.relevant_point
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'text_input':
                answer_result.selected_text_input = selected_text_input
                correct_answer = answer_result.selected_text_input == answer_result.answer.correct_text_input
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'numeric_input':
                answer_result.selected_numeric_input = selected_numeric_input
                correct_answer = answer_result.selected_numeric_input == answer_result.answer.correct_numeric_input
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'
            if correct_answer:
                answer_result.score = answer_result.answer.score
            else:
                answer_result.score = 0
            answer_result.end_time = timezone.now()
            answer_result.save()
            logger.debug(f"Результат ответа после обработки: {answer_result}")

        correct_question = all(
            answer.status == 'completed'
            for answer in question_result.answer_results.all()
        )
        if correct_question:
            logger.debug(f"Все ответы на вопрос верные")
            question_result.status = 'completed'
            question_result.score = question_result.question.score
        else:
            logger.debug(f"Ответ неверный")
            question_result.status = 'failed'
            question_result.score = 0


        question_result.end_time = timezone.now()
        question_result.save()
        logger.debug(f"Результат вопроса после обработки: {question_result}")

        answers_scores_sum = question_result.answer_results.aggregate(sum=Sum('score'))['sum']
        logger.debug(f"Сумма баллов за ответы: {answers_scores_sum}")
        logger.debug(f"Баллы за вопрос: {question_result.score}")
        logger.debug(f"Текущие баллы за попытку: {test_attempt.score}")
        test_attempt.score += (answers_scores_sum + question_result.score)
        test_attempt.save()
        logger.debug(f"Новые баллы за попытку: {test_attempt.score}")
        test_result.score += (answers_scores_sum + question_result.score)
        test_result.save()
        logger.debug(f"Новые баллы за тест: {test_result.score}")

        attempt_question_out = not test_attempt.question_results.exclude(Q(status='completed') | Q(status='failed')).exists()
        logger.debug(f"Вопросы закончились: {attempt_question_out}")

        if attempt_time_out or attempt_question_out:

            if test_attempt.status not in ['completed', 'failed', 'canceled']:
                logger.debug(f"Попытка еще не завершена")

                test_attempt_completed = test_attempt.score >= test_result.task.test.passing_score
                if test_attempt_completed:
                    logger.debug(f"Тест пройден. Требуется: {test_result.task.test.passing_score} баллов. Набрано: {test_attempt.score} баллов.")
                    test_attempt.status = 'completed'
                    test_result.status = 'completed'
                else:
                    logger.debug(f"Тест провален. Требуется: {test_result.task.test.passing_score} баллов. Набрано: {test_attempt.score} баллов.")
                    test_attempt.status = 'failed'
                    test_result.status = 'failed'

                test_finished = test_result.attempts >= test_result.task.test.attempts
                if test_finished:
                    test_result.finished = True

                test_attempt.end_time = timezone.now()
                test_result.end_time = timezone.now()
                test_attempt.save()
                test_result.save()
                logger.debug(f"Обновленный результат попытки: {test_attempt}")
                logger.debug(f"Обновленный результат теста: {test_result}")

                for question_result in test_attempt.question_results.all():
                    if question_result.status not in ['completed', 'failed']:
                        logger.debug(f"Вопрос не завершен при завершении попытки: {question_result}")
                        question_result.status = 'failed'
                        question_result.save()
                        logger.debug(f"Вопрос завершен: {question_result}")
            else:
                logger.debug(f"Попытка уже завершена")

        # Возвращаем успешный JSON-ответ с информацией о процессе инициализации.
        attempt_finished = test_attempt.status in ['completed', 'failed']
        if attempt_finished:
            serializer = TestAttemptSerializer(test_attempt, context={'request': request})
            return Response({
                'status': 'ok',
                'type': 'test_attempt',  # можно пометить, что это полный результат
                'data': serializer.data
            })
        else:
            serializer = QuestionResultSerializer(question_result, context={'request': request})
            return Response({
                'status': 'ok',
                'type': 'question_result',  # пометка, что это частичный ответ
                'data': serializer.data
            })

    except Exception as e:
        logger.exception(f"Ошибка при отправке ответов на вопрос ID={question_result_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def test_finish(request, test_attempt_id):

    # Выводим отладочную информацию о запросе.
    logger.info(f'Завершение теста: {request}, {request.body}')

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)

    # Ловим ошибки.
    try:

        test_attempt = get_object_or_404(TestAttempt, pk=test_attempt_id)
        logger.debug(f"Попытка теста: {test_attempt}")
        test_result = test_attempt.test_result
        logger.debug(f"Результат теста: {test_result}")
        task = test_result.task
        logger.debug(f"Задача: {test_result}")

        executor = task.executor == request.user
        if not executor:
            return Response({"error": "Это тест для другого пользователя"}, status=403)
        logger.debug(f"Тест принадлежит пользователю")

        test_finished = test_result.finished
        if test_finished:
            return Response({"error": "Тест уже завершен"}, status=403)
        logger.debug(f"Тест активен")

        attempt_finished = test_attempt.status in ['completed', 'failed']
        logger.debug(f"Попытка завершена: {attempt_finished }")
        test_attempt_completed = test_attempt.score >= test_result.task.test.passing_score
        logger.debug(f"Попытка успешна: {test_attempt_completed}")
        if test_attempt_completed:
            logger.debug(f"Тест пройден. Требуется: {test_result.task.test.passing_score} баллов. Набрано: {test_attempt.score} баллов.")
            if not attempt_finished:
                test_attempt.status = 'completed'
            test_result.status = 'completed'
        else:
            logger.debug(f"Тест провален. Требуется: {test_result.task.test.passing_score} баллов. Набрано: {test_attempt.score} баллов.")
            if not attempt_finished:
                test_attempt.status = 'failed'
            test_result.status = 'failed'

        if not attempt_finished:
            test_attempt.end_time = timezone.now()
            test_attempt.save()
            logger.debug(f"Обновленный результат попытки: {test_attempt}")

        test_finished = test_result.attempts >= test_result.task.test.attempts
        if test_finished:
            test_result.finished = True
        test_result.end_time = timezone.now()
        test_result.save()

        for question_result in test_attempt.question_results.all():
            if question_result.status not in ['completed', 'failed']:
                logger.debug(f"Вопрос не завершен при завершении попытки: {question_result}")
                question_result.status = 'failed'
                question_result.save()
                logger.debug(f"Вопрос завершен: {question_result}")

        logger.debug(f"Обновленный результат теста: {test_result}")

        serializer = TestAttemptSerializer(test_attempt, context={'request': request})
        return Response({
            'status': 'ok',
            'data': serializer.data
        })

    # Ловим ошибки декодирования JSON.
    except json.JSONDecodeError as e:
        logger.info(f'Ошибка декодирования JSON при завершении теста: {e}')
        return Response({'status': 'error', 'message': 'Невалидный JSON'}, status=400)

    # Обрабатываем другие исключения, выводим ошибку.
    except Exception as e:
        logger.info(f'Error in scorm_initialize: {e}')
        return Response({'status': 'error', 'message': 'Неизвестная ошибка сервера'}, status=500)
