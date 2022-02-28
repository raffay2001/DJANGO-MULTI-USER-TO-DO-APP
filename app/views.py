from cmath import polar
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from app.models import TODO
from .forms import TODOForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login/')
def home(request):
    if request.user.is_authenticated:   
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        context = {
            "form" : form,
            "todos" : todos,
        }
        return render(request, 'index.html', context=context)
    
@login_required(login_url='login/')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        context = {
            "form" : form,
        }
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return HttpResponseRedirect(reverse('app:home'))
        else:
            return render(request, 'index.html', context)


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = {
            "form" : form,
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        context = {
            "form" : form,
        }
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return HttpResponseRedirect(reverse('app:home'))
        else:
            return render(request, 'login.html', context=context)


@login_required(login_url='login/')
def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk = id).delete()
    return HttpResponseRedirect(reverse('app:home'))

@login_required(login_url='login/')
def change_status(request, id, status):
    todo = TODO.objects.get(pk = id)
    if status == 'P':
        todo.status = 'C'
    elif status == 'C':
        todo.status = 'P'
    todo.save()
    return HttpResponseRedirect(reverse('app:home'))
    

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form,
        }
        return render(request, 'signup.html', context=context)
    else:
        print(f'{request.POST}')
        form = UserCreationForm(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                redirect_url = reverse('app:login')
                print(f'The Reversed URL is: "{redirect_url}"')
                return HttpResponseRedirect(redirect_url)

        else:
            return render(request, 'signup.html', context=context)

def logout(request):
    logoutUser(request)
    return HttpResponseRedirect(reverse('app:login'))