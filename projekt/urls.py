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
	path('admin2/', admin.site.urls),
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
	path('school/student_list', vv.schoolStudentList),
	path('school/subject_list', vv.schoolSubjectList),
	path('teacher', vv.teacherHome2),
	path('teacher/subject', vv.teacherSubject),
	path('student', vv.studentHome2),
	path('student/marks_view', vv.studentMarksView),
]
