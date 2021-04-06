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
    path('api/', v.api_view, name="apiview"),
    path('reapi/', v.api_access, name="apiaccess"),
    # api urls
    path('task/',v.TaskView.as_view(), name='taskview'),
    path('task/<str:pk>/', v.TaskDetailView.as_view(), name="tasklistdetail"),

]
"""
The last 2 urls for apis

for api authentication i made custom authentication in task\authentication.py

to access the task from a user you need an apikey (key field in UserProfile model) 
for authentication
apikey = xxxxxxxxxxxxxxxxx
url = http://127.0.0.1:8000/task/?api_key=xxxxxxxxxxxxxxxxx

for particular task of a user url need task id
id=y
url = http://127.0.0.1:8000/task/y/?api_key=xxxxxxxxxxxxxxxxx



"""
