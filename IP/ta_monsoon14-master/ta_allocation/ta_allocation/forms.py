from django import forms

from django.forms.widgets import *
from ta_alloc.models import *

PROG = (
		('0','BTech'),
		('4','MTech 1st Year'),
		('5','MTech 2nd Year'),
		('7','PhD'),
		)

PROG2 = (
		('-1','Not Applicable'),
		('0','BTech'),
		('4','MTech 1st Year'),
		('5','MTech 2nd Year'),
		('7','PhD'),
		)

ALLUNALL = (
		('0','Unallocated'),
		('9','Allocated'),
		)

ROLES = (
	('0','Student'),
	('1','Professor'),
	('9','DOA'),
	('8','Admin'),
	)

SEMESTERS = (
	('1','Monsoon'),
	('2','Winter'),
	)
COURSE_TYPES = (
	('1','Core'),
	('2','Core Elective'),
	('3','Required Elective'),
	('4','Free Elective'),
	)

FIELD_NAME_MAPPING = {
    'cid':'Course Code','cname':'Course Name','cdesc':'Course Description','sem':'Semester','year':'Year','prof_id1':'Email ID of Professor1','prof_id2':'Email ID of Professor2','reg_no':'Number of Registrations','tutors_min':'Minimum number of Tutors','tutors_max':'Maximum number of Tutors','s_ta_min':'Minimum number of Senior TAs','s_ta_max':'Maximum number of Senior TAs','j_ta_min':'Minimum number of Junior TAs','j_ta_max':'Maximum number of Junior TAs','btech_ta_min':'Minimum number of BTech TAs','btech_ta_max':'Maximum number of BTech TAs','select_max':'Maximum TAs Instructor can select',
}
my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Characters and special characters are not allowed. Please enter the numeric part only!'
}
class p_form(forms.ModelForm):
	roll_no = forms.IntegerField(required=True,widget=forms.TextInput,error_messages=my_default_errors)
	name = forms.CharField(required=True,widget=forms.TextInput)
	program = forms.ChoiceField(choices = PROG)
	class Meta:
		model = student_general
		fields = ('roll_no','name','program')


# class allocation_form(forms.ModelForm):
# 	program_type = forms.ChoiceField(choices = PROG)
# 	allocation_type = forms.ChoiceField(choices = ALLUNALL)

class roles_form(forms.ModelForm):
	loginid = forms.CharField(required=True,widget=forms.TextInput)
	role = forms.ChoiceField(choices = ROLES)
	program = forms.ChoiceField(choices = PROG2)
	class Meta:
		model = role_list
		fields = ('loginid','role','program')


class UploadFileForm(forms.Form):
    file = forms.FileField()

class courses_form(forms.ModelForm):
	cid = forms.CharField(label="Course Code",required=True,widget=forms.TextInput)
	cname = forms.CharField(label="Course Name",required=True,widget=forms.TextInput)
	cdesc = forms.CharField(label="Course Description",required=False,widget=forms.TextInput)
	reg_no = forms.IntegerField(label="No of Registrations",required=False,widget=forms.TextInput)
	sem = forms.ChoiceField(label="Semester",required=True,choices = SEMESTERS)
	year = forms.IntegerField(label="Current Year",required=True,widget=forms.TextInput)
	prof_id1 = forms.CharField(label="Email ID of Professor1",required=True,widget=forms.TextInput)
	prof_id2 = forms.CharField(label="Email ID of Professor2(Blank if none)",required=False,widget=forms.TextInput)
	tutors_min = forms.IntegerField(label="Min no of PhD TAs",required=False,widget=forms.TextInput)
	tutors_max = forms.IntegerField(label="Max no of PhD TAs",required=False,widget=forms.TextInput)
	s_ta_min = forms.IntegerField(label="Min no of MTech2ndYear TAs",required=False,widget=forms.TextInput)
	s_ta_max = forms.IntegerField(label="Max no of MTech2ndYear TAs",required=False,widget=forms.TextInput)
	j_ta_min = forms.IntegerField(label="Min no of MTech1stYear TAs",required=False,widget=forms.TextInput)
	j_ta_max = forms.IntegerField(label="Max no of MTech1stYear TAs",required=False,widget=forms.TextInput)
	btech_ta_min = forms.IntegerField(label="Min no of BTech TAs",required=False,widget=forms.TextInput)
	btech_ta_max = forms.IntegerField(label="Max no of BTech TAs",required=False,widget=forms.TextInput)
	select_max = forms.IntegerField(label="Max TAs prof can shortlist",required=False,widget=forms.TextInput)
	course_type = forms.ChoiceField(label="Course Type",required=True,choices=COURSE_TYPES)
	# def add_prefix(self, field_name):
	# 	# look up field name; return original if not found
	# 	cid = FIELD_NAME_MAPPING.get(cid, cid)
	# 	cname = FIELD_NAME_MAPPING.get(cname, cname)
	# 	cdesc = FIELD_NAME_MAPPING.get(cdesc, cdesc)
	# 	sem = FIELD_NAME_MAPPING.get(sem, sem)
	# 	year = FIELD_NAME_MAPPING.get(year, year)
	# 	prof_id1 = FIELD_NAME_MAPPING.get(prof_id1, prof_id1)
	# 	prof_id2 = FIELD_NAME_MAPPING.get(prof_id2, prof_id2)
	# 	reg_no = FIELD_NAME_MAPPING.get(reg_no, reg_no)
	# 	tutors_min = FIELD_NAME_MAPPING.get(tutors_min, tutors_min)
	# 	tutors_max = FIELD_NAME_MAPPING.get(tutors_max, tutors_max)
	# 	s_ta_min = FIELD_NAME_MAPPING.get(s_ta_min, s_ta_min)
	# 	s_ta_max = FIELD_NAME_MAPPING.get(s_ta_max, s_ta_max)
	# 	j_ta_min = FIELD_NAME_MAPPING.get(j_ta_min, j_ta_min)
	# 	j_ta_max = FIELD_NAME_MAPPING.get(j_ta_max, j_ta_max)
	# 	btech_ta_min = FIELD_NAME_MAPPING.get(btech_ta_min, btech_ta_min)
	# 	btech_ta_max = FIELD_NAME_MAPPING.get(btech_ta_max, btech_ta_max)
	# 	select_max = FIELD_NAME_MAPPING.get(select_max, select_max)
	# 	return super(course, self).add_prefix(cid,cname,cdesc,sem,year,prof_id1,prof_id2,reg_no,tutors_min,tutors_max,s_ta_min,s_ta_max,j_ta_min,j_ta_max,btech_ta_min,btech_ta_max,select_max)
	class Meta:
		model = course
		fields = ('cid','cname', 'cdesc', 'sem', 'year', 'tutors_min', 'tutors_max', 's_ta_min', 's_ta_max', 'j_ta_min','j_ta_max','btech_ta_min','btech_ta_max','select_max')
