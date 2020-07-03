
from django.shortcuts import render
from first_app.forms import Userform

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'first_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == 'POST':
        user_form =Userform(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()


            registered= True
        else:
            print(user_form.errors)

    else:
        user_form=Userform

    return render(request,'first_app/registration.html',{'user_form':user_form,'registered':registered})



def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")

        else:
            return HttpResponse("someone tried to login and failed")

    else:
        return render(request,'first_app/login.html',{})