from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.context_processors import csrf
from university import settings
from student.models import *
from university.models import ExamReport

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

    student = {}
    student["id"] = current_student.student.pk
    student["full_name"] = str(current_student.student.first_name) + ' ' + str(current_student.student.middle_name) + ' '+ str(current_student.student.last_name)
    student["registered"] = current_student.student.registered

    student_auth = {}
    student_auth["id"] = current_student.pk
    student_auth["username"] = current_student.username

    student_info = {}

    student_info['student']= student
    student_info['student_auth']= student_auth
    return student_info

def get_exam_report(student_id=0, subject_id=0):
    if student_id == 0:
        return None
    if subject_id == 0:
        return None
    rp = ExamReport.objects.filter(student__pk=student_id, subject__pk=subject_id)
    report = {}
    report["items"] = []
    for r in rp:
        #report["items"][str(i)] = str(r)
        item = {}
        item["exam_type"] = r.exam.e_type.name
        item["subject"] = {
            "id": r.subject.id,
            "name":r.subject.name
        }
        item["grade"] = r.grade
        item["notes"] = r.note
        report["items"] += [item]
    if len(report["items"]) == 0:
        report["error"] = "No items found"
    return report
def get_report(request):
    student_id = request.GET.get('student_id', 0)
    subject_id = request.GET.get('subject_id', 0)
    if student_id < 1:
        try:
            student_id = request.session["loggedin_student"]
        except: return JsonResponse({"error": "student id is not provided"})

    subjects = generateExamReport(student_id, subject_id)
    if not subjects:
        return JsonResponse({"error": "items not available"})
    return JsonResponse({"items":subjects})

def get_exam_results(request):
    student_id = request.GET.get('student_id', 0)
    if student_id < 1:
        try:
            student_id = request.session["loggedin_student"]
        except: return render(request, 'students/get_exam_results.html',{"error": "either student is not loggedin or you didn't provide a valid id", 'settings':settings})

    subjects = generateExamReport(student_id, all=True)
    if not subjects:
        return render(request, 'students/get_exam_results.html',{"error": "items not available", 'settings':settings})
    return render(request, 'students/get_exam_results.html',{"items":subjects, 'settings':settings})

def generateExamReport(student_id=0, subject_id=0, all=False):
    if int(student_id) == 0:
        return {"error":"Invalid student id. Please login"}
    if int(subject_id) == 0 and all == False:
        return {"error":"Subject id is required"}
    if all == True:
        rp = ExamReport.objects.filter(student__pk=student_id)
    else:
        rp = ExamReport.objects.filter(student__pk=student_id, subject__pk=subject_id)
    subjects = {}
    for r in rp:
        # collect all subjects in this report
        s = 0
        try:
            s = len(subjects[r.subject.name])
        except:pass
        if s < 1:
            subjects[r.subject.name] = []
        subjects[r.subject.name] += [
            {
                "subject_name": r.subject.name,
                "exam_type":r.exam.e_type.name,
                "grade":r.grade, "notes":r.note
            }
        ]

    subject_exams = {}
    return subjects

def generateExamReport(student_id=0, subject_id=0, all=False):
    if int(student_id) == 0:
        return {"error":"Invalid student id. Please login"}
    if int(subject_id) == 0 and all == False:
        return {"error":"Subject id is required"}
    if all == True:
        rp = ExamReport.objects.filter(student__pk=student_id)
    else:
        rp = ExamReport.objects.filter(student__pk=student_id, subject__pk=subject_id)
    subjects = []
    for r in rp:
        # collect all subjects in this report
        s = 0
        try:
            s = len(subjects)
        except:pass
        if s < 1:
            subjects = []
        subjects += [
            {
                "subject_name": r.subject.name,
                "exam_type":r.exam.e_type.name,
                "grade":r.grade, "notes":r.note,
                "semester": r.semester
            }
        ]

    semesters = []
    for i in range(1, rp[0].student.classroom.current_semester.level):
        print("#{1}".format(i))
    return subjects


# student services
# NO LONGER USED NOW USING get_report(request) INSTEAD.
def checkmarks(request):
    print("checkmarks:")
    student_info = get_current_student(request)
    student_id = None
    try:
        student_id = student_info["student"]["id"]
    except Exception as e:
        print(e)
    if student_id == None:
        return JsonResponse({"error":"Invalid student id. Please login"})
    subject_id = request.GET.get('subject_id')
    print(subject_id)
    print(student_id)
    if int(subject_id) < 1:
        return JsonResponse({"error": "invalid subject id"})

    rp = get_exam_report(student_id=student_id, subject_id=subject_id)
    if rp is None:
        return JsonResponse({"error":"Invalid subject"})
    #return render(request, 'students/checkmarks.html',{})
    student_info["report"] = rp
    return JsonResponse(student_info, safe=False)
