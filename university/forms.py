from django.forms.models import ModelForm
from .models import *
from django import forms


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('user', 'subject', 'position')

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ('name', 'description', 'level')

        
class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ('name','description', 'dean')
        
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ('name','faculty')
        
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ('name','description')
#student1 related forms

class StudentForm(ModelForm):
    
    class Meta:
        model = Student
        help_texts = {
            'DateOfBirth': 'eg. 1999-06-01',
        }
        fields = ('first_name', 'middle_name', 'last_name','DateOfBirth', 'phone', 'address', 'guardian', 'guardian_phone', 'classroom','fee', 'status')
        
  
class YearForm(ModelForm):
    class Meta:
        model = Year
        fields = ('name','level')
        
class ClassroomForm(ModelForm):
    
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Classroom
        fields = ('name','current_year','current_semester','max_year', 'status','subjects')
        
class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ('number', 'owner')
        
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('payee','amount','description')

class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('amount', 'description')
        
class BillTypeForm(ModelForm):
    class Meta:
        model = BillType
        fields = ('name', 'description', 'is_auto_generated', 'generation_day')

class ExamTypeForm(ModelForm):
    class Meta:
        model = ExamType
        fields = ('name', 'max_marks')
        
class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = ('title', 'description', 'starting_date', 'e_type', 'is_admission')

class ExamReportForm(ModelForm):
    note = forms.CharField(required=False)
    class Meta:
        model = ExamReport
        fields = ('exam', 'subject', 'student', 'grade', 'note')
