from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Subject(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    def setName(self, name):
        if len(name) > 1:
            self.name = name
            self.name[:2].upper()+str(self.id)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.IntegerField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User)
    subject = models.ForeignKey(Subject, default=None, null=True)
    position = models.ForeignKey(Position, null=True)

    def __str__(self):
        if self.user is not None:
            if len(self.user.first_name) and len(self.user.last_name):
                return self.user.first_name + ' ' + self.user.last_name
            else:
                return self.user.username
        else: return "[None user chosen yet.]"

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    dean = models.ForeignKey(Employee, null=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)
    def __str__(self):
        return self.name

#student1 related models

class Year(models.Model):
    name = models.CharField(max_length=30, unique=True)
    level = models.IntegerField(default=1, unique=True)

    def __str__(self):
        return str(self.name) + ' year'

class Term(models.Model):
    name = models.CharField(max_length=30, unique=True)
    level = models.IntegerField(default=1, unique=True)

    def __str__(self):
        return str(self.name) + ' semester'


class Classroom(models.Model):
    name = models.CharField(max_length=30, default='One')
    current_semester = models.ForeignKey(Term)
    date_opened = models.DateField(default= timezone.now)
    max_semesters = models.IntegerField(default=4, null=False)
    department = models.ForeignKey(Department, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def graduate(self):
        # check if this is the last year
        if self.max_semesters == self.current_semester:
            # set classroom status to false
            self.status = false

            # if it's not the last year
        elif self.current_semester < self.max_semesters:
            self.current_semester += 1
    def getCurrentYear(self):
        if self.current_semester < 2:
            return 1
        elif self.current_semester < 4:
            return 2
        elif self.current_semester < 6:
            return 3
        elif self.current_semester < 8:
            return 4
        elif self.current_semester < 10:
            return 6
        elif self.current_semester < 12:
            return 7
        elif self.current_semester < 14:
            return 8

class classSubjects(models.Model):
    classroom = models.ForeignKey(Classroom)
    year = models.ForeignKey(Year)
    semester = models.ForeignKey(Term)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return str(self.classroom) + ' subjects in ' + str(self.year) + '(' + str(self.semester) + ')'


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DateOfBirth = models.DateField(verbose_name='Date of Birth')
    address = models.TextField(default=None)
    phone = models.CharField(max_length=30)
    guardian = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    registered = models.DateField(default = timezone.now)
    registered_by = models.ForeignKey(User)
    classroom = models.ForeignKey(Classroom)
    fee = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

class Account(models.Model):
    owner = models.OneToOneField(Student)
    number = models.AutoField(primary_key=True)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)

    def __str__(self):
        return str(self.owner) + "'s account"

class Transaction(models.Model):
    received_by = models.ForeignKey(User)
    payee = models.ForeignKey(Account)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)
    date = models.DateTimeField(default = timezone.now)
    description = models.TextField(max_length=300)
    is_debit = models.BooleanField(default=True)

    def __str__(self):
        if self.is_debit:
            return '$' + str(self.amount)
        else:
            return "($" + str(abs(self.amount)) +')'

class BillType(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True)
    is_auto_generated = models.BooleanField(default=False)
    generation_day = models.IntegerField(default=1)

    def __str__(self):
        if not self.is_auto_generated:
            return self.name
        else:
            return self.name + "(Autogenerated)"


class Bill(models.Model):
    account = models.ForeignKey(Account)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.0)
    description = models.TextField(max_length=300)
    date = models.DateField(default=timezone.now)
    type = models.ForeignKey(BillType, default=1)
    created_by = models.ForeignKey(Employee)

    def __str__(self):
        return self.type.name + ' of ' + str(self.amount) + ' to ' + str(self.account)

class ExamType(models.Model):
    name = models.CharField(max_length=50)
    max_marks = models.DecimalField(decimal_places=2, max_digits=5, default=100.0)

    def __str__(self):
        return self.name


class Exam(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_date = models.DateField(default=timezone.now)
    year = models.ForeignKey(Year, null=True)
    semester = models.ForeignKey(Term, null=True)
    e_type = models.ForeignKey(ExamType)
    is_admission = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ExamReport(models.Model):
    exam = models.ForeignKey(Exam)
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(Student)
    semester = models.ForeignKey(Term, default=1, null=True)
    grade = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    date = models.DateField(default=timezone.now)
    modified = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default="OK", null=True)

    def __str__(self):
        return str(self.student) + " scored " + str(self.grade) + " in " + str(self.subject.name) + " in " + str(self.exam)
class ErrorReport(models.Model):
    message=models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now)
    current_user = models.ForeignKey(Employee)
