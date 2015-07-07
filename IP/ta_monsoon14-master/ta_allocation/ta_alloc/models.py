from django.db import models
import time,os




# Create your models here.

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/%M')
    docpath = os.getcwd()+"/documents/"+time.strftime("%Y/%m/%d/%M")



class role_list(models.Model):
	aid = models.AutoField(primary_key=True)
	loginid = models.CharField(max_length=50,unique=True)
	role = models.IntegerField(default = 1) # 0->Student 1: prof  8:admin 9:Superuser
	status = models.IntegerField(default=1) 
	program = models.IntegerField(default = 0) # -1-> Not Applicabe, 0-> BTech, 4-> MTech1stYr, 5-> MTech2ndYr, 7-> PhD
	def __unicode__(self):
		return str(self.aid)

class complaints_request(models.Model):
	aid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(role_list)
	req = models.CharField(max_length=502)

class policy(models.Model):
	course_type = models.IntegerField(primary_key=True, default=4) #1->Core 2->Core Elective 3-> Required elective 4-> Free Elective
	ratio_tutors_min =  models.IntegerField(default=1) #min value of tutors's needed according to reg no
	ratio_s_ta_min =  models.IntegerField(default=1) #min value of senior ta's needed according to reg no
	ratio_j_ta_min =  models.IntegerField(default=1) #min value of junior ta's needed according to reg no
	ratio_btech_ta_min =  models.IntegerField(default=1) #min value of btech ta's needed according to reg no
	ratio_select_max = models.IntegerField(default=1) #no of ta's an instructor can select according to reg no


class course(models.Model):
	aid = models.AutoField(primary_key=True)
	cid = models.CharField(max_length=100,unique=True)
	cname = models.CharField(max_length=500) #course name
	cdesc = models.TextField() #course description
	sem = models.IntegerField(default=1) #semester no--1 for monsoon sem and 2 for winter sem
	year = models.IntegerField(default=0) #to sort courses with year
	prof_id1 = models.ForeignKey(role_list,related_name='prof1') #professor login id from role list
	prof_id2 = models.ForeignKey(role_list, related_name='prof2', null=True, blank=True, default = None) #professor login id from role list
	reg_no = models.IntegerField(default=0) #no of registrations
	course_type = models.ForeignKey(policy)
	tutors_min =  models.IntegerField(default=0) #min value of tutors's needed
	tutors_max =  models.IntegerField(default=1) #max value of tutors's needed
	s_ta_min =  models.IntegerField(default=0) #min value of senior ta's needed
	s_ta_max =  models.IntegerField(default=1) #max value of senior ta's needed
	j_ta_min =  models.IntegerField(default=0) #min value of junior ta's needed
	j_ta_max =  models.IntegerField(default=1) #max value of junior ta's needed
	btech_ta_min =  models.IntegerField(default=0) #min value of btech ta's needed
	btech_ta_max =  models.IntegerField(default=1) #max value of btech ta's needed
	select_max = models.IntegerField(default=1) #no of ta's an instructor can select 
	status = models.IntegerField(default=1) #current status of the course
	# def calculateSelected(self):
	# 	selected_studs = student_application.objects.filter(cid=self,status=9)
	# 	new_list = []
	# 	for studs in selected_studs:
	# 		new_list.append(str(studs.uid.loginid.loginid))
	# 	return new_list
	def checkPolicy(self):
		violate=0
		self.reg_no/self.btech_ta_max
		if self.reg_no/self.btech_ta_max < self.course_type.ratio_btech_ta_min or self.reg_no/self.tutors_max < self.course_type.ratio_tutors_min or self.reg_no/self.j_ta_max < self.course_type.ratio_j_ta_min or self.reg_no/self.s_ta_max < self.course_type.ratio_s_ta_min:
			violate=1 
		return violate
	chkPolicy= property(checkPolicy)		
	def calculateSelected(self):
		selected_studs = student_allocated.objects.filter(course_id=self)
		new_list = []
		for studs in selected_studs:
			new_list.append(str(studs.student_id.loginid))
		return new_list
	selected_students = property(calculateSelected)
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("cid", "sem", "year"),)



	 

class student_allocated(models.Model):
	student_id = models.ForeignKey(role_list)
	course_id = models.ForeignKey(course)
	rank = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	class Meta:
		unique_together = (("course_id", "student_id"),)

class course_allocated(models.Model):
	course_id = models.ForeignKey(course)
	avg_score = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	median_rank = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
	ta_required = models.IntegerField(default=0)
	ta_allocated = models.IntegerField(default=0)

class student_course_scores(models.Model):
	student_id = models.ForeignKey(role_list)
	course_id = models.ForeignKey(course)
	score = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

class prereq_univ_set(models.Model):
	aid = models.AutoField(primary_key=True)
	pid = models.CharField(max_length=20) #course number
	cname = models.CharField(max_length=50) #course name
	year = models.IntegerField(default=0) #to sort courses with year
	def __unicode__(self):
		return str(self.aid)

class prereq_mapping(models.Model):
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(course)
	prereq = models.ForeignKey(prereq_univ_set)
	priority = models.IntegerField(default=1) # 1 = Essential, 0 = Preferable
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("cid", "prereq"),)

class skill_kind(models.Model):
	aid = models.AutoField(primary_key=True)
	kname = models.CharField(max_length=50, unique=True) #kind name
	def __unicode__(self):
		return str(self.aid)
	
class skill_univ_set(models.Model):
	aid = models.AutoField(primary_key=True)
	sname = models.CharField(max_length=50, unique=True) #skill name
	kind = models.ForeignKey(skill_kind)
	def __unicode__(self):
		return str(self.aid)
	
class skill_mapping(models.Model):
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(course)
	skill = models.ForeignKey(skill_univ_set)
	value = models.IntegerField(default=0)
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("cid", "skill"),)





class student_general(models.Model):
	aid = models.AutoField(primary_key=True)
	loginid = models.ForeignKey(role_list, to_field='loginid', unique=True)
	roll_no = models.CharField(max_length=50) #roll no
	name = models.CharField(max_length=50) #name
	program = models.IntegerField(default=0) #0->BTech, 4->MTech, 5->MTech2nd 7->PhD
	other_courses = models.TextField() #grades for other courses
	other_skills = models.TextField() #levels for other skills the user wants to mention
	status = models.IntegerField(default=0)
	def __unicode__(self):
		return str(self.aid)
	
class student_application(models.Model):
	aid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(student_general, to_field='loginid')
	cid = models.ForeignKey(course)
	value = models.IntegerField(default=0)
	status = models.IntegerField(default=0) #0->not selected, 1-> selected by prof, 2->alloted
	pref = models.IntegerField(default=1) 
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("uid", "cid"),)

class student_prereq_grade(models.Model):
	aid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(role_list, to_field='loginid')
	pid = models.ForeignKey(prereq_univ_set) 
	value = models.IntegerField(default=0) #grade
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("uid", "pid"),)

class student_skill_level(models.Model):
	aid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(role_list, to_field='loginid')
	sid = models.ForeignKey(skill_univ_set)
	value = models.IntegerField(default=0) #level
	def __unicode__(self):
		return str(self.aid)
	class Meta:
		unique_together = (("uid", "sid"),)


