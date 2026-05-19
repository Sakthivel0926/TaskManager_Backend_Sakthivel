from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


@api_view(['GET'])
def get_tasks(request):

    tasks = Task.objects.all().order_by('-created_at')

    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "Task created successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "message": "Failed to create task",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['PUT'])
def update_task(request, pk):

    try:
        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {
                "message": "Task not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(task, data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "Task updated successfully",
                "data": serializer.data
            }
        )

    return Response(
        {
            "message": "Failed to update task",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def delete_task(request, pk):

    try:
        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {
                "message": "Task not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    task.delete()

    return Response(
        {
            "message": "Task deleted successfully"
        },
        status=status.HTTP_200_OK
    )