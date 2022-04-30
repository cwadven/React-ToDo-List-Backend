from datetime import (
    datetime,
    timedelta
)

from django.db import transaction, IntegrityError
from django.db.models import F, Q
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Todo.models import (
    ToDo,
    Category
)
from Todo.serializers import (
    CategoryListSerializer,
    CategoryCreateUpdateSerializer,
    ToDoListSerializer,
    ToDoCreateUpdateSerializer
)
from common_decorator import (
    mandatories,
    optionals
)
from common_library import (
    get_max_int_from_queryset,
    make_space_ordering_from_queryset
)


class CategoryListAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category_qs = request.user.category_set.all().order_by('orderNumber')
        category_set = CategoryListSerializer(category_qs, many=True).data

        return Response(data={"category_set": category_set}, status=status.HTTP_200_OK)

    @mandatories('name', 'orderNumber')
    def post(self, request, m):
        try:
            with transaction.atomic():
                serializer = CategoryCreateUpdateSerializer(
                    data={
                        "author": request.user.id,
                        "name": m['name'],
                        "orderNumber": m['orderNumber']
                    },
                    context={'request': request}
                )

                if serializer.is_valid():
                    category = serializer.save()
                    return Response(data={"message": "success", "id": category.id}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"message": serializer.errors}, status=status.HTTP_403_FORBIDDEN)

        except IntegrityError:
            return Response(data={"message": "category name already exists"}, status=status.HTTP_403_FORBIDDEN)


class CategoryDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @mandatories('name', 'orderNumber')
    def put(self, request, id, m):
        try:
            with transaction.atomic():
                orderNumber = int(m['orderNumber'])

                category = Category.objects.get(
                    id=id,
                    author=request.user
                )

                serializer = CategoryCreateUpdateSerializer(
                    category,
                    data={
                        "name": m['name'],
                        "orderNumber": orderNumber
                    },
                    context={'request': request}
                )
                if serializer.is_valid():
                    category = serializer.save()
                    return Response(data={"message": "success", "id": category.id}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"message": serializer.errors}, status=status.HTTP_403_FORBIDDEN)
        except Category.DoesNotExist:
            return Response(data={"message": "bad request"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        try:
            with transaction.atomic():
                user_category_set = request.user.category_set.all()

                category = user_category_set.get(id=id)
                user_category_set.filter(
                    orderNumber__gt=category.orderNumber
                ).update(
                    orderNumber=F('orderNumber') - 1
                )
                category.delete()
        except Category.DoesNotExist:
            return Response(data={"message": "bad request"}, status=status.HTTP_403_FORBIDDEN)

        return Response(data={"message": "success", "id": category.id}, status=status.HTTP_200_OK)


class ToDoListAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @optionals({'categoryId': None})
    def get(self, request, o):
        q = Q(author=request.user, completedDate__isnull=True)
        categoryId = o['categoryId']

        if o['categoryId'] == 'null':
            q &= Q(category__isnull=True)
        elif categoryId is not None:
            q &= Q(category_id=categoryId)

        todo_qs = ToDo.objects.select_related(
            'category'
        ).filter(
            q
        ).order_by(
            'orderNumber'
        )
        todo_set = ToDoListSerializer(todo_qs, many=True).data

        return Response(data={"todo_set": todo_set}, status=status.HTTP_200_OK)

    @mandatories('text')
    @optionals({'deadLine': None}, {'categoryId': None})
    def post(self, request, m, o):
        deadLine = o['deadLine']

        # 한국 9시간 더하기
        if deadLine:
            deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))

        serializer = ToDoCreateUpdateSerializer(
            data={
                "author": request.user.id,
                "startDate": timezone.now(),
                "deadLine": deadLine,
                "text": m['text'],
                "category": o['categoryId'],
            },
            context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response(data={"message": "success", "id": instance.id}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": serializer.errors}, status=status.HTTP_403_FORBIDDEN)


class ToDoDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @mandatories('text')
    @optionals({'deadLine': None}, {'categoryId': None})
    def put(self, request, id, m, o):
        deadLine = o['deadLine']

        # 한국 9시간 더하기
        if deadLine:
            deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))

        try:
            with transaction.atomic():
                todo = ToDo.objects.get(author=request.user, id=id)

                serializer = ToDoCreateUpdateSerializer(
                    todo,
                    data={
                        "deadLine": deadLine,
                        "text": m['text'],
                        "category": o['categoryId'],
                    },
                    context={'request': request}
                )

                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(data={"message": "success", "id": instance.id}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"message": serializer.errors}, status=status.HTTP_403_FORBIDDEN)
        except ToDo.DoesNotExist:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        try:
            with transaction.atomic():
                delete_todo = ToDo.objects.get(author=request.user, id=id)
                orderNumber = delete_todo.orderNumber

                if orderNumber:
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
        except Exception as e:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class ToDoOrderChangingAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @mandatories('currentId', 'targetId')
    def put(self, request, m):
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

                make_space_ordering_from_queryset(todo_set, current_todo_orderNumber, target_todo_orderNumber,
                                                  'orderNumber')

                current_todo.orderNumber = target_todo_orderNumber
                current_todo.save(update_fields=['orderNumber'])

        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


class CompletedListAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        completed_qs = ToDo.objects.select_related(
            'category'
        ).filter(
            author=request.user,
            completedDate__isnull=False,
        )
        completed_set = ToDoListSerializer(completed_qs, many=True).data
        return Response(data={"completed_set": completed_set}, status=status.HTTP_200_OK)


class CompletedTodayListAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        completed_qs = ToDo.objects.select_related(
            'category'
        ).filter(
            author=request.user,
            completedDate__year=timezone.now().year,
            completedDate__month=timezone.now().month,
            completedDate__day=timezone.now().day,
        )
        completed_set = ToDoListSerializer(completed_qs, many=True).data
        return Response(data={"completed_set": completed_set}, status=status.HTTP_200_OK)


class CompletedDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @mandatories('isCompleted')
    def put(self, request, id, m):
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
                    else:
                        max_orderNumber += 1

                    todo.orderNumber = max_orderNumber

                todo.save()

            return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
        except:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
