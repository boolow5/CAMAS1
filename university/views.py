from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response,\
    get_object_or_404
from django.template.context_processors import request
from university import settings
from django.utils import timezone
from django.contrib.auth import user_logged_in
#from django_tables2   import RequestConfig
from university.models import *
from university.forms import *
from university.tables import *
from student.views import generateExamReport

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html',{'settings':settings})
    else:
        return redirect('/users/login') #render(request, 'user/login.html',{'settings':settings})


def aboutus(request):
    return render(request, 'about.html', {'settings':settings})

def teachers_list(request):
    if request.user.is_authenticated():
        teachers = Employee.objects.filter(user__is_active = True)
        return render(request, 'teacher/teachers_list.html', {'teachers':teachers,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def teacher_profile(request, pk):
    if request.user.is_authenticated():
        teacher = Employee.objects.get(pk=pk)
        return render(request, 'teacher/teacher_profile.html', {'teacher': teacher,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def register_teacher(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == "POST":
                form = EmployeeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('/')
            else:
                form = EmployeeForm()
        except:
            error = 'Please enter a valid data before you submit!'

        return render(request, 'teacher/new_teacher.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def update_teacher(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            teacher = get_object_or_404(Employee, pk=pk)
            if request.method == 'POST':
                form = EmployeeForm(request.POST, instance=teacher)
                if form.is_valid():
                    teacher = form.save(commit=False)
                    teacher.registered_by = request.user
                    teacher.last_updated = timezone.now()
                    teacher.save()
                    return redirect('university.views.teacher_profile', pk=teacher.pk)
            else:
                form = EmployeeForm(instance=teacher)
        except:
            error = 'Please fill all required fields before you submit!'
        return render(request, 'teacher/edit_teacher.html', {'form':form,'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})


def deactivate_teacher(request, pk):
    if request.user.is_authenticated():
        teacher = get_object_or_404(Employee, pk=pk)
        if request.method == 'POST':
            teacher.status = False
            teacher.last_updated = timezone.now()
            teacher.save()
        return redirect('university.views.teacher_profile', pk=teacher.pk)
    else:return render(request, 'user/login.html',{'settings':settings})

#student related views
def students_list(request):
    if request.user.is_authenticated():
        students = Student.objects.all()

        return render(request, 'student/students_list.html', {'students':students,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def students_search(request):
    if request.user.is_authenticated():
        search = request.GET['filter']
        query = Q(id__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(middle_name__icontains=search)
        students = Student.objects.filter(query)

        return render(request, 'student/students_list.html', {'students':students,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})


def student_profile(request, pk):
    if request.user.is_authenticated():
        student = Student.objects.get(pk=pk)
        return render(request, 'student/student_profile.html', {'student': student,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def register_student(request):
    if request.user.is_authenticated():
        error = None
        #try:
        if request.method == "POST":
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.registered_by = request.user
                student.last_updated = timezone.now()
                student.save()
                ac = Account()
                ac.owner = student
                ac.save()
                return redirect('university.views.student_profile', pk=student.pk)
        else:
            form = StudentForm()
        #except:
            #error = "Please make sure you entered all required field's data"

        return render(request, 'student/new_student.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def update_student(request, pk):
    if request.user.is_authenticated():
        error=None
        try:
            student = get_object_or_404(Student, pk=pk)
            if request.method == 'POST':
                form = StudentForm(request.POST, instance=student)
                if form.is_valid():
                    student = form.save(commit=False)
                    student.registered_by = request.user
                    student.last_updated = timezone.now()
                    student.save()
                    return redirect('university.views.student_profile', pk=student.pk)
            else:
                form = StudentForm(instance=student)
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'student/edit_student.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})


#payment related views
def create_account(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == 'POST':
                form = AccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('/cms/accounts')
            else:
                form = AccountForm()
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'account/new_account.html', {'form':form,'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def accounts_list(request):
    if request.user.is_authenticated():
        accounts = Account.objects.all()
        return render(request, 'account/accounts_list.html', {'accounts':accounts})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def account_details(request, pk):
    if request.user.is_authenticated():
        account = Account.objects.get(pk=pk)
        return render(request, 'account/account_details.html', {'account':account})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def student_account_details(request, pk):
    if request.user.is_authenticated():
        account = Account.objects.get(owner=pk)
        return render(request, 'account/account_details.html', {'account':account})
    else:
        return render(request, 'user/login.html',{'settings':settings})


def edit_account(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            account = get_object_or_404(Account, pk=pk)
            if request.method == 'POST':
                form = AccountForm(request.POST, instance=account)
                if form.is_valid():
                    account = form.save()
                    return redirect('university.views.account_details', pk=account.pk)
            else:
                form = AccountForm(instance=account)
        except:
            error = 'Please enter a valid values into the fields!'
        return render(request, 'account/edit_account.html', {'form':form, 'account':account,'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def add_payment(request):
    if request.user.is_authenticated():
        form = TransactionForm(request.POST)
        try:
            if request.method == 'POST':
                if form.is_valid():
                    payment = form.save(commit=False)
                    if payment.amount > 0:
                        payment.is_debit = True
                    elif payment.amount < 0:
                        payment.is_debit = False
                    else:
                        form = TransactionForm()
                        return render(request, 'payment/new_payment.html', {'form':form, 'error':"Amount cannot be zero!",'settings':settings})
                    acount = Account.objects.get(pk= payment.payee.pk)
                    acount.balance += payment.amount
                    payment.received_by = request.user
                    payment.save()
                    acount.save()
                    return redirect('university.views.payment_details', pk=payment.pk)
            else:
                form = TransactionForm()
                return render(request, 'payment/new_payment.html', {'form':form})
        except:
            pass
        return render(request, 'payment/new_payment.html', {'form':form,'error':'Please enter valid values for each field!','settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def payments_list(request, pk=0):
    if request.user.is_authenticated():
        if pk==0:
            payments = Transaction.objects.filter(received_by = request.user)
            receiver = None
            try:
                receiver = Employee.objects.get(user = request.user)
            except:pass
            return render(request, 'payment/payments_list.html', {'payments':payments,'receiver':receiver})
        else:
            payments = Transaction.objects.filter(payee = pk)
            owner = Account.objects.get(owner=pk)
            return render(request, 'payment/payments_list.html', {'payments':payments,'owner':owner})
    else:
        return render(request, 'user/login.html')

def payment_details(request,pk):
    if request.user.is_authenticated():
        payment = get_object_or_404(Transaction, pk=pk)
        payment.amount = abs(payment.amount)
        owner = get_object_or_404(Account, pk=payment.payee.pk)
        return render(request, 'payment/payment_details.html', {'payment':payment, 'owner':owner,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

#exam related views
def create_exam(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == 'POST':
                form = ExamForm(request.POST)
                if form.is_valid():
                    exam = form.save()
                    return redirect('/cms/exams')
            else:
                form = ExamForm()
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/new_exam.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exams_list(request):
    if request.user.is_authenticated():
        exams = Exam.objects.all()
        return render(request, 'exam/exams_list.html', {'exams':exams,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exam_details(request, pk):
    if request.user.is_authenticated():
        exam = Exam.objects.get(pk=pk)
        return render(request, 'exam/exam_details.html', {'exam':exam,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def edit_exam(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            exam = get_object_or_404(Exam, pk=pk)
            if request.method == 'POST':
                form = ExamForm(request.POST, instance=exam)
                if form.is_valid():
                    exam = form.save()
                    return redirect('university.views.exam_details', pk=exam.pk)
            else:
                form = ExamForm(instance=exam)
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/edit_exam.html', {'form':form, 'exam':exam, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

#exam types
def create_exam_type(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == 'POST':
                form = ExamTypeForm(request.POST)
                if form.is_valid():
                    exam_type = form.save()
                    return redirect('university.views.exam_type_details', pk=exam_type.pk)
            else:
                form = ExamTypeForm()
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/new_exam_type.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})


def exam_types_list(request):
    if request.user.is_authenticated():
        exam_types = ExamType.objects.all()
        return render(request, 'exam/exam_types_list.html', {'exam_types':exam_types})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exam_type_details(request, pk):
    if request.user.is_authenticated():
        exam_type = ExamType.objects.get(pk=pk)
        return render(request, 'exam/exam_type_details.html', {'exam_type':exam_type})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def edit_exam_type(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            exam_type = get_object_or_404(ExamType, pk=pk)
            if request.method == 'POST':
                form = ExamTypeForm(request.POST, instance=exam_type)
                if form.is_valid():
                    exam_type = form.save()
                    return redirect('university.views.exam_details', pk=exam_type.pk)
            else:
                form = ExamForm(instance=exam_type)
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/edit_exam_type.html', {'form':form, 'exam_type':exam_type, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})
#
#exam report
def create_exam_report(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == 'POST':
                form = ExamReportForm(request.POST)
                if form.is_valid():
                    exam_report = form.save(commit=False)
                    exam_report.date = timezone.now()
                    return redirect('university.views.exam_report_details', pk=exam_report.pk)
            else:
                form = ExamReportForm()
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/new_exam_report.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exam_reports_list(request):
    if request.user.is_authenticated():
        exam_reports = ExamReport.objects.all()
        return render(request, 'exam/exam_reports_list.html', {'exam_reports':exam_reports,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exam_report_details(request, pk):
    if request.user.is_authenticated():
        exam_report = ExamReport.objects.get(pk=pk)
        minimum = (exam_report.exam.e_type.max_marks / 2)
        return render(request, 'exam/exam_report_details.html', {'exam_report':exam_report, 'minimum':minimum,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def edit_exam_report(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            exam_report = get_object_or_404(ExamReport, pk=pk)
            if request.method == 'POST':
                form = ExamReportForm(request.POST, instance=exam_report)
                if form.is_valid():
                    exam_report = form.save()
                    return redirect('university.views.exam_report_details', pk=exam_report.pk)
            else:
                form = ExamReportForm(instance=exam_report)
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'exam/edit_exam_report.html', {'form':form, 'exam_report':exam_report, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def student_exam_report(request, pk, semester=1):
    if request.user.is_authenticated():
        #t = generate_exam_marks_table(pk=pk, semester=semester)
        student =  Student.objects.get(pk=pk)
        student_id = request.GET.get('student_id', 0)
        subject_id = request.GET.get('subject_id', 0)
        if student_id < 1:
            try:
                student_id = request.session["loggedin_student"]
            except: return render(request,'exam/student_exam_report2.html', {'student':student,'semester':semester,'error':"student id is not provided", 'settings':settings})

        results = generateExamReport(student_id, subject_id)

        if int(semester) <= student.classroom.current_semester.level:
            #return render(request,'exam/student_exam_report2.html', {'student':student,'semester':semester,'subjects':subjects, 'settings':settings})
            return render(request,'exam/student_exam_report2.html', {"results": results,'student':student,'semester':semester, 'settings':settings})
        else:
            return render(request,'exam/student_exam_report2.html', {'student':student,'semester':semester,'error':'The semester you requested is not yet!', 'settings':settings})

    else:
        return render(request, 'user/login.html',{'settings':settings})

def get_subject_results(subject_id, student_id, year_id, semester_id):
        subject_results = ExamReport.objects.filter(subject__pk=subject_id,student__pk=student_id,semester__pk=semester_id)


def class_exam_report(request, class_pk, exam_pk):
    if request.user.is_authenticated():
        exam_report = ExamReport.objects.filter(student__classroom=class_pk, exam = exam_pk)
        return render(request,'exam/student_exam_report.html', {"exam_report":exam_report})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def exam_exam_report(request, exam_pk):
    if request.user.is_authenticated():
        exam_report = ExamReport.objects.filter(exam = exam_pk)
        return render(request,'exam/student_exam_report.html', {"exam_report":exam_report})
    else:
        return render(request, 'user/login.html',{'settings':settings})

#
#exam report

def classroom_details(request, pk):
    if request.user.is_authenticated():
        classroom = Classroom.objects.get(pk=pk)
        return render(request, 'class/classroom_details.html', {'classroom':classroom,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

#subjects
def create_subject(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.method == 'POST':
                form = SubjectForm(request.POST)
                if form.is_valid():
                    subject = form.save()
                    return redirect('university.views.subject_details', pk=subject.pk)
            else:
                form = SubjectForm()
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'subject/new_subject.html', {'form':form, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def subjects_list(request):
    if request.user.is_authenticated():
        subjects = Subject.objects.all()
        return render(request, 'subject/subjects_list.html', {'subjects':subjects,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def subject_details(request, pk):
    if request.user.is_authenticated():
        subject = Subject.objects.get(pk=pk)
        return render(request, 'subject/subject_details.html', {'subject':subject,'settings':settings})
    else:
        return render(request, 'user/login.html',{'settings':settings})

def edit_subject(request, pk):
    if request.user.is_authenticated():
        error = None
        try:
            subject = get_object_or_404(Subject, pk=pk)
            if request.method == 'POST':
                form = SubjectForm(request.POST, instance=subject)
                if form.is_valid():
                    subject = form.save()
                    return redirect('university.views.subject_details', pk=subject.pk)
            else:
                form = SubjectForm(instance=subject)
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'subject/edit_subject.html', {'form':form, 'subject':subject, 'error':error,'settings':settings})
    else:
        return render(request, 'user/login.html')


# Billing related View

def new_bill_type(request):
    if request.user.is_authenticated():
        error = None
        try:
            if request.user.is_superuser:
                if request.method == 'POST':
                    form = BillTypeForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('/cms/bill_types')
                else:
                    form = BillTypeForm()
            else:
                error = "Sorry you don't have enough authority to do this task."
                return render(request, 'bills/new_bill_type.html', {'form':form,'error':error})
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'bills/new_bill_type.html', {'form':form,'error':error})
    else:
        return render(request, 'user/login.html')

def edit_bill_type(request,pk):
    if request.user.is_authenticated():
        error = None
        try:
            if request.user.is_superuser:

                bill_type = get_object_or_404(BillType, pk=pk)
                if request.method == 'POST':
                    form = BillTypeForm(request.POST, instance=bill_type)
                    if form.is_valid():
                        bill_type = form.save()
                        return redirect('university.views.account_details', pk=bill_type.pk)
                else:
                    form = BillTypeForm(instance=bill_type)

                return render(request, 'bills/new_bill_type.html', {'form':form,'error':error})

            else:
                error = "Sorry you don't have enough authority to do this task."
                return render(request, 'bills/new_bill_type.html', {'form':form,'error':error})
        except:
            error = "Please make sure you entered all required field's data"

        return render(request, 'bills/new_bill_type.html', {'form':form,'error':error})
    else:
        return render(request, 'user/login.html')


def bill_type_list(request):
    if request.user.is_authenticated():
        error = None
        try:
            bill_types = BillType.objects.all()
        except:
            if bill_types == None or bill_types.count()==0:
                error = "Sorry no bill types available yet, contact the system admin to register them."

        return render('bills/bill_type_list.html',{'bill_types':bill_types, 'error':error})
    else:
        return render(request, 'user/login.html')

def generate_auto_bills(request):
    try:
        accounts = Account.objects.filter(owner__status=True)
        bill_types = BillType.objects.filter(is_auto_generated=True)

        for bill_type in bill_types:
            for ac in accounts:
                print(ac.number)
                newBill = Bill()
                newBill.account = ac
                newBill.description = bill_type.name + ' of '
                date = timezone.now()
                newBill.created_by = Employee.objects.get(pk=1)
                newBill.type = bill_type
                newBill.save()
                print("Done!")
    except Exception as e:
        print("Sorry! auto bill failed.")
        error = ErrorReport()
        error.message = e
        error.date = timezone.now()
        error.current_user = request.user
        error.save()

def generate_exam_marks_table(pk=0, year=1, semester=1):
    if pk == 0:
        return 'Invalid student id'

    student =  None
    try:
        student = Student.objects.get(pk=pk)
    except: pass

    print("student:")
    print(student)

    if student is None:
        return 'Student unavailable'

    try:
        subs = classSubjects.objects.get(classroom = student.classroom, year = year, semester = semester)
        subjects = subs.subjects.all()
        print("classSubjects:")
        print(subs.subjects[0])
    except Exception as e:
        print("Exception:", e)
        subjects = []
    subject_list = ""
    print("subjects:")
    print(subjects)

    results = []
    totals = []
    cw_results = []
    mt_results = []
    fn_results = []
    table = '<table>'

    for subject in subjects:
        subject_list+=str(subject.name) + ','
        #results.append(ExamReport.objects.filter(exam__e_type__gt=1,subject=subject, student=student).order_by('exam__e_type'))
        cw_results.append(ExamReport.objects.filter(exam__e_type=3,subject=subject, student=student, exam__year=year,exam__semester=semester).order_by('exam__e_type'))
        mt_results.append(ExamReport.objects.filter(exam__e_type=2,subject=subject, student=student, exam__year=year,exam__semester=semester).order_by('exam__e_type'))
        fn_results.append(ExamReport.objects.filter(exam__e_type=4,subject=subject, student=student, exam__year=year,exam__semester=semester).order_by('exam__e_type'))





    head = ['Subject','Class work 1', 'Mid-term', 'Class work 2', 'Final','Total']
    rows = []

    for i in range(len(subjects)):
        sub_total = 0
        row = []
        row.append(subjects[i])

        if len(cw_results[i]) != 0:
            try:
                sub_total += cw_results[i][0].grade
                row.append(str(cw_results[i][0].grade))
            except:pass
        else:
            row.append('')

        if len(mt_results[i]) != 0:
            try:
                sub_total += mt_results[i][0].grade
                row.append(str(mt_results[i][0].grade))
            except:pass
        else:
            row.append('')

        if len(cw_results[i]) ==2:
            try:
                sub_total += cw_results[i][1].grade
                row.append(str(cw_results[i][1].grade))
            except:pass

        else:
            row.append('')


        if len(fn_results[i]) != 0:
            try:
                sub_total += fn_results[i][0].grade
                row.append(str(fn_results[i][0].grade))
            except:pass
        else:
            row.append('')

        row.append(str(sub_total))
        totals.append(sub_total)


        rows.append(row)

    #Building table from the above data

    table = '<table><thead><tr>'
    for h in head:
        table += '<td>' + str(h) + '</td>'

    table += '</tr></thead><tbody>'

    for i in range(len(rows)):
        table += '<tr>'

        for j in range(len(rows[i])):
            table += '<td>' + str(rows[i][j]) + '</td>'
        table += '</tr>'
    table += '</tbody></table>'

    t = '<table>\n<thead><tr><td>name</td><td>age</td><td>sex</td></tr></thead><tbody><tr><td>mahdi</td><td>27</td><td>M</td></tr><tr><td>muno</td><td>23</td><td>F</td></tr></tbody></table>'
    return table
