from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from Todo.models import ToDo


class ToDoListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            todo_set = ToDo.objects.filter(author=request.user, completedDate__isnull=True).values()
            return Response(data={"todo_set": todo_set}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            deadLine = request.data.get('deadLine')
            text = request.data.get('text')

            # 한국 9시간 더하기
            if deadLine:
                deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))
            else:
                deadLine = None

            todo = ToDo.objects.create(
                author=request.user,
                startDate=timezone.now(),
                deadLine=deadLine,
                text=text,
            )

            return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class ToDoDetailAPI(APIView):
    def put(self, request, id):
        if request.user.is_authenticated:
            deadLine = request.data.get('deadLine')
            text = request.data.get('text')

            # 한국 9시간 더하기
            if deadLine:
                deadLine = (datetime.strptime(deadLine, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=9))
            else:
                deadLine = None

            try:
                todo = ToDo.objects.get(author=request.user, id=id)
                todo.deadLine = deadLine
                todo.text = text
                todo.save()

                return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if request.user.is_authenticated:
            try:
                ToDo.objects.get(author=request.user, id=id).delete()
                return Response(data={"message": "success"}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)


class CompletedListAPI(APIView):
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
    def put(self, request, id):
        if request.user.is_authenticated:
            isCompleted = request.data.get('isCompleted')

            try:
                todo = ToDo.objects.get(author=request.user, id=id)
                if not isCompleted:
                    todo.completedDate = timezone.now()
                else:
                    todo.completedDate = None
                todo.save()

                return Response(data={"message": "success", "id": todo.id}, status=status.HTTP_200_OK)
            except:
                return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "No Auth"}, status=status.HTTP_401_UNAUTHORIZED)
