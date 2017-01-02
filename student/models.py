from __future__ import unicode_literals

from django.db import models
from university.models import Student

# Create your models here.
class StudentAuth(models.Model):
    student = models.OneToOneField(Student)
    username = models.CharField(max_length=30, default=None, null=False)
    password = models.CharField(max_length=30, default='123456', null=False)
    def __str__(self):
        return self.username
    def getStudent():
        if len(self.username) < 1:
            return Student()
        student = Student.objects.get()
