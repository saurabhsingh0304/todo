from django.urls import path
from . import views as v

urlpatterns = [
    path('register', v.registration_view, name='register'),
    # path('home/',v.home , name='home'),
    path('login/',v.login_view, name='login'),
    path('logout/',v.logout_view, name='logout'),
    path('',v.tasklist, name='task'),
    path('update_task/<str:pk>/',v.updatetask,name='update_task'),
    path('delete/<str:pk>/',v.delete,name='delete_task'),
    path('task/',v.TaskView.as_view(), name='taskview'),
    path('task/<str:pk>/', v.TaskDetailView.as_view(), name="tasklistdetail"),
    path('api/',v.api_view, name="apiview"),
    path('reapi/',v.api_access, name="apiaccess")
]
