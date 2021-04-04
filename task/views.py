from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import UserProfile, Task
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from . forms import RegistrationForm, UserAuthenticationForm, TaskForm
import os, binascii
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from . serializers import TaskSerializer

# Create your views here.


# def home(request):
#     return render(request, "base.html", {})

def registration_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("task")
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_pass)
            user.key = binascii.hexlify(os.urandom(11)).decode()
            user.is_api_enabled = True
            user.save()
            login(request, user)
            messages.success(
                request, "You have been Registered as {}".format(request.user.username))
            return redirect('task')
        else:
            messages.error(request, "Please Correct Below Errors")
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, "register.html", context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("task")
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("task")
        else:
            messages.error(request, "Please Correct Below Errors")
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You're logged out")
    return redirect("task")


@login_required(login_url="login")
def tasklist(request):
    tasks = Task.objects.filter(task_user=request.user)
    if request.method == 'POST':
        title=request.POST.get('title')
        description = request.POST.get('description')
        category = int(request.POST.get('category'))
        due_date= request.POST.get('due_date')
        task=Task(task_user=request.user, title=title, description=description,
        category=category, due_date=due_date)
        task.save()
        return redirect("/")
    context = {
        'tasks': tasks,
    }
    return render(request, 'task/list.html', context)


@login_required(login_url="login")
def updatetask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'task/update_task.html', context)


@login_required(login_url="login")
def delete(request, pk):
    item = Task.objects.get(task_user=request.user, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request,'task/delete.html',context)


@login_required(login_url="login")
def api_view(request):
    user = request.user
    key = user.key
    context = {'apikey': key}
    return render(request, 'api.html', context)


@login_required(login_url="login")
def api_access(request):
    user = request.user
    key = binascii.hexlify(os.urandom(11)).decode()
    user.key = key
    user.save()
    return redirect("apiview")



class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return Task.objects.get(pk=pk, task_user=request.user)
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        try:
            task=self.get_object(request,pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, task_user=request.user)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        task = Task.objects.get(pk=pk, task_user=request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(task_user=self.request.user)
    
    def get(self, request):
        task = Task.objects.filter(task_user=self.request.user)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
