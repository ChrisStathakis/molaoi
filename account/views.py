from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MyRegistrationForm

# Create your views here.

def log_in(request):
    c={}
    return render(request,'log_in.html',c)



def create_user(request):
    username = request.POST['username']
    password= request.POST['password']
    email =request.POST['email']
    user_auth = auth.authenticate(username=username,password=password)
    if user_auth is not None:
        auth.login(request,user_auth)
        return HttpResponseRedirect(request,'logged_in.html')
    else:
        return render(request,'invalid_log.html')



def auth_view(request):
    username = request.POST['username']
    password= request.POST['password']

    user = auth.authenticate(username=username,password=password)
    if user:
        auth.login(request,user)
        return HttpResponseRedirect('/accounts/logged_in/')
    else:
        return render(request,'invalid_log.html')

def logged_in(request):
    context = {
        'full_name':request.user.username
    }
    return render(request,'logged_in.html',context)


def logout(request):
    auth.logout(request)
    return render(request,'logout.html')


def register(request):
    if request.method =="POST":
        form=MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    args={}
    
    args['form'] = MyRegistrationForm()
    return render(request,'register.html', args)

