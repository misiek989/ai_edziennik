from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from mainapp import models

from django.utils.timezone import now
from django.utils.safestring import mark_safe


def mainPage(request):
	if request.user.is_authenticated:
		role = request.user.role
		if role == models.CustomUser.ADMIN:
			return adminHome(request)
		elif role == models.CustomUser.SCHOOL:
			return schoolHome(request)
		elif role == models.CustomUser.TEACHER:
			return teacherHome(request)
		elif role == models.CustomUser.STUDENT:
			return studentHome(request)
		else:
			return HttpResponse('deadbaad')
	return renderMainPage(request, False)

def loginAction(request):
	if request.method != 'POST':
		return HttpResponseForbidden()
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return redirect('/')
	return renderMainPage(request, True)
	#return HttpResponse('1')
def logoutAction(request):
	auth.logout(request)
	return redirect('/')

def renderMainPage(request, badPassword):
	context = {
		'badPassword': badPassword,
	}
	return render(request, 'mainapp/index.html', context)


def adminHome(request):
	return redirect('/admin')
def schoolHome(request):
	return redirect('/school')
def teacherHome(request):
	return redirect('/teacher')
def studentHome(request):
	return redirect('/student')


def getAdminId(request):
	rid = request.GET.get('id', None)
	if rid is None:
		role = request.user.role
		if role != models.CustomUser.ADMIN:
			return None
		return models.Admin.objects.get(user=request.user)
	return models.Admin.objects.get(id=rid)
def getSchoolId(request):
	rid = request.GET.get('id', None)
	if rid is None:
		role = request.user.role
		if role != models.CustomUser.SCHOOL:
			return None
		return models.School.objects.get(user=request.user)
	return models.School.objects.get(id=rid)
def getTeacherId(request):
	rid = request.GET.get('id', None)
	if rid is None:
		role = request.user.role
		if role != models.CustomUser.TEACHER:
			return None
		return models.Teacher.objects.get(user=request.user)
	return models.Teacher.objects.get(id=rid)
def getStudentId(request):
	rid = request.GET.get('id', None)
	if rid is None:
		role = request.user.role
		if role != models.CustomUser.STUDENT:
			return None
		return models.Student.objects.get(user=request.user)
	return models.Student.objects.get(id=rid)

def failIfNotPOST(request):
	return request.method != 'POST'


def adminHome2(request):
	adminObj = getAdminId(request)

	schoolList = []
	schoolListX1 = models.School.objects.all()
	for sx1 in schoolListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
			'schoolName': sx1.schoolName,
			'schoolAddress': sx1.schoolAddress,
		}
		schoolList.append(c)



	context = {
		'adminId': adminObj.id,
		'userFName': adminObj.name,
		'userLName': adminObj.surname,
		'schoolList': schoolList,
	}
	return render(request, 'mainapp/adminRoot.html', context)
def adminAdminList(request):
	adminObj = getAdminId(request)

	adminList = []
	adminListX1 = models.Admin.objects.all()
	for sx1 in adminListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		adminList.append(c)

	context = {
		'adminId': adminObj.id,
		'userFName': adminObj.name,
		'userLName': adminObj.surname,
		'adminList': adminList,
	}
	return render(request, 'mainapp/adminAdminList.html', context)
def adminAdd(request):
	adminObj = getAdminId(request)

	context = {

	}
	return render(request, 'mainapp/adminAdd.html', context)
def adminAddSubmit(request):
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')

	return redirect('/admin/admin_list')
def adminRemove(request):
	adminObj = getAdminId(request)

	adminDelId = request.GET.get('adminId')
	adminDelObj = models.Admin.objects.get(id=adminDelId)
	adminDelName = adminDelObj.name + ' ' + adminDelObj.surname

	context = {
		'adminDelId': adminDelId,
		'adminDelName': adminDelName,
	}
	return render(request, 'mainapp/adminRemove.html', context)
def adminRemoveSubmit(request):
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	adminId = request.POST.get('adminId')

	return redirect('/admin/admin_list')
def adminSchoolAdd(request):
	adminObj = getAdminId(request)

	context = {

	}
	return render(request, 'mainapp/adminSchoolAdd.html', context)
def adminSchoolAddSubmit(request):
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')
	sname = request.POST.get('sname')
	saddr = request.POST.get('saddr')

	return redirect('/admin')
def adminSchoolRemove(request):
	adminObj = getAdminId(request)

	schoolDelId = request.GET.get('schoolId')
	schoolDelObj = models.School.objects.get(id=schoolDelId)
	schoolDelName = schoolDelObj.schoolName

	context = {
		'schoolDelId': schoolDelId,
		'schoolDelName': schoolDelName,
	}
	return render(request, 'mainapp/adminSchoolRemove.html', context)
def adminSchoolRemoveSubmit(request):
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	schoolId = request.POST.get('schoolId')

	return redirect('/admin')


def schoolHome2(request):
	schoolObj = getSchoolId(request)

	teacherList = []

	teacherListX1 = models.Teacher.objects.filter(school=schoolObj)
	for sx1 in teacherListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		teacherList.append(c)



	context = {
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'teacherList': teacherList
	}
	return render(request, 'mainapp/schoolRoot.html', context)


def schoolStudentList(request):
	schoolObj = getSchoolId(request)

	studentList = []

	studentListX1 = models.Student.objects.filter(school=schoolObj)
	for sx1 in studentListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		studentList.append(c)



	context = {
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'studentList': studentList
	}
	return render(request, 'mainapp/schoolStudentList.html', context)


def schoolSubjectList(request):
	schoolObj = getSchoolId(request)

	subjectList = []

	subjectListX1 = models.Subject.objects.filter(teacherId__school=schoolObj)
	for sx1 in subjectListX1:
		teacherx2 = sx1.teacherId
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'teacherName': teacherx2.name,
			'teacherSurname': teacherx2.surname,
		}
		subjectList.append(c)

	context = {
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList
	}
	return render(request, 'mainapp/schoolSubjectList.html', context)





def teacherHome2(request):
	teachObj = getTeacherId(request)
	schoolObj = teachObj.school

	subjectList = []

	subjectListX1 = models.Subject.objects.filter(teacherId=teachObj)
	for sx1 in subjectListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
		}
		subjectList.append(c)



	context = {
		'teacherId': teachObj.id,
		'userFName': teachObj.name,
		'userLName': teachObj.surname,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList
	}
	return render(request, 'mainapp/teacherRoot.html', context)
def teacherSubject(request):
	teachObj = getTeacherId(request)
	schoolObj = teachObj.school


	subjectId2 = request.GET.get('subjectId')
	studentList = []

	studentListX1 = models.SubjectStudent.objects.filter(subjectId=subjectId2)
	for sx1 in studentListX1:
		stud = sx1.studentId
		c = {
			'name': stud.name,
			'surname': stud.surname,
			'email': stud.email,
		}
		studentList.append(c)



	context = {
		'teacherId': teachObj.id,
		'userFName': teachObj.name,
		'userLName': teachObj.surname,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'studentList': studentList,
	}
	return render(request, 'mainapp/teacherSubject.html', context)














def studentHome2(request):
	studObj = getStudentId(request)
	schoolObj = studObj.school

	subjectList = []

	subjectListX1 = models.SubjectStudent.objects.filter(studentId=studObj)
	for sx1 in subjectListX1:
		subx2 = sx1.subjectId
		teacherx2 = subx2.teacherId
		c = {
			'id': sx1.id,
			'name': subx2.name,
			'teacherName': teacherx2.name,
			'teacherSurname': teacherx2.surname,
			'sr': '5,0',
		}
		subjectList.append(c)



	context = {
		'studentId': studObj.id,
		'userFName': studObj.name,
		'userLName': studObj.surname,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList
	}
	return render(request, 'mainapp/studentRoot.html', context)
def studentMarksView(request):
	#studObj = getStudentId(request)

	studentSubjectId = request.GET.get('studentSubjectId')

	subjectStudentObj = models.SubjectStudent.objects.get(id=studentSubjectId)

	studObj = subjectStudentObj.studentId
	schoolObj = studObj.school

	subjectObj = subjectStudentObj.subjectId
	subjectName = subjectObj.name


	markList = []

	markListX1 = models.Mark.objects.filter(idSubjectStudent=studentSubjectId)
	for sx1 in markListX1:
		c = {
			'id': sx1.id,
			'date': dateToStr(sx1.date),
			'mark': sx1.mark,
			'weight': sx1.weight,
			'comment': sx1.comment,
		}
		markList.append(c)



	context = {
		'studentId': studObj.id,
		'userFName': studObj.name,
		'userLName': studObj.surname,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectName': subjectName,
		'markList': markList,
	}
	return render(request, 'mainapp/studentMarksView.html', context)


def dateToStr(date):
	hour = date.hour
	minute = date.minute
	seconds = date.second
	day = date.day
	month = date.month
	year = date.year
	ret = '%02d:%02d:%02d %02d.%02d.%d' % (hour, minute, seconds, day, month, year)
	return ret












##
