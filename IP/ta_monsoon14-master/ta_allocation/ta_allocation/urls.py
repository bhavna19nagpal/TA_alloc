from django.conf.urls import patterns, include, url
from views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ta_allocation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', index, name='home'), #index page
	url(r'^members/', index, name='home'), #Home page(Choose whether a ta or a professor)
	url(r'^logout$', logout), #LogOut
	


	#Students' URLs

	url(r'^ta/$', student_index, name='index'), #TA's home page
	url(r'^ta/mycourses/$', student_mycourses, name='mycourses'), #TA's profile page
	url(r'^ta/profile/$', student_profile, name='profile'), #TA's profile page
	url(r'^ta/profile/courses$', student_grades, name='grades'), #TA's profile page (grades)
	url(r'^ta/profile/skills$', student_skills1, name='skills'), #TA's profile page (skills)
	url(r'^ta/profile/enable$', student_enable, name='enable'),
	url(r'^ta/profile/disable$', student_disable, name='disable'),
	url(r'^ta/apply/$', student_apply, name='apply'), #apply for courses
	url(r'^ta/apply/details$', student_cdetails, name='details'), #details for courses
	url(r'^ta/apply/done$', student_cdone, name='done'), #done



	#Professors' URLs:

	url(r'^professor/$', prof_index, name='index'), #professor's home page
	url(r'^professor/add/$', prof_add, name='add'), #add courses
	url(r'^professor/skill/$', skill, name='skill'), #add skills to courses
	url(r'^professor/prereq', prereq, name='prereq'), #add prereqs to courses
	url(r'^professor/viewcourse/(?P<param>.+)', prof_viewcourse, name='index'),
	url(r'^professor/editcourse/(?P<param>.+)', editcourse, name='index'),
	url(r'^professor/mycourses/$', prof_allcourses, name='mycourses'), #courses of a logged in professor
	# url(r'^professor/mycourses/select$', prof_selectta, name='selectta'), #edit course details
	url(r'^professor/applications/(?P<param>.+)', prof_applications, name='selectta'), #edit course details
	


	#DOA's URLs:

	url(r'^doa/$', doa_index, name='index'), 
	url(r'^doa/allapplications$', doa_allapplications, name='index'), 
	url(r'^doa/doa_algodone$', doa_algodone, name='index'), 
	url(r'^doa/download_algoresult$', doa_download_algoresult, name='index'), 
	url(r'^doa/allocation$', doa_allocation, name='index'), 
	url(r'^doa/reminder$', doa_reminder, name='index'),
	url(r'^doa/confirmation$', doa_confirmation, name='index'), 
	url(r'^doa/run_algo$', doa_run_algo, name='index'), 
	url(r'^doa/run_algoresult$', doa_algo_results, name='index'), 
	url(r'^doa/policy$', doa_upload_policy, name='index'),
	url(r'^doa/policyshow$', doa_policyshow, name='index'),
	url(r'^doa/download_policyxls$', doa_download_policyxls, name='index'),
	url(r'^doa/download_registrationxls$', doa_download_registrationdataxls, name='index'),
	url(r'^doa/registration$', doa_upload_registration, name='index'),
	url(r'^doa/results$', doa_results, name='index'),
	url(r'^doa/courseresults/(?P<param>.+)$', doa_courseresults, name='index'),
	url(r'^doa/viewuserprofile/(?P<param>.+)$', viewuserprofile, name='/doa/allapplications'),
	
	#url(r'^doa/csv/$', views.dcsv, name='dcsv'),
	#url(r'^doa/selectedta/$', views.selectedta, name='selectedta'),



	url(r'^admin/$', admin_index, name='index'),
	url(r'^admin/addprereq$', admin_addprereqs_univ, name='index'),
	url(r'^admin/addprerequnivs/excels$', admin_addprereqs_univ_excel, name='index'),
	url(r'^admin/allprereqs$', admin_allprereqs, name='index'),
	url(r'^admin/delete_prereq_univs/(?P<param>.+)', admin_deleteprereq_univs, name='index'),
	url(r'^admin/addskillkind$', admin_addskillkinds_univ, name='index'),
	url(r'^admin/addskillkindunivs/excels$', admin_addskillkinds_univ_excel, name='index'),
	url(r'^admin/allskillkinds$', admin_allskillkinds, name='index'),
	url(r'^admin/delete_skillkind_univs/(?P<param>.+)', admin_deleteskillkind_univs, name='index'),
	url(r'^admin/addskill$', admin_addskills_univ, name='index'),
	url(r'^admin/addskillunivs/excels$', admin_addskills_univ_excel, name='index'),
	url(r'^admin/allskills$', admin_allskills, name='index'),
	url(r'^admin/delete_skill_univs/(?P<param>.+)', admin_deleteskill_univs, name='index'),
	url(r'^admin/download_rolesxls$', admin_download_rolesxls, name='index'),
	url(r'^admin/download_coursesxls$', admin_download_coursesxls, name='index'),
	url(r'^admin/download_prereqsxls$', admin_download_prereqsxls, name='index'),
	url(r'^admin/download_skillsxls$', admin_download_skillsxls, name='index'),
	url(r'^admin/addusers/excels$', admin_addroles_excel, name='index'),
	url(r'^admin/addusers$', admin_addroles, name='index'),
	url(r'^admin/viewuser/(?P<param>.+)', admin_viewroles, name='index'),
	url(r'^admin/edituser/(?P<param>.+)', admin_editroles, name='index'),
	url(r'^admin/viewuserprofile/(?P<param>.+)', viewuserprofile, name='/admin/allusers'),
	url(r'^admin/allusers', admin_allroles, name='index'),
	url(r'^admin/addcourses/excels$', admin_addcourses_excel, name='index'),
	url(r'^admin/addcourses', admin_addcourses, name='index'),
	url(r'^admin/viewcourse/(?P<param>.+)', admin_viewcourse, name='index'),
	url(r'^admin/editcourse/(?P<param>.+)', editcourse, name='index'),
	url(r'^admin/allcourses', admin_allcourses, name='index'),
	url(r'^admin/delete_users/(?P<param>.+)', admin_deleteroles, name='index'),
	url(r'^admin/delete_courses/(?P<param>.+)', admin_deletecourses, name='index'),
	url(r'^admin/delete_prereqs/(?P<param>.+)', admin_deleteprereqs, name='index'),
	url(r'^admin/delete_skills/(?P<param>.+)', admin_deleteskills, name='index'),
	url(r'^admin/addprereq_course/(?P<param>.+)', admin_addprereq_course, name='index'),
	url(r'^admin/addskill_course/(?P<param>.+)', admin_addskill_course, name='index'),
	url('', include('social.apps.django_app.urls', namespace='social')),
)
