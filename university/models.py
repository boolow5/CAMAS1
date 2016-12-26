from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

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
            return self.user.first_name + ' ' + self.user.last_name
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
    name = models.CharField(max_length=30)
    level = models.IntegerField()

    def __str__(self):
        return str(self.name) + ' year'

class Term(models.Model):
    is_first = models.BooleanField(default=True)
    name = models.CharField(max_length=30)


    def __str__(self):
        return str(self.name) + ' semester'



class Classroom(models.Model):
    name = models.CharField(max_length=30, default='One')
    current_year = models.ForeignKey(Year)
    current_semester = models.ForeignKey(Term)
    date_opened = models.DateField(default= timezone.now)
    max_year = models.IntegerField(default=4)
    department = models.ForeignKey(Department, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

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
    grade = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    date = models.DateField(default=timezone.now)
    modified = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return str(self.grade)
class ErrorReport(models.Model):
    message=models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now)
    current_user = models.ForeignKey(Employee)
