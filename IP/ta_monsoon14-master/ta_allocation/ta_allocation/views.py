from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from ta_alloc.models import *
from ta_allocation.forms import *
from django.views.decorators.csrf import csrf_exempt
import xlrd
import StringIO
import csv
import os
import xlwt
from django.core.mail import send_mail, EmailMessage
# from StringIO import StringIO
from pyExcelerator import *
import zipfile
import xlrd, xlwt
from xlutils.copy import copy
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from subprocess import call
from django.core.urlresolvers import *

#Loads Home page(that contains the choices TA and Professor) if the user is authenticated and index page otherwise
def index(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==0):
				return redirect(student_index)
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			else:
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html')
	#return render(request, 'ta_allocation/index.html')


def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return HttpResponseRedirect('/')


#Students' views:

def student_index(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry_student = student_general.objects.get(loginid = request.user.email)
			status = entry_role.status
			s_all = skill_univ_set.objects.all()
			s_kind = skill_kind.objects.all()
			skills={}
			for element in s_kind:
				s_entry=skill_univ_set.objects.filter(kind=element)
				skills[element.aid]=s_entry
			stu_skills = student_skill_level.objects.filter(uid = entry_role)
			slist={}
			profile = student_general.objects.get(loginid = entry_role)
			courses1 = prereq_univ_set.objects.filter(year = 1)
			courses2 = prereq_univ_set.objects.filter(year = 2)
			courses3 = prereq_univ_set.objects.filter(year = 3)
			courses4 = prereq_univ_set.objects.filter(year = 4)
			grades = student_prereq_grade.objects.filter(uid = entry_role)
			gradelist={}
			for element in grades:
				print type(element.pid)
				gradelist[element.pid]=element.value
				print "element: "
				print element.pid
				print element.value
			if entry_student.name == "":
				return render(request, 'ta_allocation/student_index.html',{'gradelist':gradelist, 'skill_set':skills,'user':request.user.username,'check':0})
			else:
				return render(request, 'ta_allocation/student_index.html',{'skill_set':skills, 'user':request.user.username,'status':entry_student.status,'email':request.user.email,'check':1,'rollno':entry_student.roll_no,'name':entry_student.name,'program':entry_student.program,'courses':entry_student.other_courses,'skills':entry_student.other_skills})
		except student_general.DoesNotExist:
			print "Helloo!!!"
			print request.user.email
			student = student_general(loginid = entry_role, roll_no = "", name = "", program = 0, other_courses = "", other_skills = "", status = 0)
			student.save()
			return render(request, 'ta_allocation/student_index.html',{'user':request.user.username,'check':0})
		
	else:
		return render(request, 'ta_allocation/index.html')


def student_mycourses(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		profile = student_general.objects.get(loginid = entry_role)
		ap1 = student_application.objects.filter(uid = entry).order_by('pref')
		if request.method=='POST': #get the details from request, if it is a post request
			aid = request.POST['aid']
			c = course.objects.get(pk = aid)
			ap = student_application.objects.get(uid = entry, cid = c)
			new_status=request.POST['new_status']
			if(new_status=="0"):
				pref=ap.pref
				if(pref>1):
					ap.pref-=1
					for element in ap1.exclude(aid=ap.aid):
						if element.pref==pref-1:
							element.pref+=1
							element.save()
				ap.save()	
			elif(new_status=="1"):
				pref=ap.pref
				max=pref
				for element in ap1:
					if element.pref>max:
						max=element.pref
				if(pref<max):
					ap.pref+=1
					for element in ap1.exclude(aid=ap.aid):
						if element.pref==pref+1:
							element.pref-=1
							element.save()
				ap.save()
			elif(new_status=="2"):
				pref=ap.pref
				ap.pref=0
				for element in ap1.exclude(aid=ap.aid):
					if element.pref>pref:
						element.pref=element.pref-1
						element.save()
				ap.delete()
		mycourses = student_application.objects.filter(uid=entry).order_by('pref')	
		return render(request, 'ta_allocation/student_mycourses.html', {'mycourses' : mycourses , 'user':request.user.email})
	else: #if user is not authenticated, take him back to index page
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})


def student_profile(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		if request.method == 'POST':
			form = p_form(request.POST)
			entry = student_general.objects.get(loginid = request.user.email)
			status = entry.status
			str = "Please enter All the values."
			if form.is_valid():			
				entry.name = request.POST['name']
				entry.roll_no = request.POST['roll_no']
				entry.program = request.POST['program']
				entry.save()
				str="Your details have been saved"
			return render(request, 'ta_allocation/student_profile.html', {'status': status, 'form': form, 'str': str})
		else:
			loginid = request.user.email
			entry = student_general.objects.get(loginid = loginid)
			status = 0;
			if(entry):
				form = p_form(
					initial={'name':entry.name, 'roll_no':entry.roll_no, 'program':entry.program}
					)
				status = entry.status
			return render(request, 'ta_allocation/student_profile.html', {'status': status, 'form': form})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})





def student_disable(request):
	print "in disable"
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry_role.status=-1
		entry_role.save()
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		loginid = request.user.email
		entry = student_general.objects.get(loginid = loginid)
		print entry.status
		print "setting to 1"
		entry.status = 1
		print entry.status
		entry.save()
		return redirect(student_index)
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})

def student_enable(request):
	print "in enable"
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry_role.status=1
		entry_role.save()
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		print entry.status
		loginid = request.user.email
		entry = student_general.objects.get(loginid = loginid)
		entry.status = 0
		print "setting to 0"
		entry.save()
		print entry.status
		return redirect(student_index)
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})




def student_grades(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		if request.method == 'POST':
			profile = student_general.objects.get(loginid = entry_role)
			courses = prereq_univ_set.objects.all()
			for element in courses:
				v = request.POST.get('id_'+str(element.aid),False)
				print v
				if not(v):
					continue
				pre=prereq_univ_set.objects.get(pk=element.aid)
				try:
					sc = student_prereq_grade.objects.get(uid = entry_role, pid=pre)
					sc.value = v
					sc.save()
				except student_prereq_grade.DoesNotExist:
					sc = student_prereq_grade.objects.create(uid=entry_role, pid=pre, value=v)
					sc.save
			courses1 = prereq_univ_set.objects.filter(year = 1)
			courses2 = prereq_univ_set.objects.filter(year = 2)
			courses3 = prereq_univ_set.objects.filter(year = 3)
			courses4 = prereq_univ_set.objects.filter(year = 4)
			str1="Your Grades have been updated"
			grades = student_prereq_grade.objects.filter(uid = entry_role)
			print "asda"
			gradelist={}
			for element in grades:
				print type(element.pid)
				print "jeez"
				gradelist[element.pid]=element.value
			print gradelist
			return render(request, 'ta_allocation/student_grades.html',{'gradelist':gradelist, 'str': str1, 'user':request.user.email, 'courses1':courses1, 'courses2':courses2, 'courses3':courses3, 'courses4':courses4})
		else:
			profile = student_general.objects.get(loginid = entry_role)
			courses1 = prereq_univ_set.objects.filter(year = 1)
			courses2 = prereq_univ_set.objects.filter(year = 2)
			courses3 = prereq_univ_set.objects.filter(year = 3)
			courses4 = prereq_univ_set.objects.filter(year = 4)
			grades = student_prereq_grade.objects.filter(uid = entry_role)
			gradelist={}
			for element in grades:
				print type(element.pid)
				gradelist[element.pid]=element.value
				print "element: "
				print element.pid
				print element.value
			#print gradelist
			return render(request, 'ta_allocation/student_grades.html',{'gradelist':gradelist, 'user':request.user.email, 'courses1':courses1, 'courses2':courses2, 'courses3':courses3, 'courses4':courses4})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.email})




def student_skills1(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		if request.method == 'POST':
			profile = student_general.objects.get(loginid = request.user.email)
			skills = skill_univ_set.objects.all()
			for element in skills:
				v = request.POST['id_'+str(element.aid)]
				print v
				if not(v):
					continue
				print "got true"
				s_entry=skill_univ_set.objects.get(pk=element.aid)
				try:
					ss = student_skill_level.objects.get(uid = entry_role, sid=s_entry)
					ss.value = v
					ss.save()
				except student_skill_level.DoesNotExist:
					ss = student_skill_level.objects.create(uid=entry_role, sid=s_entry, value=v)
					ss.save
			s_all = skill_univ_set.objects.all()
			s_kind = skill_kind.objects.all()
			skills={}
			for element in s_kind:
				s_entry=skill_univ_set.objects.filter(kind=element)
				skills[element.aid]=s_entry
			stu_skills = student_skill_level.objects.filter(uid = entry_role)
			slist={}
			for element in stu_skills:
				print type(element.sid.aid)
				slist[element.sid.aid]=element.value
			print slist
			s1 = "Your skills have been updated"
			return render(request, 'ta_allocation/student_skills.html',{'str':s1, 'slist':slist, 'klist':s_kind, 'user':request.user.email, 'skills':skills})
		else:
			profile = student_general.objects.get(loginid = request.user.email)
			s_all = skill_univ_set.objects.all()
			s_kind = skill_kind.objects.all()
			skills={}
			for element in s_kind:
				s_entry=skill_univ_set.objects.filter(kind=element)
				skills[element.aid]=s_entry
			stu_skills = student_skill_level.objects.filter(uid = entry_role)
			slist={}
			print skills
			for element in stu_skills:
				print type(element.sid.aid)
				slist[element.sid.aid]=element.value
			print slist
			return render(request, 'ta_allocation/student_skills.html',{'slist':slist, 'klist':s_kind, 'user':request.user.email, 'skills':skills})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.email})



def student_apply(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		uname = request.user.email
		profile = student_general.objects.get(loginid = entry_role)
		c1=course.objects.filter(status=1)
		print c1
		c2=course.objects.filter(status=1).filter(year=2)
		c3=course.objects.filter(status=1).filter(year=3)
		c4=course.objects.filter(status=1).filter(year=4)
		sa1 = student_application.objects.filter(uid = entry)
		return render(request, 'ta_allocation/student_apply1.html', {'applications' : sa1, 'courses1' : c1, 'courses2' : c2, 'courses3' : c3, 'courses4' : c4, 'user':request.user.email})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.email})



@csrf_exempt		
def student_cdetails(request):
	if request.user.is_authenticated():
		uname = request.user.email
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		if request.method == 'POST':
			aid = request.POST['aid']
			profile = student_general.objects.get(loginid = entry_role)
			print "aid: "
			print aid
			course_obj=course.objects.get(pk=aid)
			try:
				sa1 = student_application.objects.get(uid = entry, cid=course_obj)
				score = sa1.value
			except student_application.DoesNotExist:
				score = ""
			prereqs=prereq_mapping.objects.filter(cid=course_obj)
			skills=skill_mapping.objects.filter(cid=course_obj)
			stu_skills = student_skill_level.objects.filter(uid = entry_role)
			slist={}
			for element in stu_skills:
				print type(element.sid.aid)
				slist[element.sid.aid]=element.value
			print "slist: "
			print slist
			grades = student_prereq_grade.objects.filter(uid = entry_role)
			gradelist={}
			for element in grades:
				print type(element.pid)
				print "jeez"
				gradelist[element.pid]=element.value
			return render(request, 'ta_allocation/student_cdetails.html', {'score' : score, 'slist' : slist, 'gradelist' : gradelist, 'course' : course_obj,'prereqs': prereqs, 'skills': skills, 'user':request.user.email})
		else:
			return render(request, 'ta_allocation/student_index.html',{'user':request.user.email})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.email})



def student_cdone(request):
	if request.user.is_authenticated():
		try:
			entry_role = role_list.objects.get(loginid = request.user.email)
			if(entry_role.role==9):
				return render(request, 'ta_allocation/members.html', {'user':request.user.username})
			elif(entry_role.role==1):
				return redirect(prof_index)
			elif(entry_role.role==8):
				return redirect(admin_index)
			elif(entry_role.role!=0):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		try:
			entry = student_general.objects.get(loginid = entry_role)
		except student_general.DoesNotExist:
			return redirect(student_index)
		uname = request.user.email
		if request.method == 'POST':
			aid = request.POST['aid']
			course_obj=course.objects.get(pk=aid)
			profile = student_general.objects.get(loginid = entry_role)
			val= int(float(request.POST['grade']))
			try:
				sa1 = student_application.objects.get(uid = entry, cid=course_obj)
				sa1.value = val
				sa1.save()
			except student_application.DoesNotExist:
				applications = student_application.objects.filter(uid = entry)
				max=0
				for element in applications:
					if (element.pref>max):
						max=element.pref
				sa1 = student_application.objects.create(uid=entry, cid=course_obj, value=val, pref=max+1)
				sa1.save()
			prereqs=prereq_mapping.objects.filter(cid=course_obj)
			skills=skill_mapping.objects.filter(cid=course_obj)			
			for element in prereqs:
				v= request.POST["p_"+str(element.prereq.aid)]
				if v=="":
					v=0
				else:
					v=int(float(v))
				pre=prereq_univ_set.objects.get(pk=element.prereq.aid)
				try:
					sc = student_prereq_grade.objects.get(uid = entry_role, pid=pre)
					sc.value = v
					sc.save()
				except student_prereq_grade.DoesNotExist:
					sc = student_prereq_grade.objects.create(uid=entry_role, pid=pre, value=v)
					sc.save()
			for element in skills:
				v= request.POST["s_"+str(element.skill.aid)]
				print v
				skill=skill_univ_set.objects.get(pk=element.skill.aid)
				try:
					ss = student_skill_level.objects.get(uid = entry_role, sid=skill)
					ss.value = v
					ss.save()
					print "already existed"
				except student_skill_level.DoesNotExist:
					ss = student_skill_level.objects.create(uid=entry_role, sid=skill, value=v)
					ss.save()
					print "created new skill here"
			return redirect(student_mycourses)
		else:
			return student_index(request)
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.email})


#Professors' views

def prof_index(request):
	if request.user.is_authenticated(): #get the details from request, if it is a post request
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})				
		if request.method == 'POST':
			print "in index"
			cid = request.POST['cid']
			cid = cid.replace(" ","")
			cid = cid.replace("/","-")
			cid = cid.replace(",","-")
			print cid
			cname = request.POST['cname']
			cname = cname.replace("/","-")
			cname = cname.replace(",","-")
			print cname
			year = request.POST['year']
			print year
			tamin = request.POST['tamin']
			tamax = request.POST['tamax']
			print tamin
			print tamax
			try:
					c1 = course_details.objects.get(cid = cid)
					str="Course : "+cid+" already exists"
					print str
			except course_details.DoesNotExist:
					c1 = course_details.objects.create(cid=cid,cname=cname,year=year,prof_name=request.user.email,ta_min=tamin,ta_max=tamax,status=1)
					c1.save()
					str="Your course : "+cid+" has been registered"
					print str
			return render(request, 'ta_allocation/prof_index.html',{'user':request.user.email, 'str':str})
		else:
			return render(request, 'ta_allocation/prof_index.html',{'user':request.user.username})
	else:#if user is not authenticated, take him back to index page
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})



def prof_add(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		courses1=courses_all.objects.filter(year=1)
		courses2=courses_all.objects.filter(year=2)
		courses3=courses_all.objects.filter(year=3)
		courses4=courses_all.objects.filter(year=4)
		s_k=skills_kind.objects.all
		skills1=skills_all.objects.filter(kind=1)
		skills2=skills_all.objects.filter(kind=2)
		skills3=skills_all.objects.filter(kind=3)
		skills4=skills_all.objects.filter(kind=4)
		skills5=skills_all.objects.filter(kind=5)
		all_courses = course_details.objects.all()
		form = c_form(
				initial={'cid':"Ex:CSE101",'cname':"Course Name here",'year':1,'tamin':"Minimum Number of TA's here",'tamax':"Maximum Number of TA's here"}
				)
		return render(request, 'ta_allocation/prof_add.html', {'form': form,'all' : all_courses, 'courses1' : courses1, 'courses2' : courses2, 'courses3' : courses3, 'courses4' : courses4, 'skills1' : skills1, 'skills2' : skills2, 'skills3' : skills3, 'skills4' : skills4, 'skills5' : skills5, 'skills_kind' : s_k})
	else: #if user is not authenticated, take him back to index page
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})



def prof_allcourses(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries1 = course.objects.filter(prof_id1=entry)
		entries2 = course.objects.filter(prof_id2=entry)
		return render(request, 'ta_allocation/prof_allcourses.html', {'entries': entries1 , 'entries2': entries2})
	else:
		return render(request, 'ta_allocation/index.html')




def prof_viewcourse(request,param):
	print "hey!"
	print param
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries = course.objects.all()
		entry1 = course.objects.get(aid=int(param))
		prereqs = prereq_mapping.objects.filter(cid=entry1)
		prereqs_len = len(prereqs)
		skills = skill_mapping.objects.filter(cid=entry1)
		skills_len = len(skills)
		if ((entry1.prof_id1) and entry1.prof_id1.loginid != request.user.email) and ((entry1.prof_id2) and entry1.prof_id2.loginid != request.user.email) and entry.role==1:
			return redirect(prof_index)
		return render(request, 'ta_allocation/viewcourse.html', {'prereqs':prereqs,'skills':skills,'prereqs_len':prereqs_len,'skills_len':skills_len, 'entry':entry1})
	else:
		return render(request, 'ta_allocation/index.html')



def prof_editcourse(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif (entry.role==9):
				return HttpResponseRedirect('/admin/editcourse/'+param)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "post"
			form = courses_form(request.POST)
			entry = course.objects.get(aid=param)
			str = "Please enter All the values."
			entry.cid = request.POST['cid']
			entry.cname = request.POST['cname']
			entry.cdesc = request.POST['cdesc']
			entry.sem = request.POST['sem']
			entry.year = request.POST['year']
			try:
				entry.prof_id1 = role_list.objects.get(loginid=request.POST['prof_id1'])
			except:	
				prof1 = role_list(loginid=request.POST['prof_id1'],role=1,status=1,program=-1)
				prof1.save()
				entry.prof_id1 = prof1

			if request.POST['prof_id2']!="":
				try:
					prof2 = role_list.objects.get(loginid=request.POST['prof_id2'])
					entry.prof_id2 = prof2
				except:	
					prof2 = role_list(loginid=request.POST['prof_id2'],role=1,status=1,program=-1)
					prof2.save()
					entry.prof_id2 = prof2
				
				
			entry.reg_no = request.POST.get('reg_no')
			entry.tutors_min = request.POST['tutors_min']
			entry.tutors_max = request.POST['tutors_max']
			entry.s_ta_min = request.POST['s_ta_min']
			entry.s_ta_max = request.POST['s_ta_max']
			entry.j_ta_min = request.POST['j_ta_min']
			entry.j_ta_max = request.POST['j_ta_max']
			entry.btech_ta_min = request.POST['btech_ta_min']
			entry.btech_ta_max = request.POST['btech_ta_max']
			entry.select_max = request.POST['select_max']
			entry.aid = param
			entry.save()
			str1="Your details have been saved"
			doa_update_ta_min_and_max()
			return HttpResponseRedirect('/professor/viewcourse/'+param)
		else:
			print "What"
			entry = course.objects.get(aid = param)
			prereqs = prereq_mapping.objects.filter(cid=entry)
			prereqs_len = len(prereqs)
			skills = skill_mapping.objects.filter(cid=entry)
			skills_len = len(skills)
			courses1=prereq_univ_set.objects.filter(year=1)
			courses2=prereq_univ_set.objects.filter(year=2)
			courses3=prereq_univ_set.objects.filter(year=3)
			courses4=prereq_univ_set.objects.filter(year=4)
			prereq_all = prereq_univ_set.objects.all()
			s_k=skill_kind.objects.all
			skills1=skill_univ_set.objects.filter(kind=1)
			skills2=skill_univ_set.objects.filter(kind=2)
			skills3=skill_univ_set.objects.filter(kind=3)
			skills4=skill_univ_set.objects.filter(kind=4)
			skills5=skill_univ_set.objects.filter(kind=5)
			skills_all = skill_univ_set.objects.all()

			if ((entry.prof_id1) and entry.prof_id1.loginid != request.user.email) and ((entry.prof_id2) and entry.prof_id2.loginid != request.user.email) and user_role==1:
				return render(request, 'ta_allocation/index.html', {'user':request.user.username})
			if(entry):
				if(entry.prof_id2):
					form = courses_form(
					initial={'aid':entry.aid, 'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'prof_id2':entry.prof_id2.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
					)
				else:
					form = courses_form(
					initial={'aid':entry.aid,'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
					)
					form.fields['cid'].widget.attrs['readonly'] = True
					form.fields['prof_id1'].widget.attrs['readonly'] = True
					form.fields['prof_id2'].widget.attrs['readonly'] = True
					form.fields['reg_no'].widget.attrs['readonly'] = True
					form.fields['select_max'].widget.attrs['readonly'] = True
			doa_update_ta_min_and_max()
			return render(request, 'ta_allocation/editcourse.html',{'prereq_all':prereq_all, 'skills_all':skills_all, 's_k':s_k, 'courses1':courses1, 'courses2':courses2, 'courses3':courses3, 'courses4':courses4, 'skills1':skills1, 'skills2':skills2,'skills3':skills3, 'skills4':skills4, 'skills5':skills5, 'prereqs':prereqs, 'prereqs_len':prereqs_len, 'skills':skills, 'skills_len':skills_len, 'form': form, 'aid': param})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})






# def prof_selectta(request):
# 	if request.user.is_authenticated(): #get the details from request, if it is a post request
# 		try:
# 			entry_role = role_list.objects.get(loginid = request.user.email)
# 			if entry_role.role<1:
# 				return admin_index(request)
# 		except role_list.DoesNotExist:
# 			try:
# 				entry = student_general.objects.get(loginid = entry_role)
# 				return render(request, 'ta_allocation/student_index.html',{'user':request.user.email})
# 			except student_general.DoesNotExist:
# 				return render(request, 'ta_allocation/notallowed.html',{'user':request.user.email})
# 		if request.method == 'POST':
# 			aid=request.POST['aid']
# 			c = course.objects.get(pk=aid)
# 			if(int(request.POST['samepage'])==1):
# 				login = request.POST['loginid']
# 				student=student_general.objects.get(loginid = entry_role)
# 				if(int(request.POST['type'])==1):
# 					student.status=9
# 					student.save()
# 					s_ap=student_application.objects.filter(uid = entry)
# 					for element in s_ap:
# 						element.status=5
# 						element.save()
# 					try:
# 						ap1=student_application.objects.get(uid = entry, cid = c)
# 						ap1.status=1
# 						ap1.save()
# 					except student_application.DoesNotExist:
# 						print "doesnt exist"
# 					# entry = student_selected.objects.create(uid= entry_role, cid=c)	
# 					# entry.save()
# 				if(int(request.POST['type'])==-1):
# 					student.status=0
# 					student.save()
# 					s_ap=student_application.objects.filter(uid = entry)
# 					for element in s_ap:
# 						element.status=0
# 						element.save()
# 					# entry = student_selected.objects.get(uid= entry_role, cid=c)	
# 					# entry.delete()
# 			profiles=student_general.objects.filter(status=0)
# 			selected=student_selected.objects.filter(cid=c,status=1)
# 			all_selected=student_general.objects.filter(status=9)
# 			applications=student_applications.objects.filter(cid = c)
# 			return render(request, 'ta_allocation/prof_selectta.html',{'user':request.user.email, 'cid': cid, 'all_selected': all_selected, 'profiles': profiles, 'applications': applications, 'selected': selected})
# 		else:
# 			return render(request, 'ta_allocation/prof_index.html',{'user':request.user.email})
# 	else:#if user is not authenticated, take him back to index page
# 		return render(request, 'ta_allocation/index.html',{'user':request.user.email})





def prof_applications(request,param):
	if request.user.is_authenticated(): #get the details from request, if it is a post request
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role!=1 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "request.post is: "
			print request.POST
			# aid=request.POST['aid']
			c = course.objects.get(pk=int(param))
			if(int(request.POST['samepage'])==1):
				login = request.POST['loginid']
				print "login is"
				print login
				entry_role_student = role_list.objects.get(aid = int(login))
				entry = student_general(loginid = entry_role_student)
				print " entry_role_student.aid is"
				print entry_role_student.aid
				student=student_general.objects.get(loginid = entry_role_student)
				print " student.aid is"
				print student.aid
				if(int(request.POST['type'])==1):
					student.status=1
					student.save()
					s_ap=student_application.objects.filter(uid = entry,status=0)
					for element in s_ap:
						element.status=5
						element.save()
					try:
						ap1=student_application.objects.get(uid = entry, cid = c)
						ap1.status=1
						ap1.save()
					except student_application.DoesNotExist:
						print "doesnt exist"
					# entry = student_selected.objects.create(uid= entry_role, cid=c)	
					# entry.save()
				if(int(request.POST['type'])==-1):
					student.status=0
					student.save()
					s_ap=student_application.objects.filter(uid = entry,cid=c)
					for element in s_ap:
						element.status=0
						element.save()
					# entry = student_selected.objects.get(uid= entry_role, cid=c)	
					# entry.delete()
			entry_course = course.objects.get(aid=int(param))
			profiles=student_application.objects.filter(Q(cid=entry_course,status=0) | Q(cid=entry_course,status=5))
			shortlisted = student_application.objects.filter(cid=c,status=1)
			selected=student_allocated.objects.filter(course_id=c)
			all_selected=student_general.objects.filter(status=1)
			applications=student_application.objects.filter(cid = c)
			return render(request, 'ta_allocation/prof_selectta.html',{'user':request.user.email, 'shortlisted':shortlisted, 'cid': c.cid, 'all_selected': all_selected, 'profiles': profiles, 'applications': applications, 'selected': selected})
		else:
			entry_course = course.objects.get(aid=int(param))
			# entries = student_application.objects.filter(cid=entry_course,status=1)
			profiles=student_application.objects.filter(Q(cid=entry_course,status=0) | Q(cid=entry_course,status=5))
			shortlisted = student_application.objects.filter(cid=entry_course,status=1)
			selected=student_allocated.objects.filter(course_id=entry_course)
			all_selected=student_general.objects.filter(status=1)
			applications=student_application.objects.filter(cid = entry_course)
			cid = entry_course.cid
			return render(request, 'ta_allocation/prof_selectta.html',{'user':request.user.email,'shortlisted':shortlisted, 'cid': cid, 'all_selected': all_selected, 'profiles': profiles, 'applications': applications, 'selected': selected})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.email})




def doa_index(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		return render(request, 'ta_allocation/doa_index.html',{'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})



def doa_reminder(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		reminder_mail()
		return render(request, 'ta_allocation/doa_reminder.html',{'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})



def reminder_mail():
	courses_list = course.objects.all()
	course_prereq_list = prereq_mapping.objects.all()
	contains_prereq = []
	for c in course_prereq_list:
		if c.cid not in contains_prereq:
			contains_prereq.append(c.cid)

	course_skill_list = skill_mapping.objects.all()
	contains_skill = []
	for c in course_skill_list:
		if c.cid not in contains_skill:
			contains_skill.append(c.cid)

	contains_nothing = []
	for c in courses_list:
		#Remove courses that don't need any pre-requisites
		if c.cname=="COM301A":
			continue
		# Add to list, if it is neither present in prereq list nor in skill list
		if c not in contains_prereq and c not in contains_skill:
			contains_nothing.append(c)


	# #Remove courses that don't need any pre-requisites
	# for c in contains_nothing:
	# 	if c.cname=="COM301A":
	# 		contains_nothing

	# print contains_nothing
	for c in contains_nothing:
		if c.prof_id1!=None and c.prof_id2!=None:
			email = EmailMessage('[TA-Allocation] Reminder to update your course details', 'Your course "'+c.cname+'" does not have any pre-requisites or skills yet. Login here: byld5.iiitd.edu.in and edit the details of your course here: byld5.iiitd.edu.in/professor/editcourse/'+str(c.aid)+' . Kindly update it as soon as possible. ', 'pulkit12082@iiitd.ac.in',[c.prof_id1.loginid,c.prof_id2.loginid])
			email.send()
		elif c.prof_id1!=None:
			email = EmailMessage('[TA-Allocation] Reminder to update your course details', 'Your course "'+c.cname+'" does not have any pre-requisites or skills yet. Login here: byld5.iiitd.edu.in and edit the details of your course here: byld5.iiitd.edu.in/professor/editcourse/'+str(c.aid)+' . Kindly update it as soon as possible. ', 'pulkit12082@iiitd.ac.in',[c.prof_id1.loginid])
			email.send()
		elif c.prof_id2!=None:
			email = EmailMessage('[TA-Allocation] Reminder to update your course details', 'Your course "'+c.cname+'" does not have any pre-requisites or skills yet. Login here: byld5.iiitd.edu.in and edit the details of your course here: byld5.iiitd.edu.in/professor/editcourse/'+str(c.aid)+' . Kindly update it as soon as possible. ', 'pulkit12082@iiitd.ac.in',[c.prof_id2.loginid])
			email.send()
				


def doa_allocation(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		# form_1 = allocation_form()
		return render(request, 'ta_allocation/doa_allocation.html',{'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})




def doa_run_algo(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		print "here!!!!!!!!!!!!!!!!!!!!!"
		if request.method == 'POST':
			print request.POST
			print request.POST['program_type']
			with open(os.path.join(os.getcwd(),'file.txt'), 'w') as f:
				f.write("0")
				f.close()

			doa_generate_csvs1(request,int(request.POST['program_type']),int(request.POST['allocation_type']))
			# Read output from files generated by algorithm and pass it to the html file
			print "here before making call"
			path1 = os.path.join(os.getcwd(),"")
			print path1
			call(["java","-jar","./TAallocation/dist/TAallocation.jar",path1])
			print "after making call"
			check_var = "true"
			return render(request, 'ta_allocation/doa_run_algo.html',{'user':request.user.username,'check_var':check_var})
		else:
			# check if the value in file_lock has changed to 1
			# if it has, show the contents of the output file
			# else, show the same page 
			with open(os.path.join(os.getcwd(),'file.txt'), 'r') as f:
				a = f.readline()
				if a=="0":
					print "hey, it is 0"
					str1 = "Algorithm is in running phase right now"
				else:
					print "hey, it is 1"
					str1 = "1 now"
					# doa_parse_output()
					print "back here - - .........................."
					path1=os.path.join(os.getcwd(),'final.csv')
					# return render(request, 'ta_allocation/doa_run_algo_part1.html',{'user':request.user.username, 'str1':str1, 'path1':path1})
					return redirect(doa_algodone)
					f1 = open(path1)
					str1 = f1.read()
					str1="<br />".join(str1.split("\n"))
					print str1
			check_var = "true"
			return render(request, 'ta_allocation/doa_run_algo.html',{'check_var':check_var ,'user':request.user.username, 'str1':str1})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})

def doa_algodone(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		return render(request, 'ta_allocation/doa_run_algodone.html',{'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})



def doa_algo_results(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		print "here!!!!!!!!!!!!!!!!!!!!!"
		reader =""
		my_dict = {}
		with open(os.path.join(os.getcwd(),'final.csv')) as infile:
			reader = csv.reader(infile)
			for row in reader:
				print row
				my_dict[row[0]]=row[1]
		print my_dict
			# my_dict = {rows[0]:rows[1] for rows in reader}
		return render(request, 'ta_allocation/doa_run_algoresult.html',{'my_dict':my_dict, 'user':request.user.username})

	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})

def doa_parse_output():
	with open(os.path.join(os.getcwd(),'final.csv')) as f:
		reader = csv.reader(f)

		count = 0
		for row in reader:
			print row
			count = count+1
			
			try:
				r = role_list.objects.get(loginid=row[0])
				print "here - "
				print r
				c = course.objects.get(cid=row[1])
				print "here - -"
				print c
				s = student_allocated.objects.create(student_id=r,course_id=c)
				s.save()
				continue
			except role_list.DoesNotExist:
				doNothing=0
			except course.DoesNotExist:
				doNothing=0
			except:
				doNothing=0
		print "end of loop-----"

	return 





def doa_generate_csvs1(request,type1,type2):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==1):
				return 
		except role_list.DoesNotExist:
			return 
		# Create the HttpResponse object with the appropriate CSV header.
		# c_file=StringIO.StringIO()
		coursefile =csv.writer(open(os.path.join(os.getcwd(),'courses.csv'), 'w'))
		# p_file=StringIO.StringIO()
		prereqfile =csv.writer(open(os.path.join(os.getcwd(),'prereqs.csv'), 'w'))
		# s_file=StringIO.StringIO()
		skillfile =csv.writer(open(os.path.join(os.getcwd(),'skills.csv'), 'w'))
		# pref_file=StringIO.StringIO()
		preffile =csv.writer(open(os.path.join(os.getcwd(),'preferences.csv'), 'w'))
		# prof_file=StringIO.StringIO()
		proffile =csv.writer(open(os.path.join(os.getcwd(),'course_details.csv'), 'w'))
		
		shortlistfile = csv.writer(open(os.path.join(os.getcwd(),'shortlist.csv'), 'w'))
		
		if type2==0:
			profiles=student_general.objects.all()
			r = role_list.objects.filter(program=type1)
			list_r = []
			for element in r:
				list_r.append(element.loginid)
			list_profiles = []
			for element in profiles:
				if element.loginid.loginid in list_r:
					list_profiles.append(element)
			profiles = list_profiles
			select_appls = student_allocated.objects.all()
			sel_studs = []
			for s in select_appls:
				if s.student_id not in sel_studs:
					sel_studs.append(s.student_id)
			list_profiles = []
			for p in profiles:
				if p.loginid not in sel_studs:
					list_profiles.append(p)
			profiles = list_profiles
		elif type2==-1:
			profiles=student_general.objects.all()
			r = role_list.objects.filter(program=type1)
			list_r = []
			for element in r:
				list_r.append(element.loginid)
			list_profiles = []
			for element in profiles:
				if element.loginid.loginid in list_r:
					list_profiles.append(element)
			profiles = list_profiles
		

		if type1==0:
			profiles=student_general.objects.all()
			r = role_list.objects.filter(program=type1)
			list_r = []
			for element in r:
				list_r.append(element.loginid)
			list_profiles = []
			for element in profiles:
				if element.loginid.loginid in list_r:
					list_profiles.append(element)
			appls = student_application.objects.all()
			list_applicants = []
			for a in appls:
				list_applicants.append(a.uid.loginid.loginid)
			list_profiles2 = []
			for a in list_profiles:
				if a.loginid.loginid in list_applicants:
					list_profiles2.append(a)
			profiles = list_profiles2

		courses=course.objects.all()
		prereq=prereq_univ_set.objects.all()
		skills=skill_univ_set.objects.all()
		
		#csvwriter.writerow(['First row', 'Foo', 'Bar', 'Baz'])
		#csvwriter.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
		header_c = ['Student_ID']
		header_pref = ['Student_ID']
		for element in courses:
			header_c.append(element.cid)
			header_pref.append(element.cid)
		header_p = ['Student_ID']
		for element in prereq:
			header_p.append(element.cname)
		header_s = ['Student_ID']
		for element in skills:
			header_s.append(element.sname)
		coursefile.writerow(header_c)
		shortlistfile.writerow(header_c)
		prereqfile.writerow(header_p)
		skillfile.writerow(header_s)
		preffile.writerow(header_pref)
		list1_proffile = ['Course_id', 'ta_min', 'ta_max', 'prereqs', 'skills']
		# proffile.writerow(['Course_id', 'ta_min', 'ta_max', 'prereqs', 'skills'])
		for element in profiles:
			list=[element.loginid.loginid]
			for c in courses:
				try:
					sa = student_application.objects.get(uid = element, cid=c)
					list.append(sa.value)
				except student_application.DoesNotExist:
					list.append('0')	
			coursefile.writerow(list)
			
		for element in profiles:
			list=[element.loginid.loginid]
			for p in prereq:
				try:
					sc = student_prereq_grade.objects.get(uid = element.loginid, pid=p)
					list.append(sc.value)
				except student_prereq_grade.DoesNotExist:
					list.append('0')	
			prereqfile.writerow(list)
		
		for element in profiles:
			list=[element.loginid.loginid]
			for s in skills:
				try:
					ss = student_skill_level.objects.get(uid = element.loginid, sid=s)
					list.append(ss.value)
				except student_skill_level.DoesNotExist:
					list.append('0')	
			skillfile.writerow(list)
			
		for element in profiles:
			list=[element.loginid.loginid]
			for c in courses:
				try:
					sa = student_application.objects.get(uid = element, cid=c)
					if(sa.pref==1):
						list.append("10")
					elif(sa.pref==2):
						list.append("8")
					elif(sa.pref==3):
						list.append("6")
					elif(sa.pref==4):
						list.append("5")
					elif(sa.pref==5):
						list.append("4")
					else:
						list.append("2")
				except student_application.DoesNotExist:
					list.append('0')	
			preffile.writerow(list)
		

		#Course Details file
		list2_proffile = [list1_proffile[0]]
		list3_proffile = [list1_proffile[1]]
		list4_proffile = [list1_proffile[2]]
		list5_proffile = [list1_proffile[3]]
		list6_proffile = [list1_proffile[4]]
		for element in courses:
			list2_proffile.append(element.cid)
			count=0
			c = element
			#c = course.objects.get(pk=element.cid)
			selected = student_allocated.objects.filter(course_id=c)
			count_bt = 0
			count_mt1 = 0
			count_mt2 = 0
			count_phd = 0
			for s in selected:
				if s.student_id.program==0:
					count_bt = count_bt + 1
				elif s.student_id.program==4:
					count_mt1 = count_mt1 + 1
				elif s.student_id.program==5:
					count_mt2 = count_mt2 + 1
				elif s.student_id.program==7:
					count_phd = count_phd + 1
			min_bt=0
			max_bt=0
			min_mt1=0
			max_mt1=0
			min_mt2=0
			max_mt2=0
			min_phd=0
			max_phd=0
			minta = 0
			maxta = 0
			if type1 == 0:
				if(element.btech_ta_min-count>0):
					minta= element.btech_ta_min-count_bt
				if(element.btech_ta_max-count>0):
					maxta= element.btech_ta_max-count_bt
			elif type1 == 4:
				if(element.j_ta_min-count>0):
					minta= element.j_ta_min-count_mt1
				if(element.j_ta_max-count>0):
					maxta= element.j_ta_max-count_mt1
			elif type1 == 5:
				if(element.s_ta_min-count>0):
					minta= element.s_ta_min-count_mt2
				if(element.s_ta_max-count>0):
					maxta= element.s_ta_max-count_mt2
			elif type1 == 7:
				if(element.tutors_min-count>0):
					minta= element.tutors_min-count_phd
				if(element.tutors_max-count>0):
					maxta= element.tutors_max-count_phd
			
			list3_proffile.append(minta)
			list4_proffile.append(maxta)
			prereq_list = ""
			skill_list = ""
			c_p = prereq_mapping.objects.filter(cid = element)
			c_s = skill_mapping.objects.filter(cid = element)
			for pre in c_p:
				prereq_list= prereq_list+pre.prereq.cname+"!"
			for s in c_s:
				skill_list= skill_list+s.skill.sname+"!"
			if prereq_list == "":
				prereq_list="!"
			if skill_list == "":
				skill_list="!"
			list5_proffile.append(prereq_list)
			list6_proffile.append(skill_list)
		proffile.writerow(list2_proffile)
		proffile.writerow(list3_proffile)
		proffile.writerow(list4_proffile)
		proffile.writerow(list5_proffile)
		proffile.writerow(list6_proffile)
			


		# list1_shortlists = ['Student_ID']
		# list2_shortlists = ['Course_ID']
		# shortlisted_studs = student_application.objects.filter(status=1)
		# for s in shortlisted_studs :
		# 	list1_shortlists.append(s.uid.loginid.loginid)
		# 	list2_shortlists.append(s.cid.cid)
		# shortlistfile.writerow(list1_shortlists)
		# shortlistfile.writerow(list2_shortlists)

		for element in profiles:
			list=[element.loginid.loginid]
			for c in courses:
				try:
					sa = student_application.objects.get(uid = element, cid=c)
					if sa.status==1:
						list.append(1)
					else:
						list.append(0)
				except student_application.DoesNotExist:
					list.append('0')	
			shortlistfile.writerow(list)


		# email = EmailMessage('Ta-allocation', 'PFA files', 'pulkit12082@iiitd.ac.in',['pulkit12082@iiitd.ac.in'])
		# #email = EmailMessage('Ta-allocation', 'PFA files', 'prakhar11074@iiitd.ac.in',['prakhar11074@iiitd.ac.in', 'manish11063@iiitd.ac.in', 'sourabh11112@iiitd.ac.in'])
		# email.attach('courses.csv', c_file.getvalue(), 'text/csv')
		# email.attach('prereqs.csv', p_file.getvalue(), 'text/csv')
		# email.attach('skills.csv', s_file.getvalue(), 'text/csv')
		# email.attach('preferences.csv', pref_file.getvalue(), 'text/csv')
		# email.attach('course_details.csv', prof_file.getvalue(), 'text/csv')
		# #email.attach(response)
		# email.send()
		text="csv has been mailed."
		return 
	


def doa_generate_csvs2(request,type_user):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==1):
				return 
		except role_list.DoesNotExist:
			return 
		# Create the HttpResponse object with the appropriate CSV header.
		# c_file=StringIO.StringIO()
		coursefile =csv.writer(open(os.path.join(os.getcwd(),'inp_courses.csv'), 'w'))
		# p_file=StringIO.StringIO()
		prereqfile =csv.writer(open(os.path.join(os.getcwd(),'inp_prereqs.csv'), 'w'))
		# s_file=StringIO.StringIO()
		skillfile =csv.writer(open(os.path.join(os.getcwd(),'inp_skills.csv'), 'w'))
		# pref_file=StringIO.StringIO()
		preffile =csv.writer(open(os.path.join(os.getcwd(),'inp_preferences.csv'), 'w'))
		# prof_file=StringIO.StringIO()
		proffile =csv.writer(open(os.path.join(os.getcwd(),'inp_course_details.csv'), 'w'))
		
		profiles=student_general.objects.filter(status=9)
		if type_user==-2:
			profiles=student_general.objects.filter(status=0)
		courses=course.objects.all()
		prereq=prereq_univ_set.objects.all()
		skills=skill_univ_set.objects.all()
		
		#csvwriter.writerow(['First row', 'Foo', 'Bar', 'Baz'])
		#csvwriter.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
		header_c = ['Student_ID']
		header_pref = ['Student_ID']
		for element in courses:
			header_c.append(element.cid)
			header_pref.append(element.cid)
		header_p = ['Student_ID']
		for element in prereq:
			header_p.append(element.cname)
		header_s = ['Student_ID']
		for element in skills:
			header_s.append(element.sname)
		coursefile.writerow(header_c)
		prereqfile.writerow(header_p)
		skillfile.writerow(header_s)
		preffile.writerow(header_pref)
		proffile.writerow(['Course_id', 'btech_ta_min', 'btech_ta_max','mtech1_ta_min', 'mtech1_ta_max','mtech2_ta_min', 'mtech2_ta_max','phd_ta_min', 'phd_ta_max', 'prereqs', 'skills'])
		for element in profiles:
			list=[element.loginid]
			for c in courses:
				try:
					sa = student_application.objects.get(uid = element, cid=c)
					list.append(sa.value)
				except student_application.DoesNotExist:
					list.append('0')	
			coursefile.writerow(list)
			
		for element in profiles:
			list=[element.loginid]
			for p in prereq:
				try:
					sc = student_prereq_grade.objects.get(uid = element.loginid, pid=p)
					list.append(sc.value)
				except student_prereq_grade.DoesNotExist:
					list.append('0')	
			prereqfile.writerow(list)
		
		for element in profiles:
			list=[element.loginid]
			for s in skills:
				try:
					ss = student_skill_level.objects.get(uid = element.loginid, sid=s)
					list.append(ss.value)
				except student_skill_level.DoesNotExist:
					list.append('0')	
			skillfile.writerow(list)
			
		for element in profiles:
			list=[element.loginid]
			for c in courses:
				try:
					sa = student_application.objects.get(uid = element, cid=c)
					if(sa.pref==1):
						list.append("10")
					elif(sa.pref==2):
						list.append("8")
					elif(sa.pref==3):
						list.append("6")
					elif(sa.pref==4):
						list.append("5")
					elif(sa.pref==5):
						list.append("4")
					else:
						list.append("2")
				except student_applications.DoesNotExist:
					list.append('0')	
			preffile.writerow(list)
		
		for element in courses:
			list=[element.cid]
			count=0
			c = element
			#c = course.objects.get(pk=element.cid)
			selected = student_allocated.objects.filter(course_id=c)
			count_bt = 0
			count_mt1 = 0
			count_mt2 = 0
			count_phd = 0
			for s in selected:
				if s.student_id.program==0:
					count_bt = count_bt + 1
				elif s.student_id.program==4:
					count_mt1 = count_mt1 + 1
				elif s.student_id.program==5:
					count_mt2 = count_mt2 + 1
				elif s.student_id.program==7:
					count_phd = count_phd + 1
			min_bt=0
			max_bt=0
			min_mt1=0
			max_mt1=0
			min_mt2=0
			max_mt2=0
			min_phd=0
			max_phd=0
			min_ta = 0
			max_ta = 0
			if type_user == 0:
				if(element.btech_ta_min-count>0):
					min_bt= element.btech_ta_min-count_bt
				if(element.btech_ta_max-count>0):
					max_bt= element.btech_ta_max-count_bt
			elif type_user == 4:
				if(element.j_ta_min-count>0):
					min_mt1= element.j_ta_min-count_mt1
				if(element.j_ta_max-count>0):
					max_mt1= element.j_ta_max-count_mt1
			elif type_user == 5:
				if(element.s_ta_min-count>0):
					min_mt2= element.s_ta_min-count_mt2
				if(element.s_ta_max-count>0):
					max_mt2= element.s_ta_max-count_mt2
			elif type_user == 7:
				if(element.tutors_min-count>0):
					min_phd= element.tutors_min-count_phd
				if(element.tutors_max-count>0):
					max_phd= element.tutors_max-count_phd
			
			list.append(min_bt)
			list.append(max_bt)
			list.append(min_mt1)
			list.append(max_mt1)
			list.append(min_mt2)
			list.append(max_mt2)
			list.append(min_phd)
			list.append(max_phd)
			prereq_list = ""
			skill_list = ""
			c_p = prereq_mapping.objects.filter(cid = element)
			c_s = skill_mapping.objects.filter(cid = element)
			for pre in c_p:
				prereq_list= prereq_list+pre.prereq.cname+"!"
			for s in c_s:
				skill_list= skill_list+s.skill.sname+"!"
			list.append(prereq_list)
			list.append(skill_list)
			proffile.writerow(list)
			
		# email = EmailMessage('Ta-allocation', 'PFA files', 'pulkit12082@iiitd.ac.in',['pulkit12082@iiitd.ac.in'])
		# #email = EmailMessage('Ta-allocation', 'PFA files', 'prakhar11074@iiitd.ac.in',['prakhar11074@iiitd.ac.in', 'manish11063@iiitd.ac.in', 'sourabh11112@iiitd.ac.in'])
		# email.attach('courses.csv', c_file.getvalue(), 'text/csv')
		# email.attach('prereqs.csv', p_file.getvalue(), 'text/csv')
		# email.attach('skills.csv', s_file.getvalue(), 'text/csv')
		# email.attach('preferences.csv', pref_file.getvalue(), 'text/csv')
		# email.attach('course_details.csv', prof_file.getvalue(), 'text/csv')
		# #email.attach(response)
		# email.send()
		text="csv has been mailed."
		return 




def doa_upload_policy(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "policy func"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						if row[0].lower()=="core":
							try:
								entry = policy.objects.get(course_type=1)
								if(row[1]!=""):
									entry.ratio_s_ta_min = int(float(row[1]))
								if(row[2]!=""):
									entry.ratio_j_ta_min = int(float(row[2]))
								if(row[3]!=""):
									entry.ratio_btech_ta_min = int(float(row[3]))
								if(row[4]!=""):
									entry.ratio_tutors_min = int(float(row[4]))
								entry.save()
								doa_update_ta_min_and_max()
							except policy.DoesNotExist:
								r=policy(course_type=1,ratio_s_ta_min = int(float(row[1])),ratio_j_ta_min = int(float(row[2])),ratio_btech_ta_min = int(float(row[3])),ratio_tutors_min = int(float(row[4])))
								r.save()
								doa_update_ta_min_and_max()
						elif row[0].lower()=="core elective":
							try:
								entry = policy.objects.get(course_type=2)
								if(row[1]!=""):
									entry.ratio_s_ta_min = int(float(row[1]))
								if(row[2]!=""):
									entry.ratio_j_ta_min = int(float(row[2]))
								if(row[3]!=""):
									entry.ratio_btech_ta_min = int(float(row[3]))
								if(row[4]!=""):
									entry.ratio_tutors_min = int(float(row[4]))
								entry.save()
								doa_update_ta_min_and_max()
							except policy.DoesNotExist:
								r=policy(course_type=2,ratio_s_ta_min = int(float(row[1])),ratio_j_ta_min = int(float(row[2])),ratio_btech_ta_min = int(float(row[3])),ratio_tutors_min = int(float(row[4])))
								r.save()
								doa_update_ta_min_and_max()
						elif row[0].lower()=="required elective":
							try:
								entry = policy.objects.get(course_type=3)
								if(row[1]!=""):
									entry.ratio_s_ta_min = int(float(row[1]))
								if(row[2]!=""):
									entry.ratio_j_ta_min = int(float(row[2]))
								if(row[3]!=""):
									entry.ratio_btech_ta_min = int(float(row[3]))
								if(row[4]!=""):
									entry.ratio_tutors_min = int(float(row[4]))
								entry.save()
								doa_update_ta_min_and_max()
							except policy.DoesNotExist:
								r=policy(course_type=3,ratio_s_ta_min = int(float(row[1])),ratio_j_ta_min = int(float(row[2])),ratio_btech_ta_min = int(float(row[3])),ratio_tutors_min = int(float(row[4])))
								r.save()
								doa_update_ta_min_and_max()
						elif row[0].lower()=="free elective":
							try:
								entry = policy.objects.get(course_type=4)
								if(row[1]!=""):
									entry.ratio_s_ta_min = int(float(row[1]))
								if(row[2]!=""):
									entry.ratio_j_ta_min = int(float(row[2]))
								if(row[3]!=""):
									entry.ratio_btech_ta_min = int(float(row[3]))
								if(row[4]!=""):
									entry.ratio_tutors_min = int(float(row[4]))
								entry.save()
								doa_update_ta_min_and_max()
							except policy.DoesNotExist:
								r=policy(course_type=4,ratio_s_ta_min = int(float(row[1])),ratio_j_ta_min = int(float(row[2])),ratio_btech_ta_min = int(float(row[3])),ratio_tutors_min = int(float(row[4])))
								r.save()
								doa_update_ta_min_and_max()
    					
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = "Policies updated"#str(count_of_users_added) + " users have been added and "+ str(count_of_users_updated) + " have been updated!"
			loginid = request.user.email
			form = UploadFileForm()
			return render(request, 'ta_allocation/doa_addpolicy_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/doa_addpolicy_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')



def doa_update_ta_min_and_max():
	courses = course.objects.all()
	for c in courses:
		if c.course_type_id and c.reg_no:

			c.s_ta_min = c.reg_no / policy.objects.get(course_type=c.course_type_id).ratio_s_ta_min
			c.s_ta_max = c.s_ta_min + 2
			c.j_ta_min = c.reg_no / policy.objects.get(course_type=c.course_type_id).ratio_j_ta_min
			c.j_ta_max = c.j_ta_min + 2
			c.btech_ta_min = c.reg_no / policy.objects.get(course_type=c.course_type_id).ratio_btech_ta_min
			c.btech_ta_max = c.btech_ta_min
			c.tutors_min = c.reg_no / policy.objects.get(course_type=c.course_type_id).ratio_tutors_min
			c.tutors_max = c.tutors_min + 2
			if c.reg_no<=10:
				c.s_ta_min = 0
				c.s_ta_max = 0
				c.j_ta_min = 0
				c.j_ta_max = 0
				c.btech_ta_min = 0
				c.btech_ta_max = 0
				c.tutors_min = 0
				c.tutors_max = 0
			c.save()




def doa_download_policyxls(request):
	policy_path = os.path.join(os.getcwd(),'Policy.xls')

	filenames = [policy_path]
	zip_subdir = os.getcwd()
	zip_filename = "Policy.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp
	resp = HttpResponse(mimetype = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename="Policy.zip"'
	resp['X-Sendfile'] = policy_path
	return resp



def doa_upload_registration(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				c_found = 0
				c_notfound = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "reg func"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						try:
							entry = course.objects.get(cid = row[0])
							entry.reg_no = int(float(row[1]))
							entry.save()
							c_found = c_found + 1
						except course.DoesNotExist:
							c_notfound = c_notfound + 1
						
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = "Registration Numbers updated for "+ str(c_found)+" courses. "+str(c_notfound)+" courses were not found."#str(count_of_users_added) + " users have been added and "+ str(count_of_users_updated) + " have been updated!"
			loginid = request.user.email
			form = UploadFileForm()
			doa_update_ta_min_and_max()
			return render(request, 'ta_allocation/doa_registration_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/doa_registration_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')
def doa_allapplications(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		appls = student_application.objects.all()
		return render(request, 'ta_allocation/doa_allapplications.html', {'appls':appls,'user':request.user.username})


def doa_download_algoresult(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		pref_path = os.path.join(os.getcwd(),'preferences.csv')
		util_path = os.path.join(os.getcwd(),'utility.csv')
		final_path  = os.path.join(os.getcwd(),'final.csv')
		filenames = [pref_path,util_path,final_path]
		zip_subdir = os.getcwd()
		zip_filename = "AlgoResults.zip"
		s = StringIO.StringIO()
		zf = zipfile.ZipFile(s, "w")
		for fpath in filenames:
			fdir, fname = os.path.split(fpath)
			zip_path = fname
			zf.write(fpath, zip_path)
		zf.close()
		resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
		resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
		return resp
		resp = HttpResponse(mimetype = "application/x-zip-compressed")
		# ..and correct content-disposition
		resp['Content-Disposition'] = 'attachment; filename="AlgoResults.zip"'
		resp['X-Sendfile'] = pref_path
		resp['X-Sendfile'] = util_path
		resp['X-Sendfile'] = final_path
		return resp
	else:
		return render(request, 'ta_allocation/index.html',{'user':request.user.username})
	



def doa_download_registrationdataxls(request):
	doa_write_registration_data()
	reg_spath = os.path.join(os.getcwd(),'RegistrationData01.xls')

	filenames = [reg_path]
	zip_subdir = os.getcwd()
	zip_filename = "RegistrationData.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp
	resp = HttpResponse(mimetype = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename="RegistrationData.zip"'
	resp['X-Sendfile'] = reg_path
	return resp




def doa_write_registration_data():
	rb = xlrd.open_workbook(os.path.join(os.getcwd(),'RegistrationData.xls')) #Make Readable Copy
	wb = copy(rb) #Make Writeable Copy

	ws1 = wb.get_sheet(0) #Get sheet 1 in writeable copy
	
	courses = course.objects.all()
	ctr = 1
	for c in courses:
		ws1.write(ctr,0,c.cid)
		ws1.write(ctr,1,c.reg_no)
		ctr = ctr + 1
	wb.save(os.path.join(os.getcwd(),'RegistrationData01.xls'))



def doa_results(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			courses = course.objects.all()
		else:
			courses = course.objects.all()
			selected_students = {}
			# for course_iter in courses:
			# 	selected_studs = student_application.objects.filter(cid=course_iter,status=9)
			# 	new_list = []
			# 	for studs in selected_studs:
			# 		new_list.append(studs.uid.loginid.loginid)
			# 	selected_students[course_iter.cid] = new_list
			return render(request, 'ta_allocation/doa_results.html', {'courses': courses,'str':"", 'selected_students': selected_students})
	else:
		return render(request, 'ta_allocation/index.html')


def doa_courseresults(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			c = course.objects.get(aid = int(param))
			if(int(request.POST['samepage'])==1):
				login = request.POST['loginid']
				print "login is"
				print login
				entry_role_student = role_list.objects.get(aid = int(login))
				entry = student_general(loginid = entry_role_student)
				print " entry_role_student.aid is"
				print entry_role_student.aid
				student=student_general.objects.get(loginid = entry_role_student)
				print " student.aid is"
				print student.aid
				if(int(request.POST['type'])==1):
					# student.status=9
					# student.save()
					# s_ap=student_application.objects.filter(uid = entry)
					# for element in s_ap:
					# 	element.status=5
					# 	element.save()
					# try:
					# 	ap1=student_application.objects.get(uid = entry, cid = c)
					# 	ap1.status=9
					# 	ap1.save()
					# except student_application.DoesNotExist:
					# 	print "doesnt exist"


					try:
						entry = student_allocated.objects.get(student_id=entry_role_student,course_id=c)
					except student_allocated.DoesNotExist:
						entry = student_selected.objects.create(uid= entry_role_student, cid=c)	
						entry.save()

				if(int(request.POST['type'])==-1):
					# student.status=0
					# student.save()
					# s_ap=student_application.objects.filter(uid = entry)
					# for element in s_ap:
					# 	element.status=0
					# 	element.save()


					try:
						entry = student_allocated.objects.get(student_id=entry_role_student,course_id=c)
						entry.delete()
					except student_allocated.DoesNotExist:
						kachra=2
					kachra=1	
					# entry = student_selected.objects.get(uid= entry_role, cid=c)	
					# entry.delete()
			
			course_obj = course.objects.get(aid = int(param))
			selected = student_application.objects.filter(cid=course_obj)
			stud_sels = student_allocated.objects.filter(course_id=course_obj)
			list_stud_sels = []
			for s in stud_sels:
				list_stud_sels.append(s.student_id)
			list_selected = []
			list_not_selected = []
			for s in selected:
				if s.uid.loginid in list_stud_sels:
					list_selected.append(s)
				else:
					list_not_selected.append(s)
			selected = list_selected
			not_selected = student_application.objects.filter(cid=course_obj,status=0)
			not_selected = list_not_selected
			return render(request, 'ta_allocation/doa_courseresults.html', {'course': course_obj, 'selected':selected, 'not_selected':not_selected,'str':""})
		else:
			course_obj = course.objects.get(aid = int(param))
			selected = student_application.objects.filter(cid=course_obj)
			stud_sels = student_allocated.objects.filter(course_id=course_obj)
			list_stud_sels = []
			for s in stud_sels:
				list_stud_sels.append(s.student_id)
			list_selected = []
			list_not_selected = []
			for s in selected:
				if s.uid.loginid in list_stud_sels:
					list_selected.append(s)
				else:
					list_not_selected.append(s)
			selected = list_selected
			not_selected = student_application.objects.filter(cid=course_obj,status=0)
			not_selected = list_not_selected
			return render(request, 'ta_allocation/doa_courseresults.html', {'course': course_obj, 'selected':selected, 'not_selected':not_selected,'str':""})
	else:
		return render(request, 'ta_allocation/index.html')

	
def doa_policyshow(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==8):
				return redirect(admin_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			courses = course.objects.all()
		else:
			policies = policy.objects.all()
			return render(request, 'ta_allocation/doa_showpolicy.html', {'policies': policies,'str':""})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_index(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		return render(request, 'ta_allocation/admin_index.html', {'user':request.user.username})
	else:
		return render(request, 'ta_allocation/index.html')


def admin_editroles(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		
		if request.method == 'POST':
			entry = role_list.objects.get(aid=param)
			entry.loginid=request.POST['loginid'] 
			entry.role= request.POST['role']
			entry.program = request.POST['program']
			entry.save()
			str="Your details have been saved"
			return redirect('/admin/allusers', {'str': str})
		else:
			entry = role_list.objects.get(aid=param)
			form = roles_form(
				initial ={'loginid':entry.loginid,'role':entry.role,'program':entry.program})
			form.fields['loginid'].widget.attrs['readonly'] = True
			return render(request, 'ta_allocation/admin_editroles.html', {'form': form,'entry':entry})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})

#Function to view User Profile of a TA from admin page.		
def viewuserprofile(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		Previous_path = resolve(request.path).url_name
		if request.method == 'GET':
			entry = role_list.objects.get(aid=param)
			GeneralInfo = student_general.objects.get(loginid=entry.loginid)
			form = roles_form(
				initial ={'loginid':entry.loginid,'role':entry.role,'program':entry.program,'name':GeneralInfo.name,'roll':GeneralInfo.roll_no})
			return render(request, 'ta_allocation/admin_viewuserprofile.html', {'form': form,'entry':entry,'info':GeneralInfo,'path':Previous_path})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})		
		
def admin_addroles(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = roles_form(request.POST)
			str = "Please enter All the values."
			if form.is_valid():		
				entry = role_list(loginid = request.POST['loginid'],role = request.POST['role'],program = request.POST['program'])	
				entry.save()
				str="Your details have been saved"
			return render(request, 'ta_allocation/admin_addroles.html', {'form': form, 'str': str})
		else:
			loginid = request.user.email
			form = roles_form()
			return render(request, 'ta_allocation/admin_addroles.html', {'form': form})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})


def admin_addroles_excel(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				count_of_users_added = 0
				count_of_users_updated = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "hello"
					print "here-------------------------------"
					# print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						# print row
						# print "row[0]"
						# print row[0]
						matrix.append(row)
						program_value = -1
						if row[2].lower()=="notapplicable":
							program_value = -1
						elif row[2].lower()=="btech":
							program_value = 0
						elif row[2].lower()=="mtech1styr":
							program_value = 4
						elif row[2].lower()=="mtech2ndyr":
							program_value = 5
						elif row[2].lower()=="phd":
							program_value = 7
						if row[1].lower()=="ta":
							try:
								entry = role_list.objects.get(loginid=row[0])
								entry.role = 0
								entry.program = program_value
								count_of_users_updated = count_of_users_updated + 1
								entry.save()
							except role_list.DoesNotExist:
								r=role_list(loginid=row[0],role=0,program=program_value)
								count_of_users_added = count_of_users_added + 1
								r.save()
						elif row[1].lower()=="professor":
							try:
								entry = role_list.objects.get(loginid=row[0])
								entry.role = 1
								entry.program = program_value
								count_of_users_updated = count_of_users_updated + 1
								entry.save()
							except role_list.DoesNotExist:
								r=role_list(loginid=row[0],role=1,program=program_value)
								count_of_users_added = count_of_users_added + 1
								r.save()
						elif row[1].lower()=="admin":
							try:
								entry = role_list.objects.get(loginid=row[0])
								entry.role = 8
								entry.program = program_value
								count_of_users_updated = count_of_users_updated + 1
								entry.save()
							except role_list.DoesNotExist:
								r=role_list(loginid=row[0],role=8,program=program_value)
								count_of_users_added = count_of_users_added + 1
								r.save()
						elif row[1].lower()=="superuser":
							try:
								entry = role_list.objects.get(loginid=row[0])
								entry.role = 9
								entry.program = program_value
								count_of_users_updated = count_of_users_updated + 1
								entry.save()
							except role_list.DoesNotExist:
								r=role_list(loginid=row[0],role=9,program=program_value)
								count_of_users_added = count_of_users_added + 1
								r.save()
    					
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = str(count_of_users_added) + " users have been added and "+ str(count_of_users_updated) + " have been updated!"
			loginid = request.user.email
			form = UploadFileForm()
			return render(request, 'ta_allocation/admin_addroles_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/admin_addroles_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')


def admin_download_rolesxls(request):
	# wb = xlwt.Workbook()
	# response = HttpResponse(content_type='application/vnd.ms-excel')
	# response['Content-Disposition'] = 'attachment; filename="Roles.xls"'
	roles_path = os.path.join(os.getcwd(),'Roles.xls')
	# #response = HttpResponse(mimetype='application/force-download')
	# #response['Content-Disposition'] = 'attachment; filename=%s' %"Roles.xls"
	# response['X-Sendfile'] = roles_path
	# #wb.save(response)
	# # It's usually a good idea to set the 'Content-Length' header too.
	# # You can also set any other required headers: Cache-Control, etc.
	# return response


	# output = StringIO.StringIO()
 #   	w = csv.writer(output)
 #   	for i in range(10):
	# 	w.writerow(range(10))
 #   	# rewind the virtual file
 #   	output.seek(0)
 #   	return HttpResponse(output.read(),mimetype='application/vnd.ms-excel')
	# wb = Workbook()
	# ws0 = wb.add_sheet('0')
	# for x in range(10):
	# 	for y in range(10):
	# 		# writing to a specific x,y
	# 		ws0.write(x,y,"this is cell %s, %s" % (x,y))

	# 	wb.save('output.xls')
	# return HttpResponse(open('output.xls','r').read(), mimetype='application/vnd.ms-excel')

	filenames = [roles_path]
	zip_subdir = os.getcwd()
	zip_filename = "Roles.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp
	resp = HttpResponse(mimetype = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename="Roles.zip"'
	resp['X-Sendfile'] = roles_path
	return resp


def admin_download_coursesxls(request):
	courses_path = os.path.join(os.getcwd(),'Courses.xls')

	filenames = [courses_path]
	zip_subdir = os.getcwd()
	zip_filename = "Course.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp
	resp = HttpResponse(mimetype = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename="Course.zip"'
	resp['X-Sendfile'] = courses_path
	return resp


def admin_download_prereqsxls(request):
	prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')

	filenames = [prereqs_path]
	zip_subdir = os.getcwd()
	zip_filename = "PreRequisite.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp
	resp = HttpResponse(mimetype = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename="PreRequisite.zip"'
	resp['X-Sendfile'] = prereqs_path
	return resp


def admin_download_skillsxls(request):
	skills_path = os.path.join(os.getcwd(),'Skills.xls')

	filenames = [skills_path]
	zip_subdir = os.getcwd()
	zip_filename = "Skill.zip"
	s = StringIO.StringIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		fdir, fname = os.path.split(fpath)
		zip_path = fname
		zf.write(fpath, zip_path)
	zf.close()
	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp

def admin_addprereqs_univ(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here (y)"
			#print request
			
			pid = request.POST["pid"]
			cname = request.POST["cname"]
			year = request.POST["year"]
			try:
				prereq_univ = prereq_univ_set(pid=pid,cname=cname,year=year)
				prereq_univ.save()
			except:
				return render(request, 'ta_allocation/admin_addprereqsuniv.html', {'user':request.user.username, 'str':"This Pre-Requisite already exists."})
			return render(request, 'ta_allocation/admin_addprereqsuniv.html', {'user':request.user.username, 'str':"Pre-Requisite successfully added."})
		else:
			return render(request, 'ta_allocation/admin_addprereqsuniv.html', {'user':request.user.username, 'str':""})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})



def admin_addprereqs_univ_excel(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				count_of_prereqs_added = 0
				count_of_prereqs_updated = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "hello"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						try:
							pre_entry = prereq_univ_set.objects.get(pid = row[0])
							pre_entry.cname = row[1]
							if row[2]=="1st year":
								pre_entry.year = 1
							elif row[2]=="2nd year":
								pre_entry.year = 2
							elif row[2]=="UG/PG":
								pre_entry.year = 3
							elif row[2]=="PG":
								pre_entry.year = 4
							pre_entry.save()
							count_of_prereqs_updated = count_of_prereqs_updated + 1
						except prereq_univ_set.DoesNotExist:
							if row[2]=="1st year":
								pre_entry_year = 1
							elif row[2]=="2nd year":
								pre_entry_year = 2
							elif row[2]=="UG/PG":
								pre_entry_year = 3
							elif row[2]=="PG":
								pre_entry_year = 4
							pre_entry = prereq_univ_set(pid=row[0],cname=row[1],year=pre_entry_year)
							pre_entry.save()
							count_of_prereqs_added = count_of_prereqs_added + 1
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = str(count_of_prereqs_added) + " prereqs have been added and "+ str(count_of_prereqs_updated) + " have been updated!"
			loginid = request.user.email
			form = UploadFileForm()
			return render(request, 'ta_allocation/admin_addprereqs_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/admin_addprereqs_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_allprereqs(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entries = prereq_univ_set.objects.all()
		return render(request, 'ta_allocation/admin_allprereqs.html', {'entries': entries})			
	else:
		return render(request, 'ta_allocation/index.html')


def admin_deleteprereq_univs(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	for a in param_split:
		prereq_univ_set.objects.get(aid=int(a)).delete()
	return redirect(admin_allprereqs)


def admin_addskills_univ(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here (y)"
			#print request
			
			skind = request.POST["skind"]
			sname = request.POST["sname"]
			try:
				try:
					s_kind_entry = skill_kind.objects.get(kname = skind)
				except skill_kind.DoesNotExist:
					return render(request, 'ta_allocation/admin_addskillsuniv.html', {'user':request.user.username, 'str':"There does not exist any such kind. Go back and make an entry for this kind of skills first."})
				skill_univ = skill_univ_set(sname=sname,kind=s_kind_entry)
				skill_univ.save()
			except:
				return render(request, 'ta_allocation/admin_addskillsuniv.html', {'user':request.user.username, 'str':"This Skill already exists."})
			return render(request, 'ta_allocation/admin_addskillsuniv.html', {'user':request.user.username, 'str':"Skill successfully added."})
		else:
			return render(request, 'ta_allocation/admin_addskillsuniv.html', {'user':request.user.username, 'str':""})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})



def admin_allskills(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entries = skill_univ_set.objects.all()
		print entries
		return render(request, 'ta_allocation/admin_allskills.html', {'entries': entries})
	else:
		return render(request, 'ta_allocation/index.html')


def admin_addskillkinds_univ(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here (y)"
			#print request
			
			skind = request.POST["skind"]
			try:
				s_kind_entry = skill_kind.objects.get(kname = skind)
				return render(request, 'ta_allocation/admin_addskillkindsuniv.html', {'user':request.user.username, 'str':"Skill kind with this name already exists."})
			except skill_kind.DoesNotExist:
				s_kind_entry = skill_kind(kname=skind)
				s_kind_entry.save()
			return render(request, 'ta_allocation/admin_addskillkindsuniv.html', {'user':request.user.username, 'str':"Skill kind successfully added."})
		else:
			return render(request, 'ta_allocation/admin_addskillkindsuniv.html', {'user':request.user.username, 'str':""})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})



def admin_addskills_univ_excel(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				count_of_skills_added = 0
				count_of_skills_updated = 0
				skill_kind_not_found = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "hello"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						try:
							skill_kind_entry = skill_kind.objects.get(kname = row[1])
							try:
								skill_univ_entry = skill_univ_set.objects.get(kind=skill_kind_entry, sname=row[0])
								count_of_skills_updated = count_of_skills_updated + 1
							except:
								skill_univ_entry = skill_univ_set(kind=skill_kind_entry,sname=row[0])
								skill_univ_entry.save()
								count_of_skills_added = count_of_skills_added + 1
						except skill_kind.DoesNotExist:
							skill_kind_not_found= skill_kind_not_found + 1
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = str(count_of_skills_added) + " skills have been added and "+ str(count_of_skills_updated) + " have been updated and Skill Kind not found for "+ str(skill_kind_not_found) + " !"
			loginid = request.user.email
			form = UploadFileForm()
			return render(request, 'ta_allocation/admin_addskills_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/admin_addskills_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_addskillkinds_univ_excel(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				count_of_skillkinds_exist = 0
				skill_kind_added = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "hello"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						try:
							skill_kind_entry = skill_kind.objects.get(kname = row[0])
							count_of_skillkinds_exist = count_of_skillkinds_exist + 1
						except skill_kind.DoesNotExist:
							skill_kind_entry = skill_kind(kname=row[0])
							skill_kind_entry.save()
							skill_kind_added= skill_kind_added + 1
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
				str1 = str(skill_kind_added) + " skill kinds have been added and "+ str(count_of_skillkinds_exist) + " already existed!"
			loginid = request.user.email
			form = UploadFileForm()
			return render(request, 'ta_allocation/admin_addskillkinds_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/admin_addskillkinds_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')




def admin_allskillkinds(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entries = skill_kind.objects.all()
		return render(request, 'ta_allocation/admin_allskillkinds.html', {'entries': entries})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_deleteskill_univs(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	for a in param_split:
		skill_univ_set.objects.get(aid=int(a)).delete()
	return redirect(admin_allskills)



def admin_deleteskillkind_univs(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	for a in param_split:
		skill_kind.objects.get(aid=int(a)).delete()
	return redirect(admin_allskillkinds)


def admin_viewroles(request,param):
	print "hey!"
	print param
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entries = course.objects.all()
		entry1 = role_list.objects.get(aid=int(param))
		if entry1.role==9:
			role="Admin"
		elif entry1.role==8:
			role="DOAA"
		elif entry1.role==1:
			role="Professor"
		else:
			role="Student"
		return render(request, 'ta_allocation/admin_viewroles.html', {'entry':entry1, 'role':role})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_allroles(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries = role_list.objects.all()
		return render(request, 'ta_allocation/admin_allroles.html', {'entries': entries})
	else:
		return render(request, 'ta_allocation/index.html')


def admin_deleteroles(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	for a in param_split:
		role_list.objects.get(aid=int(a)).delete()
	return redirect(admin_allroles)
	#return render(request, 'ta_allocation/admin_allroles.html',{'user':request.user.username})


def admin_addcourses(request,param=None):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here in add course post req"
			form = courses_form(request.POST)
			str = "Please enter All the values."
			if 1==1:
				print "kyu?"	
				try:
					prof1 = role_list.objects.get(loginid=request.POST['prof_id1'])
				except:	
					prof1 = role_list(loginid=request.POST['prof_id1'],role=1,status=1,program=-1)
					prof1.save()
				print "kyu2?"
				if request.POST['prof_id2']!="":
					try:
						prof2 = role_list.objects.get(loginid=request.POST['prof_id2'])
					except:	
						prof2 = role_list(loginid=request.POST['prof_id2'],role=1,status=1,program=-1)
						prof2.save()
					if(request.POST['course_type'].lower() == "core"):
						course_type_id = 1
					elif(request.POST['course_type'].lower() == "core elective"):
						course_type_id = 2
					elif(request.POST['course_type'].lower() == "required elective"):
						course_type_id = 3
					elif(request.POST['course_type'].lower() == "free elective"):
						course_type_id = 4
					else:
						course_type_id = 4
					q = course.objects.filter(sem=request.POST['sem'], year=request.POST['year'],cid__startswith=request.POST['cid'])
					if len(q) == 0:
						entry = course(cid = request.POST['cid'],cname=request.POST['cname'], reg_no=request.POST['reg_no'], cdesc=request.POST['cdesc'], sem=request.POST['sem'], year=request.POST['year'], prof_id1=prof1, prof_id2=prof2,tutors_min=request.POST['tutors_min'], tutors_max=request.POST['tutors_max'], s_ta_min=request.POST['s_ta_min'], s_ta_max=request.POST['s_ta_max'], j_ta_min=request.POST['j_ta_min'],j_ta_max=request.POST['j_ta_max'],btech_ta_min=request.POST['btech_ta_min'],btech_ta_max=request.POST['btech_ta_max'],select_max=request.POST['select_max'],course_type_id=course_type_id)	
						entry.save()
					else:
						entry = course(cid = request.POST['cid']+"_"+str(len(q)),cname=request.POST['cname'], reg_no=request.POST['reg_no'], cdesc=request.POST['cdesc'], sem=request.POST['sem'], year=request.POST['year'], prof_id1=prof1, prof_id2=prof2,tutors_min=request.POST['tutors_min'], tutors_max=request.POST['tutors_max'], s_ta_min=request.POST['s_ta_min'], s_ta_max=request.POST['s_ta_max'], j_ta_min=request.POST['j_ta_min'],j_ta_max=request.POST['j_ta_max'],btech_ta_min=request.POST['btech_ta_min'],btech_ta_max=request.POST['btech_ta_max'],select_max=request.POST['select_max'],course_type_id=course_type_id)	
						entry.save()
					

				else:
					if(request.POST['course_type'].lower() == "core"):
						course_type_id = 1
					elif(request.POST['course_type'].lower() == "core elective"):
						course_type_id = 2
					elif(request.POST['course_type'].lower() == "required elective"):
						course_type_id = 3
					elif(request.POST['course_type'].lower() == "free elective"):
						course_type_id = 4
					else:
						course_type_id = 4
					q = course.objects.filter(sem=request.POST['sem'], year=request.POST['year'],cid__startswith=request.POST['cid'])
					if len(q) == 0:
						entry = course(cid = request.POST['cid'],cname=request.POST['cname'], reg_no=request.POST['reg_no'],cdesc=request.POST['cdesc'], sem=request.POST['sem'], year=request.POST['year'], prof_id1=prof1, tutors_min=request.POST['tutors_min'], tutors_max=request.POST['tutors_max'], s_ta_min=request.POST['s_ta_min'], s_ta_max=request.POST['s_ta_max'], j_ta_min=request.POST['j_ta_min'],j_ta_max=request.POST['j_ta_max'],btech_ta_min=request.POST['btech_ta_min'],btech_ta_max=request.POST['btech_ta_max'],select_max=request.POST['select_max'],course_type_id = course_type_id)	
						entry.save()
					else:
						entry = course(cid = request.POST['cid']+"_"+str(len(q)),cname=request.POST['cname'], reg_no=request.POST['reg_no'],cdesc=request.POST['cdesc'], sem=request.POST['sem'], year=request.POST['year'], prof_id1=prof1, tutors_min=request.POST['tutors_min'], tutors_max=request.POST['tutors_max'], s_ta_min=request.POST['s_ta_min'], s_ta_max=request.POST['s_ta_max'], j_ta_min=request.POST['j_ta_min'],j_ta_max=request.POST['j_ta_max'],btech_ta_min=request.POST['btech_ta_min'],btech_ta_max=request.POST['btech_ta_max'],select_max=request.POST['select_max'],course_type_id = course_type_id)	
						entry.save()
					
				print "why?"
				str="Your details have been saved"
			doa_update_ta_min_and_max()
			return render(request, 'ta_allocation/admin_addcourses.html', {'form': form, 'str': str})
		else:
			if param==None:
				loginid = request.user.email
				courses1=prereq_univ_set.objects.filter(year=1)
				courses2=prereq_univ_set.objects.filter(year=2)
				courses3=prereq_univ_set.objects.filter(year=3)
				courses4=prereq_univ_set.objects.filter(year=4)
				s_k=skill_kind.objects.all
				skills1=skill_univ_set.objects.filter(kind=1)
				skills2=skill_univ_set.objects.filter(kind=2)
				skills3=skill_univ_set.objects.filter(kind=3)
				skills4=skill_univ_set.objects.filter(kind=4)
				skills5=skill_univ_set.objects.filter(kind=5)
				all_courses = course.objects.all()
				print "courses1 is:"
				# print courses1
				form = courses_form()
				doa_update_ta_min_and_max()
				return render(request, 'ta_allocation/admin_addcourses.html', {'form': form,'all' : all_courses, 'courses1' : courses1, 'courses2' : courses2, 'courses3' : courses3, 'courses4' : courses4, 'skills1' : skills1, 'skills2' : skills2, 'skills3' : skills3, 'skills4' : skills4, 'skills5' : skills5, 'skills_kind' : s_k})
			else:
				entry = course.objects.get(aid = param)
			
				if(entry):
					if(entry.prof_id2):
						form = courses_form(
						initial={'aid':entry.aid, 'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'prof_id2':entry.prof_id2.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
						)
					else:
						form = courses_form(
						initial={'aid':entry.aid,'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
						)
				doa_update_ta_min_and_max()
				return render(request, 'ta_allocation/editcourse.html', { 'form': form })

	else:
		return render(request, 'ta_allocation/index.html')



def admin_addcourses_excel(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		if request.method == 'POST':
			form = UploadFileForm(request.POST,request.FILES)
			str1 = "Please enter All the values."
			if form.is_valid():
				newdoc = Document(docfile=request.FILES['file'])
				newdoc.save()
				wb = xlrd.open_workbook(os.getcwd()+"/"+newdoc.docfile.name)
				sh = wb.sheet_by_name('Sheet1')
				your_csv_file = open('converted.csv', 'wb')
				wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					print sh.row_values(rownum)
					wr.writerow(sh.row_values(rownum))
				print os.path.join(os.getcwd(),'converted.csv')
				your_csv_file.close()
				count_of_users_added = 0
				count_of_users_updated = 0
				with open(os.path.join(os.getcwd(),'converted.csv'),'rb') as csvfile:
					contents = csv.reader(csvfile)
					print "hello1"
					print contents
					matrix = list()
					row_count = 0
					for row in contents:
						row_count = row_count+1
						if(row_count==1):
							continue
						str1 = ""
						print row
						print "row[0]"
						print row[0]
						matrix.append(row)
						try:
							if row[4].lower()=="monsoon":
								entry = course.objects.get(cid=row[0],sem=1,year=int(float(row[5])))

							elif row[4].lower()=="winter":
								entry = course.objects.get(cid=row[0],sem=2,year=int(float(row[5])))
							else:
								entry = course.objects.get(cid=row[0],sem=123,year=int(float(row[5]))) #to make it go to except block, since sem=123 not possible
							if row[1]!="":
								entry.cname = row[1]
							if row[2]!="":
								entry.cdesc = row[2]
							if row[3]!="":
								entry.reg_no = int(float(row[3]))
							if row[6]!="":
								try:
									entry_prof1 = role_list.objects.get(loginid=row[6].lower())
									entry.prof_id1 = entry_prof1
								except role_list.DoesNotExist:
									entry_prof1 = role_list.objects.create(loginid=row[6].lower(),role=1,status=1,program=-1)
									entry.prof_id1 = entry_prof1
							if row[7]!="":
								try:
									entry_prof2 = role_list.objects.get(loginid=row[7].lower())
									entry.prof_id2 = entry_prof2
								except role_list.DoesNotExist:
									entry_prof2 = role_list.objects.create(loginid=row[7].lower(),role=1,status=1,program=-1)
									entry.prof_id2 = entry_prof2
							if row[8]!="":
								entry.tutors_min = int(float(row[8]))
							if row[9]!="":
								entry.tutors_max = int(float(row[9]))
							if row[10]!="":
								entry.s_ta_min = int(float(row[10]))
							if row[11]!="":
								entry.s_ta_max = int(float(row[11]))
							if row[12]!="":
								entry.j_ta_min = int(float(row[12]))
							if row[13]!="":
								entry.j_ta_max = int(float(row[13]))
							if row[14]!="":
								entry.btech_ta_min = int(float(row[14]))
							if row[15]!="":
								entry.btech_ta_max = int(float(row[15]))
							if row[16]!="":
								entry.select_max = int(float(row[16]))
							if row[32]!="":
								if(row[32].lower() == "core"):
									entry.course_type_id = 1
								elif(row[32].lower() == "core elective"):
									entry.course_type_id = 2
								elif(row[32].lower() == "required elective"):
									entry.course_type_id = 3
								elif(row[32].lower() == "free elective"):
									entry.course_type_id = 4
								else:
									entry.course_type_id = 4
							entry.save()
							

							str1 = str1 + " Course details have been updated. "
							if row[17]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[17])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prereq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq1 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq1 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq1 does not exist. "
							if row[18]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[18])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prereq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq2 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq2 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq2 does not exist. "
							if row[19]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[19])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prereq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq3 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq3 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq3 does not exist. "
							if row[20]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[20])
									
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prereq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq4 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq4 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq4 does not exist. "
							if row[21]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[21])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prereq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq5 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq5 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq5 does not exist. "
							if row[22]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[22])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[23].lower()=="low":
											val = 5
										elif row[23].lower()=="medium":
											val = 7
										elif row[23].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill1 added. "
									except:
										val=0
										if row[23].lower()=="low":
											val = 5
										elif row[23].lower()=="medium":
											val = 7
										elif row[23].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill1 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill1 does not exist. "
							if row[24]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[24])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[25].lower()=="low":
											val = 5
										elif row[25].lower()=="medium":
											val = 7
										elif row[25].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill2 added. "
									except:
										val=0
										if row[25].lower()=="low":
											val = 5
										elif row[25].lower()=="medium":
											val = 7
										elif row[25].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill2 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill2 does not exist. "
							if row[26]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[26])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[27].lower()=="low":
											val = 5
										elif row[27].lower()=="medium":
											val = 7
										elif row[27].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill3 added. "
									except:
										val=0
										if row[27].lower()=="low":
											val = 5
										elif row[27].lower()=="medium":
											val = 7
										elif row[27].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill3 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill3 does not exist. "
							if row[28]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[28])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[29].lower()=="low":
											val = 5
										elif row[29].lower()=="medium":
											val = 7
										elif row[29].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill4 added. "
									except:
										val=0
										if row[29].lower()=="low":
											val = 5
										elif row[29].lower()=="medium":
											val = 7
										elif row[29].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill4 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill4 does not exist. "
							if row[30]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[30])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[31].lower()=="low":
											val = 5
										elif row[31].lower()=="medium":
											val = 7
										elif row[31].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill5 added. "
									except:
										val=0
										if row[31].lower()=="low":
											val = 5
										elif row[31].lower()=="medium":
											val = 7
										elif row[31].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill5 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill5 does not exist. "
							
							
						except course.DoesNotExist:
							str1=""
							entry_cid = row[0]
							if row[4].lower()=="monsoon":
								entry_sem = 1
							elif row[4].lower()=="winter":
								entry_sem = 2
							entry_year = int(float(row[5]))
							entry_cname = row[1]
							entry_cdesc = row[2]
							entry_reg_no = 0
							if row[3]!="":
								entry_reg_no = int(float(row[3]))
							if row[6]!="":
								try:
									entry_prof1 = role_list.objects.get(loginid=row[6].lower())
									entry_prof_id1 = entry_prof1
								except role_list.DoesNotExist:
									entry_prof1 = role_list.objects.create(loginid=row[6].lower(),role=1,status=1,program=-1)
									entry_prof_id1 = entry_prof1
							entry_prof_id2 = ""
							if row[7]!="":
								try:
									entry_prof2 = role_list.objects.get(loginid=row[7].lower())
									entry_prof_id2 = entry_prof2
								except role_list.DoesNotExist:
									entry_prof2 = role_list.objects.create(loginid=row[7].lower(),role=1,status=1,program=-1)
									entry_prof_id2 = entry_prof2
							entry_tutors_min = 0
							if row[8]!="":
								entry_tutors_min = int(float(row[8]))
							entry_tutors_max = 0
							if row[9]!="":
								entry_tutors_max = int(float(row[9]))
							entry_s_ta_min = 0
							if row[10]!="":
								entry_s_ta_min = int(float(row[10]))
							entry_s_ta_max = 0
							if row[11]!="":
								entry_s_ta_max = int(float(row[11]))
							entry_j_ta_min = 0
							if row[12]!="":
								entry_j_ta_min = int(float(row[12]))
							entry_j_ta_max = 0
							if row[13]!="":
								entry_j_ta_max = int(float(row[13]))
							entry_btech_ta_min = 0
							if row[14]!="":
								entry_btech_ta_min = int(float(row[14]))
							entry_btech_ta_max =0
							if row[15]!="":
								entry_btech_ta_max = int(float(row[15]))
							entry_select_max = 0
							if row[16]!="":
								entry_select_max = int(float(row[16]))
							entry_course_type_id = 4
							if row[32]!="":
								if(row[32].lower() == "core"):
									entry_course_type_id = 1
								elif(row[32].lower() == "core elective"):
									entry_course_type_id = 2
								elif(row[32].lower() == "required elective"):
									entry_course_type_id = 3
								elif(row[32].lower() == "free elective"):
									entry_course_type_id = 4
								else:
									entry_course_type_id = 4
							if entry_prof_id2!="":
								entry = course(cid = entry_cid,cname=entry_cname, course_type_id=entry_course_type_id, reg_no=entry_reg_no, cdesc=entry_cdesc, sem=entry_sem, year=entry_year, prof_id1=entry_prof_id1, prof_id2=entry_prof_id2,tutors_min=entry_tutors_min, tutors_max=entry_tutors_max, s_ta_min=entry_s_ta_min, s_ta_max=entry_s_ta_max, j_ta_min=entry_j_ta_min,j_ta_max=entry_j_ta_max,btech_ta_min=entry_btech_ta_min,btech_ta_max=entry_btech_ta_max,select_max=entry_select_max)	
								entry.save()
							else:
								entry = course(cid = entry_cid,cname=entry_cname, course_type_id=entry_course_type_id, reg_no=entry_reg_no, cdesc=entry_cdesc, sem=entry_sem, year=entry_year, prof_id1=entry_prof_id1,tutors_min=entry_tutors_min, tutors_max=entry_tutors_max, s_ta_min=entry_s_ta_min, s_ta_max=entry_s_ta_max, j_ta_min=entry_j_ta_min,j_ta_max=entry_j_ta_max,btech_ta_min=entry_btech_ta_min,btech_ta_max=entry_btech_ta_max,select_max=entry_select_max)	
								entry.save()
							entry.save()
							str1 = str1 + " Course has been added. "
							
							if row[17]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[17])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prerq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq1 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq1 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq1 does not exist. "
							if row[18]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[18])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prerq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq2 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq2 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq2 does not exist. "
							if row[19]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[19])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prerq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq3 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq3 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq3 does not exist. "
							if row[20]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[20])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prerq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq4 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq4 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq4 does not exist. "
							if row[21]!="":
								try:
									entry_pre = prereq_univ_set.objects.get(pid=row[21])
									try:
										existing_prereq = prereq_mapping.objects.get(cid=entry,prerq=entry_pre)
										existing_prereq.priority = 1
										existing_prereq.save()
										str1 = str1+" Prereq5 added. "
									except prereq_mapping.DoesNotExist:
										entry_pre_map = prereq_mapping.objects.create(cid=entry, prereq=entry_pre, priority=1)
										entry_pre_map.save()
										str1 = str1+" Prereq5 added. "
								except prereq_univ_set.DoesNotExist:
									str1 = str1+" Prereq5 does not exist. "
							if row[22]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[22])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[23].lower()=="low":
											val = 5
										elif row[23].lower()=="medium":
											val = 7
										elif row[23].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill1 added. "
									except:
										val=0
										if row[23].lower()=="low":
											val = 5
										elif row[23].lower()=="medium":
											val = 7
										elif row[23].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill1 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill1 does not exist. "
							if row[24]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[24])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[25].lower()=="low":
											val = 5
										elif row[25].lower()=="medium":
											val = 7
										elif row[25].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill2 added. "
									except:
										val=0
										if row[25].lower()=="low":
											val = 5
										elif row[25].lower()=="medium":
											val = 7
										elif row[25].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill2 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill2 does not exist. "
							if row[26]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[26])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[27].lower()=="low":
											val = 5
										elif row[27].lower()=="medium":
											val = 7
										elif row[27].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill3 added. "
									except:
										val=0
										if row[27].lower()=="low":
											val = 5
										elif row[27].lower()=="medium":
											val = 7
										elif row[27].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill3 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill3 does not exist. "
							if row[28]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[28])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[29].lower()=="low":
											val = 5
										elif row[29].lower()=="medium":
											val = 7
										elif row[29].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill4 added. "
									except:
										val=0
										if row[29].lower()=="low":
											val = 5
										elif row[29].lower()=="medium":
											val = 7
										elif row[29].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill4 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill4 does not exist. "
							if row[30]!="":
								try:
									entry_skill = skill_univ_set.objects.get(sname=row[30])
									try:
										existing_skill = skill_mapping.objects.get(cid=entry, skill=entry_skill)
										val=0
										if row[31].lower()=="low":
											val = 5
										elif row[31].lower()=="medium":
											val = 7
										elif row[31].lower()=="high":
											val = 9
										existing_skill.value = val
										existing_skill.save()
										str1 = str1+" Skill5 added. "
									except:
										val=0
										if row[31].lower()=="low":
											val = 5
										elif row[31].lower()=="medium":
											val = 7
										elif row[31].lower()=="high":
											val = 9
										entry_skill_map = skill_mapping.objects.create(cid=entry, skill=entry_skill, value=val)
										entry_skill_map.save()
										str1 = str1+" Skill5 added. "
								except skill_univ_set.DoesNotExist:
									str1 = str1+" Skill5 does not exist. "
							
							
    					
					print matrix
				#f = request.FILES['file'].read()		
				#wb = open_workbook(f)
				#if wb:
				#	print "yay!"
				#for sheet in wb.sheets():
				#	number_of_rows = sheet.nrows
    			#	number_of_columns = sheet.ncols
    			#	items = []

    			#	rows = []
    			#	for row in range(1, number_of_rows):
    			#		r=role_list(loginid=sheet.cell(row,0).value,role=sheet.cell(row,1).value)
    			#		r.save()
				#str="Your details have been saved"
			loginid = request.user.email
			form = UploadFileForm()
			doa_update_ta_min_and_max()
			return render(request, 'ta_allocation/admin_addcourses_excel.html', {'str': str1,'form': form})
		else:
			loginid = request.user.email
			form = UploadFileForm()
			roles_path = os.path.join(os.getcwd(),'Roles.xls')
			courses_path = os.path.join(os.getcwd(),'Courses.xls')
			prereqs_path = os.path.join(os.getcwd(),'PreRequisites.xls')
			skills_path = os.path.join(os.getcwd(),'Skills.xls')
			return render(request, 'ta_allocation/admin_addcourses_excel.html', {'form': form,'str':"", 'roles_path':roles_path})
	else:
		return render(request, 'ta_allocation/index.html')



def admin_allcourses(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries = course.objects.all()
		return render(request, 'ta_allocation/admin_allcourses.html', {'entries': entries})
	else:
		return render(request, 'ta_allocation/index.html')

def admin_deletecourses(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries = course.objects.all()
		for a in param_split:
			course.objects.get(aid=int(a)).delete()
		return redirect(admin_allcourses)
	else:
		return render(request, 'ta_allocation/index.html')

	#return render(request, 'ta_allocation/admin_allroles.html',{'user':request.user.username})


def admin_deleteprereqs(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			cid_aid = 0
			entry1 = prereq_mapping.objects.get(aid=int(param_split[0])).cid
			
			if entry.role>=8 or (((entry1.prof_id1.loginid.lower() == request.user.email.lower()) or (entry1.prof_id2.loginid.lower() == request.user.email.lower())) and entry.role>=1):
				for a in param_split:
					cid_aid = prereq_mapping.objects.get(aid=int(a)).cid.aid
					prereq_mapping.objects.get(aid=int(a)).delete()
				print "cid_aid is: "
				print cid_aid
				if entry.role == 1:
					print "hmmm"
					return HttpResponseRedirect('/professor/viewcourse/'+ str(cid_aid))
				else:
					return editcourse(request,cid_aid)
			else:
				return render(request, 'ta_allocation/index.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html')
	else:
		return render(request, 'ta_allocation/index.html')



def admin_deleteskills(request,param):
	print "hey!"
	print param
	param_split = param.split(',')
	print "param_split"
	print param_split
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			cid_aid = 0
			entry1 = skill_mapping.objects.get(aid=int(param_split[0])).cid
				
			if entry.role>=8 or (((entry1.prof_id1.loginid.lower() == request.user.email.lower()) or (entry1.prof_id2.loginid.lower() == request.user.email.lower())) and entry.role>=1):
				for a in param_split:
					cid_aid = skill_mapping.objects.get(aid=int(a)).cid.aid
					skill_mapping.objects.get(aid=int(a)).delete()
				print "cid_aid is: "
				print cid_aid
				if entry.role == 1:
					print "hmmm"
					return HttpResponseRedirect('/professor/viewcourse/'+ str(cid_aid))
				else:
					return editcourse(request,cid_aid)
			else:
				return render(request, 'ta_allocation/index.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html')
	else:
		return render(request, 'ta_allocation/index.html')

def admin_viewcourse(request,param):
	print "hey!"
	print param
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role==1):
				return redirect(prof_index)
			elif(entry.role!=8 and entry.role!=9):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entries = course.objects.all()
		entry1 = course.objects.get(aid=int(param))
		email1 = entry1.prof_id1.loginid
		email2 = ""
		if entry1.prof_id2:
			email2 = entry1.prof_id2.loginid
		prereqs = prereq_mapping.objects.filter(cid=entry1)
		prereqs_len = len(prereqs)
		skills = skill_mapping.objects.filter(cid=entry1)
		skills_len = len(skills)
		return render(request, 'ta_allocation/viewcourse.html', {'skills':skills, 'skills_len':skills_len, 'entry':entry1 , 'email1':email1, 'email2':email2, 'prereqs':prereqs, 'prereqs_len':prereqs_len})
	else:
		return render(request, 'ta_allocation/index.html')
	
def editcourse(request,param,param_error=None):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role!=8 and entry.role!=9 and entry.role!=1):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry = role_list.objects.get(loginid = request.user.email)
		entry1 = course.objects.get(aid=int(param))
		if ((entry1.prof_id1) and entry1.prof_id1.loginid != request.user.email) and ((entry1.prof_id2) and entry1.prof_id2.loginid != request.user.email) and entry.role==1:
			return redirect(prof_index)
		if request.method == 'POST':
			entry = course.objects.get(aid=int(param))
			form = courses_form(request.POST,instance=entry)
			str = "Please enter All the values."
			entry.cid = request.POST['cid']
			print "cid is:"
			print request.POST['cid']
			entry.cname = request.POST['cname']
			entry.cdesc = request.POST['cdesc']
			entry.sem = request.POST['sem']
			entry.year = request.POST['year']
			try:
				entry.prof_id1 = role_list.objects.get(loginid=request.POST['prof_id1'])
			except:	
				prof1 = role_list(loginid=request.POST['prof_id1'],role=1,status=1,program=-1)
				prof1.save()
				entry.prof_id1 = prof1

			if request.POST['prof_id2']!="":
				try:
					prof2 = role_list.objects.get(loginid=request.POST['prof_id2'])
					entry.prof_id2 = prof2
				except:	
					prof2 = role_list(loginid=request.POST['prof_id2'],role=1,status=1,program=-1)
					prof2.save()
					entry.prof_id2 = prof2
				
				
			entry.reg_no = request.POST.get('reg_no')
			entry.tutors_min = request.POST['tutors_min']
			entry.tutors_max = request.POST['tutors_max']
			entry.s_ta_min = request.POST['s_ta_min']
			entry.s_ta_max = request.POST['s_ta_max']
			entry.j_ta_min = request.POST['j_ta_min']
			entry.j_ta_max = request.POST['j_ta_max']
			entry.btech_ta_min = request.POST['btech_ta_min']
			entry.btech_ta_max = request.POST['btech_ta_max']
			entry.select_max = request.POST['select_max']
			entry.aid = param
			entry.save()
			prereqs = prereq_mapping.objects.filter(cid=entry)
			prereqs_len = len(prereqs)
			skills = skill_mapping.objects.filter(cid=entry)
			skills_len = len(skills)
			str="Your details have been saved"
			form.fields['cid'].widget.attrs['readonly'] = True
			courses1=prereq_univ_set.objects.filter(year=1)
			courses2=prereq_univ_set.objects.filter(year=2)
			courses3=prereq_univ_set.objects.filter(year=3)
			courses4=prereq_univ_set.objects.filter(year=4)
			prereq_all = prereq_univ_set.objects.all()
			s_k=skill_kind.objects.all
			skills1=skill_univ_set.objects.filter(kind=1)
			skills2=skill_univ_set.objects.filter(kind=2)
			skills3=skill_univ_set.objects.filter(kind=3)
			skills4=skill_univ_set.objects.filter(kind=4)
			skills5=skill_univ_set.objects.filter(kind=5)
			skills_all = skill_univ_set.objects.all()
			if param_error!=None:
				str=param_error
			return render(request, 'ta_allocation/editcourse.html', {'prereq_all':prereq_all, 'skills_all':skills_all, 's_k':s_k, 'courses1':courses1, 'courses2':courses2, 'courses3':courses3, 'courses4':courses4, 'skills1':skills1, 'skills2':skills2,'skills3':skills3, 'skills4':skills4, 'skills5':skills5, 'prereqs':prereqs, 'prereqs_len':prereqs_len, 'skills':skills, 'skills_len':skills_len, 'form': form, 'str': str, 'aid': param})
		else:
			
			entry = course.objects.get(aid = param)
			prereqs = prereq_mapping.objects.filter(cid=entry)
			prereqs_len = len(prereqs)
			skills = skill_mapping.objects.filter(cid=entry)
			skills_len = len(skills)
			courses1=prereq_univ_set.objects.filter(year=1)
			courses2=prereq_univ_set.objects.filter(year=2)
			courses3=prereq_univ_set.objects.filter(year=3)
			courses4=prereq_univ_set.objects.filter(year=4)
			prereq_all = prereq_univ_set.objects.all()
			s_k=skill_kind.objects.all
			skills1=skill_univ_set.objects.filter(kind=1)
			skills2=skill_univ_set.objects.filter(kind=2)
			skills3=skill_univ_set.objects.filter(kind=3)
			skills4=skill_univ_set.objects.filter(kind=4)
			skills5=skill_univ_set.objects.filter(kind=5)
			skills_all = skill_univ_set.objects.all()
			if(entry):
				if(entry.prof_id2):
					form = courses_form(
					initial={'aid':entry.aid, 'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'prof_id2':entry.prof_id2.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
					)
				else:
					form = courses_form(
					initial={'aid':entry.aid,'cid':entry.cid, 'cname':entry.cname, 'cdesc':entry.cdesc, 'sem':entry.sem, 'year':entry.year, 'prof_id1': entry.prof_id1.loginid, 'reg_no':entry.reg_no,'tutors_min':entry.tutors_min,'tutors_max':entry.tutors_max,'s_ta_min':entry.s_ta_min,'s_ta_max':entry.s_ta_max,'j_ta_min':entry.j_ta_min,'j_ta_max':entry.j_ta_max,'btech_ta_min':entry.btech_ta_min,'btech_ta_max':entry.btech_ta_max,'select_max':entry.select_max}
					)
				form.fields['cid'].widget.attrs['readonly'] = True
				if role_list.objects.get(loginid = request.user.email).role<=1:
					form.fields['select_max'].widget.attrs['readonly'] = True
					
			if param_error!=None:
				str=param_error
			return render(request, 'ta_allocation/editcourse.html', {'prereq_all':prereq_all, 'skills_all':skills_all, 's_k':s_k, 'courses1':courses1, 'courses2':courses2, 'courses3':courses3, 'courses4':courses4, 'skills1':skills1, 'skills2':skills2,'skills3':skills3, 'skills4':skills4, 'skills5':skills5, 'skills':skills, 'skills_len':skills_len, 'form': form , 'aid': entry.aid, 'cid': entry.cid, 'prereqs':prereqs, 'prereqs_len':prereqs_len })
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})

def admin_addprereq_course(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role in range(2,7)):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry1 = course.objects.get(aid=int(param))
		if ((entry1.prof_id1) and (entry1.prof_id1.loginid != request.user.email)) and ((entry1.prof_id2) and (entry1.prof_id2.loginid != request.user.email)) and entry.role==1:
			return render(request, 'ta_allocation/index.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here (y)"
			#print request
			request.method='GET'
			print "request method: "
			print request.method
			prereq_univ_aid = request.POST["pre_subjects_2"]
			prereq_mapping_priority = request.POST["pre_pri_1"]
			prereq_univ = prereq_univ_set.objects.get(aid=int(prereq_univ_aid))
			try:
				prereq_map = prereq_mapping(cid=course.objects.get(aid=int(param)),prereq=prereq_univ,priority=int(prereq_mapping_priority))
				prereq_map.save()
			except:
				if entry.role == 1:
					print "hmmm"
					return editcourse(request,param)
				else:
					return editcourse(request,param)
			if entry.role == 1:
				return editcourse(request,param)
			else:
				return editcourse(request,param)
		else:
			if entry.role == 1:
				print "hmmm"
				return editcourse(request,param)
			else:
				return editcourse(request,param)
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})


def admin_addskill_course(request,param):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
			if(entry.role==0):
				return redirect(student_index)
			elif(entry.role in range(2,7)):
				return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html', {'user':request.user.username})
		entry1 = course.objects.get(aid=int(param))
		if ((entry1.prof_id1) and (entry1.prof_id1.loginid != request.user.email)) and ((entry1.prof_id2) and (entry1.prof_id2.loginid != request.user.email)) and entry.role==1:
			return render(request, 'ta_allocation/index.html', {'user':request.user.username})
		if request.method == 'POST':
			print "came here (y)"
			#print request
			request.method='GET'
			print "request method: "
			print request.method
			skill_univ_aid = request.POST["skillname"]
			skill_mapping_value = request.POST["skillvalue"]
			print "skill_univ_aid is:"
			print skill_univ_aid
			print "skill_mapping_value is:"
			print skill_mapping_value
			skill_univ = skill_univ_set.objects.get(aid=int(skill_univ_aid))

			try:
				skill_map = skill_mapping(cid=course.objects.get(aid=int(param)),skill=skill_univ,value=int(skill_mapping_value))
				skill_map.save()
			except:
				if entry.role == 1:
					print "hmmm"
					return editcourse(request,param,"This Skill already exists.")
				else:
					return editcourse(request,param,"This Skill already exists.")
			if entry.role == 1:
				print "hmmm"
				return editcourse(request,param,"This Skill already exists.")
			else:
				return editcourse(request,param,"This Skill already exists.")
		else:
			if entry.role == 1:
				print "hmmm"
				return editcourse(request,param)
			else:
				return editcourse(request,param)
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.username})


def prereq(request):
	print "I came here in Prereqs"
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html',{'user':request.user.email})
		if request.method == 'POST':
			print "in prereq"
			flag = int(request.POST['flag'])
			cid = request.POST['cid']
			cid=cid.replace(" ","")
			print "can get cid"
			print cid
			c = course.objects.get(cid=cid)
			print "can fetch course too"
			print flag
			print cid
			if(flag>=5):
				pre_id=request.POST['pre_subjects_5']
				s = prereq_univ_set.objects.get(pid=pre_id)
				p = request.POST['pre_pri_5']
				try:
					entry = prereq_mapping.objects.get(cid=c, prereq=s)
					entry.priority = p
					entry.save()
				except prereq_mapping.DoesNotExist:
					entry = prereq_mapping.objects.create(cid=c,prereq=s,priority=p)
					entry.save()	
			if(flag>=4):
				pre_id=request.POST['pre_subjects_4']
				s = prereq_univ_set.objects.get(pid=pre_id)
				p = request.POST['pre_pri_4']
				try:
					entry = prereq_mapping.objects.get(cid=c, prereq=s)
					entry.priority = p
					entry.save()
				except prereq_mapping.DoesNotExist:
					entry = prereq_mapping.objects.create(cid=c,prereq=s,priority=p)
					entry.save()
			if(flag>=3):
				pre_id=request.POST['pre_subjects_3']
				s = prereq_univ_set.objects.get(pid=pre_id)
				p = request.POST['pre_pri_3']
				try:
					entry = prereq_mapping.objects.get(cid=c, prereq=s)
					entry.priority = p
					entry.save()
				except prereq_mapping.DoesNotExist:
					entry = prereq_mapping.objects.create(cid=c,prereq=s,priority=p)
					entry.save()
			if(flag>=2):
				pre_id=request.POST['pre_subjects_2']
				s = prereq_univ_set.objects.get(pid=pre_id)
				p = request.POST['pre_pri_2']
				try:
					entry = prereq_mapping.objects.get(cid=c, prereq=s)
					entry.priority = p
					entry.save()
				except prereq_mapping.DoesNotExist:
					entry = prereq_mapping.objects.create(cid=c,prereq=s,priority=p)
					entry.save()
			if(flag>=1):
				print "in flag>=1"
				pre_id=request.POST['pre_subjects_1']
				print "pre_id is"
				print pre_id
				s = prereq_univ_set.objects.get(pid=pre_id)
				print "s is"
				print s.pid
				print "after s"
				p = request.POST['pre_pri_1']
				print "p is"
				print p
				try:
					entry = prereq_mapping.objects.get(cid=c, prereq=s)
					entry.priority = p
					entry.save()
				except prereq_mapping.DoesNotExist:
					entry = prereq_mapping.objects.create(cid=c,prereq=s,priority=p)
					entry.save()
				print "just before returning"
			return HttpResponse("Prereqs defined")
		else:
			return render(request, 'ta_allocation/admin_index.html',{'user':request.user.email, 'str':"try not to use the address bar"})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.email})


def skill(request):
	if request.user.is_authenticated():
		try:
			entry = role_list.objects.get(loginid = request.user.email)
		except role_list.DoesNotExist:
			return render(request, 'ta_allocation/notallowed.html',{'user':request.user.email})
		if request.method == 'POST':
			print "in skill"
			flag=int(request.POST['flag'])
			cid=request.POST['cid']
			cid=cid.replace(" ","")
			print "can get cid"
			c = course.objects.get(cid=cid)
			print "can fetch course too"
			print type(flag)
			if(flag>=5):
				print "in5"
				skill_id=request.POST['skill_specific_5']
				s = skill_univ_set.objects.get(aid=skill_id)
				v=request.POST['skill_value_5']
				try:
					entry = skill_mapping.objects.get(cid=c, skill=s)
					entry.value = v
					entry.save()
				except skill_mapping.DoesNotExist:
					entry = skill_mapping.objects.create(cid=c,skill=s,value=v)
					entry.save()
			if(flag>=4):
				print "in4"
				skill_id=request.POST['skill_specific_4']
				s = skill_univ_set.objects.get(aid=skill_id)
				v=request.POST['skill_value_4']
				try:
					entry = skill_mapping.objects.get(cid=c, skill=s)
					entry.value = v
					entry.save()
				except skill_mapping.DoesNotExist:
					entry = skill_mapping.objects.create(cid=c,skill=s,value=v)
					entry.save()
			if(flag>=3):
				print "in3"
				skill_id=request.POST['skill_specific_3']
				s = skill_univ_set.objects.get(aid=skill_id)
				v=request.POST['skill_value_3']
				try:
					entry = skill_mapping.objects.get(cid=c, skill=s)
					entry.value = v
					entry.save()
				except skill_mapping.DoesNotExist:
					entry = skill_mapping.objects.create(cid=c,skill=s,value=v)
					entry.save()
			if(flag>=2):
				print "in2"
				skill_id=request.POST['skill_specific_2']
				s = skill_univ_set.objects.get(aid=skill_id)
				v=request.POST['skill_value_2']
				try:
					entry = skill_mapping.objects.get(cid=c, skill=s)
					entry.value = v
					entry.save()
				except skill_mapping.DoesNotExist:
					entry = skill_mapping.objects.create(cid=c,skill=s,value=v)
					entry.save()
			if(flag>=1):
				print "in1"
				skill_id=request.POST['skill_specific_1']
				print skill_id
				s = skill_univ_set.objects.get(aid=skill_id)
				v=request.POST['skill_value_1']
				try:
					entry = skill_mapping.objects.get(cid=c, skill=s)
					entry.value = v
					entry.save()
				except skill_mapping.DoesNotExist:
					entry = skill_mapping.objects.create(cid=c,skill=s,value=v)
					entry.save()
			str="Your course : "+cid+" has been registered"
			return render(request, 'ta_allocation/admin_index.html',{'user':request.user.email, 'str':str})
		else:
			return render(request, 'ta_allocation/admin_index.html',{'user':request.user.email, 'str':"try not to use the address bar"})
	else:
		return render(request, 'ta_allocation/index.html', {'user':request.user.email})
