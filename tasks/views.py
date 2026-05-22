from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task
from .serializers import TaskSerializer


# REGISTER
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if User.objects.filter(username=username).exists():

        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):

    # ADMIN CAN SEE ALL TASKS
    if request.user.is_staff:

        tasks = Task.objects.all()

    else:

        # NORMAL USER SEES OWN TASKS
        tasks = Task.objects.filter(
            user=request.user
        )

    serializer = TaskSerializer(
        tasks,
        many=True
    )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# UPDATE TASK
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):

    try:
        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(
        task,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# DELETE TASK
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):

    try:
        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    task.delete()

    return Response(
        {"message": "Deleted successfully"},
        status=status.HTTP_200_OK
    )