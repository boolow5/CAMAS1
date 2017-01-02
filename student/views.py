from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from university import settings
from student.models import *

# Create your views here.
def index(request):
    print("Student Index")
    if request.user.is_authenticated():
        #return render(request, 'students/index.html',{'settings':settings})
        return redirect('/cms')
    else:
        context = {'settings':settings, 'student_user':True}
        if is_student_authenticated(request):
            context["loggedin_student"] = True
        current_student = get_current_student(request)
        if current_student is None:
            context["current_student"] = current_student
        return render(request, 'students/index.html',context)


#student views
def login(request):
    print("Student Login")
    context = {'settings':settings, 'student_user':True}
    if is_student_authenticated(request):
        print("You're already logged in")
        redirect('/')
    return render(request,'students/login.html',context)

def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    student_id = authenticate(username=username, password=password)

    if student_id != 0:
        request.session["loggedin_student"] = student_id
        return redirect('/student/loggedin')
    else:
        # contex = {}
        # contex.update(csrf(request))
        return redirect('/student/invalid')

def loggedin(request):
    print("Student Logged In")
    context = {
        'settings':settings,
        'student_user':True,
        'username':request.user.username,
    }
    if is_student_authenticated(request):
        context["loggedin_student"] = True
    return render(request,'students/loggedin.html', context)

def invalid_login(request):
    print("Student Invalid Login")
    context = {'settings':settings, 'student_user':True}
    if is_student_authenticated(request):
        context["loggedin_student"] = True
    return render(request,'students/invalid.html',context)

def logout(request):
    print("Student Logout")
    loggedin_student = is_student_authenticated(request)
    context = {'settings':settings, 'student_user':True, 'loggedin_student':loggedin_student}
    try:
        del request.session["loggedin_student"]
        print("loggedout_student")
        print(request.session["loggedin_student"])
    except: pass
    return render(request,'students/logout.html',context)

# custom Functions
def authenticate(username="", password=""):
    print("Student Authenticate")
    # search student with user name
    student_user = None
    try:
        student_user = StudentAuth.objects.get(username=username)
    except: pass
    # if student is not null
    if student_user is not None:
        # compare the password of the database object and user entered password
        if student_user.password == password:
            # if object has pk return that
            if student_user.pk > 0:
                return student_user.pk
    # else return 0
    return 0
def is_student_authenticated(request):
    print("is_student_authenticated:")
    loggedin_student = get_current_student(request)
    if loggedin_student is not None:
        print(loggedin_student)
        print("")
        return True
    else:
        return False

def get_current_student(request):
    print("Get Current Student")
    student_id = 0
    try:
        student_id = request.session["loggedin_student"]
    except:pass
    if student_id is None or student_id < 1:
        print("STUDENT NOT FOUND IN SESSION")
        return None
    current_student = None
    try:
        current_student = StudentAuth.objects.get(pk=student_id)
    except:
        print("ERROR: STUDENT NOT IN DATABASE")
    if current_student is None:
        print("STUDENT NOT FOUND")
        return None

    student_info = {
        'student': current_student.student,
        'student_auth': current_student
    }
    return student_info

# student services
def checkmarks(request):
    return render(request, 'students/checkmarks.html',{})
