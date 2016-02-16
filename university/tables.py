import django_tables2 as tables
from university.models import *

class ResultsTable(tables.Table):
    class Meta:
        model = ExamReport
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}