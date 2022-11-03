from django.contrib.auth.views import LogoutView
from django.urls import path

from base.views import TaskList, TaskDetail, TaskCreateView, TaskUpdateView, TaskDeleteView, UserLogin, UserRegister

urlpatterns = [
    path("", TaskList.as_view(), name="home"),
    path("task/<int:pk>", TaskDetail.as_view(), name="details"),
    path("task/", TaskCreateView.as_view(), name="task_create"),
    path("task-update/<int:pk>", TaskUpdateView.as_view(), name="task_update"),
    path("task-delete/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),
    path("task/login", UserLogin.as_view(), name="user_login"),
    path("task/logout", LogoutView.as_view(next_page='user_login'), name="user_logout"),
    path("task/register", UserRegister.as_view(), name="register"),
]
