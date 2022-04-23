from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import F, Max, QuerySet
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from typing import Optional

from Todo.models import ToDo
from common_decorator import mandatories, optionals


def get_max_int_from_queryset(qs: QuerySet, _from: str) -> Optional[int]:
    return qs.aggregate(_max=Max(_from)).get('_max')


class ToDoListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            todo_set = ToDo.objects.filter(author=request.user, completedDate__isnull=True).order_by('orderNumber').values()
            return Response(data={"todo_set": todo_set}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    @mandatories('text')
    @optionals({'deadLine': None})
    def post(self, request, m, o):
        if request.user.is_authenticated:
            deadLine = o['deadLine']
            text = m['text']

            # 한국 9시간 더하기
            if deadLine:
                deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))

            todo_qs = ToDo.objects.filter(
                author=request.user,
                completedDate__isnull=True,
                orderNumber__isnull=False,
            )
            max_orderNumber = get_max_int_from_queryset(todo_qs, 'orderNumber')

            if not max_orderNumber:
                max_orderNumber = 1

            todo = ToDo.objects.create(
                author=request.user,
                startDate=timezone.now(),
                deadLine=deadLine,
                text=text,
                orderNumber=max_orderNumber + 1,
            )

            return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class ToDoDetailAPI(APIView):

    @mandatories('text')
    @optionals({'deadLine': None})
    def put(self, request, id, m, o):
        if request.user.is_authenticated:
            deadLine = o['deadLine']
            text = m['text']

            # 한국 9시간 더하기
            if deadLine:
                deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))

            try:
                todo = ToDo.objects.get(author=request.user, id=id)
                todo.deadLine = deadLine
                todo.text = text
                todo.save(['deadLine', 'text', 'updated_at'])

                return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if request.user.is_authenticated:
            try:
                with transaction.atomic():
                    delete_todo = ToDo.objects.get(author=request.user, id=id)
                    orderNumber = delete_todo.orderNumber

                    # TODO 추후에 Signal 로 작업
                    ToDo.objects.filter(
                        author=request.user,
                        completedDate__isnull=True,
                        orderNumber__isnull=False,
                        orderNumber__gt=orderNumber
                    ).update(
                        orderNumber=F('orderNumber') - 1
                    )

                    delete_todo.delete()

                return Response(data={"message": "success"}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class ToDoOrderChangingAPI(APIView):

    @mandatories('currentId', 'targetId')
    def put(self, request, m):
        if request.user.is_authenticated:
            currentId = m['currentId']
            targetId = m['targetId']

            todo_set = ToDo.objects.filter(author=request.user, completedDate__isnull=True)
            try:
                current_todo = todo_set.get(pk=currentId)
                target_todo = todo_set.get(pk=targetId)
            except ToDo.DoesNotExist:
                return Response(data={"message": "bad request"}, status=status.HTTP_403_FORBIDDEN)

            # 위로 이동
            with transaction.atomic():
                # NULL 예외처리
                if target_todo.orderNumber is None and current_todo.orderNumber is None:
                    todo_set.filter(orderNumber__isnull=False).update(orderNumber=F('orderNumber') + 2)

                    target_todo = todo_set.get(pk=targetId)
                    target_todo.orderNumber = 2
                    target_todo.save(update_fields=['orderNumber'])

                    current_todo = todo_set.get(pk=currentId)
                    current_todo.orderNumber = 1
                    current_todo.save(update_fields=['orderNumber'])
                elif target_todo.orderNumber is None:
                    todo_set.filter(orderNumber__gt=current_todo.orderNumber).update(orderNumber=F('orderNumber') + 1)
                    todo_set.filter(orderNumber__lt=current_todo.orderNumber).update(orderNumber=F('orderNumber') + 2)

                    target_todo = todo_set.get(pk=targetId)
                    target_todo.orderNumber = 2
                    target_todo.save(update_fields=['orderNumber'])

                    current_todo = todo_set.get(pk=currentId)
                    current_todo.orderNumber = 1
                    current_todo.save(update_fields=['orderNumber'])
                elif current_todo.orderNumber is None:
                    target_todo = todo_set.get(pk=targetId)
                    to_be_current_order = target_todo.orderNumber

                    todo_set.filter(orderNumber__gte=to_be_current_order).update(orderNumber=F('orderNumber') + 1)

                    current_todo.orderNumber = to_be_current_order
                    current_todo.save(update_fields=['orderNumber'])
                elif target_todo.orderNumber and current_todo.orderNumber:
                    target_todo_orderNumber = target_todo.orderNumber
                    current_todo_orderNumber = current_todo.orderNumber

                    if target_todo_orderNumber < current_todo_orderNumber:
                        need_to_modify_ordering_todo_set = todo_set.filter(orderNumber__lt=current_todo_orderNumber, orderNumber__gte=target_todo_orderNumber)
                        need_to_modify_ordering_todo_set.update(orderNumber=F('orderNumber') + 1)
                    elif target_todo_orderNumber > current_todo_orderNumber:
                        need_to_modify_ordering_todo_set = todo_set.filter(orderNumber__lte=target_todo_orderNumber, orderNumber__gt=current_todo_orderNumber)
                        need_to_modify_ordering_todo_set.update(orderNumber=F('orderNumber') - 1)

                    current_todo.orderNumber = target_todo_orderNumber
                    current_todo.save(update_fields=['orderNumber'])

            return Response(data={"message": "success"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class CompletedListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            completed_set = ToDo.objects.filter(
                author=request.user,
                completedDate__isnull=False,
            ).values()
            return Response(data={"completed_set": completed_set}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class CompletedTodayListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            completed_set = ToDo.objects.filter(
                author=request.user,
                completedDate__year=timezone.now().year,
                completedDate__month=timezone.now().month,
                completedDate__day=timezone.now().day,
            ).values()
            return Response(data={"completed_set": completed_set}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class CompletedDetailAPI(APIView):

    @mandatories('isCompleted')
    def put(self, request, id, m):
        if request.user.is_authenticated:
            isCompleted = m['isCompleted']

            try:
                todo = ToDo.objects.get(author=request.user, id=id)
                with transaction.atomic():
                    if not isCompleted:
                        todo.completedDate = timezone.now()
                        orderNumber = todo.orderNumber

                        ToDo.objects.filter(
                            author=request.user,
                            completedDate__isnull=True,
                            orderNumber__isnull=False,
                            orderNumber__gt=orderNumber
                        ).update(
                            orderNumber=F('orderNumber') - 1
                        )
                    else:
                        todo.completedDate = None

                        todo_qs = ToDo.objects.filter(
                            author=request.user,
                            completedDate__isnull=True,
                            orderNumber__isnull=False,
                        )
                        max_orderNumber = get_max_int_from_queryset(todo_qs, 'orderNumber')

                        if not max_orderNumber:
                            max_orderNumber = 1

                        todo.orderNumber = max_orderNumber + 1

                    todo.save()

                return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
