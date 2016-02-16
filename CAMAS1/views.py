from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from university import settings


#user views
#Session['settings'] = settings
def login(request):
    return render(request,'user/login.html',{'settings':settings})

def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)        
        return HttpResponseRedirect('/users/loggedin')
    else:
        contex = {}
        contex.update(csrf(request))
        return HttpResponseRedirect('/users/invalid')

def loggedin(request):
    return render(request,'user/loggedin.html', {'username':request.user.username,'settings':settings})

def invalid_login(request):
    return render(request,'user/invalid.html',{'settings':settings})

def logout(request):
    auth.logout(request)
    return render(request,'user/logout.html',{'settings':settings})
