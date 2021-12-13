"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import mainapp.views as vv


urlpatterns = [
	#path('admin2/', admin.site.urls),
	path('', vv.mainPage),
	path('login', vv.loginAction),
	path('logout', vv.logoutAction),
	path('admin', vv.adminHome2),
	path('admin/admin_list', vv.adminAdminList),
	path('admin/add_admin', vv.adminAdd),
	path('admin/add_admin_submit', vv.adminAddSubmit),
	path('admin/remove_admin', vv.adminRemove),
	path('admin/remove_admin_submit', vv.adminRemoveSubmit),
	path('admin/add_school', vv.adminSchoolAdd),
	path('admin/add_school_submit', vv.adminSchoolAddSubmit),
	path('admin/remove_school', vv.adminSchoolRemove),
	path('admin/remove_school_submit', vv.adminSchoolRemoveSubmit),
	path('school', vv.schoolHome2),
	path('school/add_teacher', vv.schoolTeacherAdd),
	path('school/add_teacher_submit', vv.schoolTeacherAddSubmit),
	path('school/remove_teacher', vv.schoolTeacherRemove),
	path('school/remove_teacher_submit', vv.schoolTeacherRemoveSubmit),
	path('school/student_list', vv.schoolStudentList),
	path('school/add_student', vv.schoolStudentAdd),
	path('school/add_student_submit', vv.schoolStudentAddSubmit),
	path('school/remove_student', vv.schoolStudentRemove),
	path('school/remove_student_submit', vv.schoolStudentRemoveSubmit),
	path('school/subject_list', vv.schoolSubjectList),
	path('school/add_subject', vv.schoolSubjectAdd),
	path('school/add_subject_submit', vv.schoolSubjectAddSubmit),
	path('school/remove_subject', vv.schoolSubjectRemove),
	path('school/remove_subject_submit', vv.schoolSubjectRemoveSubmit),
	path('school/add_subjectstudent', vv.schoolSubjectStudentAdd),
	path('school/add_subjectstudent_submit', vv.schoolSubjectStudentAddSubmit),
	path('school/remove_subjectstudent', vv.schoolSubjectStudentRemove),
	path('school/remove_subjectstudent_submit', vv.schoolSubjectStudentRemoveSubmit),
	path('teacher', vv.teacherHome2),
	path('teacher/subject', vv.teacherSubject),
	path('teacher/add_mark', vv.teacherAddMark),
	path('teacher/add_mark_submit', vv.teacherAddMarkSubmit),
	path('teacher/edit_mark', vv.teacherEditMark),
	path('teacher/edit_mark_submit', vv.teacherEditMarkSubmit),
	path('teacher/remove_mark_submit', vv.teacherRemoveMarkSubmit),
	path('teacher/add_subject_mark', vv.teacherAddSubjectMark),
	path('teacher/add_subject_mark_submit', vv.teacherAddSubjectMarkSubmit),
	path('student', vv.studentHome2),
	path('student/marks_view', vv.studentMarksView),
]
