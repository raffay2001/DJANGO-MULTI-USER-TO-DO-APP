from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser

# Create your views here.

def home(request):
    return render(request, 'index.html')


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
    