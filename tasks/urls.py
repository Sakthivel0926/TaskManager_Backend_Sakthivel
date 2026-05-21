from django.urls import path
from .views import (
    register_user,
    get_tasks,
    create_task,
    update_task,
    delete_task,
)

urlpatterns = [
    # 🔐 AUTH
    path('register/', register_user, name="register"),

    # 📌 TASKS
    path('tasks/', get_tasks, name="get_tasks"),
    path('tasks/create/', create_task, name="create_task"),
    path('tasks/update/<int:pk>/', update_task, name="update_task"),
    path('tasks/delete/<int:pk>/', delete_task, name="delete_task"),
]