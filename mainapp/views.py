from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from mainapp import models

from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.template import Context


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

ROLE_ADMIN = 0
ROLE_SCHOOL = 1
ROLE_TEACHER = 2
ROLE_STUDENT = 3


def getAdminId(request):
	role = request.user.role
	if role != models.CustomUser.ADMIN:
		return None
	return models.Admin.objects.get(user=request.user)
def getSchoolId(request):
	rid = request.GET.get('id', None)
	role = request.user.role
	if rid is None:
		if role != models.CustomUser.SCHOOL:
			return None, False
		return models.School.objects.get(user=request.user), False
	if role == models.CustomUser.SCHOOL:
		return models.School.objects.get(user=request.user), False
	if role == models.CustomUser.ADMIN:
		return models.School.objects.get(id=rid), True
	return None, False
def getTeacherId(request):
	rid = request.GET.get('id', None)
	role = request.user.role
	if rid is None:
		if role != models.CustomUser.TEACHER:
			return None, None
		return models.Teacher.objects.get(user=request.user), ROLE_TEACHER
	if role == models.CustomUser.TEACHER:
		return models.Teacher.objects.get(user=request.user), ROLE_TEACHER
	if role == models.CustomUser.SCHOOL:
		schoolObj = models.School.objects.get(user=request.user)
		teacherObj = models.Teacher.objects.get(id=rid)
		if teacherObj.school == schoolObj:
			return teacherObj, ROLE_SCHOOL
		return None, None
	if role == models.CustomUser.ADMIN:
		return models.Teacher.objects.get(id=rid), ROLE_ADMIN
	return None, None
def getStudentId(request):
	rid = request.GET.get('id', None)
	role = request.user.role
	if rid is None:
		if role != models.CustomUser.STUDENT:
			return None, None
		return models.Student.objects.get(user=request.user), ROLE_STUDENT
	if role == models.CustomUser.STUDENT:
		return models.Student.objects.get(user=request.user), ROLE_STUDENT
	if role == models.CustomUser.TEACHER:
		return None, None
	if role == models.CustomUser.SCHOOL:
		schoolObj = models.School.objects.get(user=request.user)
		studentObj = models.Student.objects.get(id=rid)
		if studentObj.school == schoolObj:
			return studentObj, ROLE_SCHOOL
		return None, None
	if role == models.CustomUser.ADMIN:
		return models.Student.objects.get(id=rid), ROLE_ADMIN
	return None, None
def getStudentAllowTeacherId(request, subjectStudentId):
	rid = request.GET.get('id', None)
	role = request.user.role
	if rid is None:
		if role != models.CustomUser.STUDENT:
			return None, None
		return models.Student.objects.get(user=request.user), ROLE_STUDENT
	if role == models.CustomUser.STUDENT:
		return models.Student.objects.get(user=request.user), ROLE_STUDENT
	if role == models.CustomUser.TEACHER:
		ssObj = models.SubjectStudent.objects.get(id=subjectStudentId)
		teachObj = models.Teacher.objects.get(user=request.user)
		if ssObj.subjectId.teacherId == teachObj:
			return models.Student.objects.get(id=rid), ROLE_TEACHER
		return None, None
	if role == models.CustomUser.SCHOOL:
		schoolObj = models.School.objects.get(user=request.user)
		studentObj = models.Student.objects.get(id=rid)
		if studentObj.school == schoolObj:
			return studentObj, ROLE_SCHOOL
		return None, None
	if role == models.CustomUser.ADMIN:
		return models.Student.objects.get(id=rid), ROLE_ADMIN
	return None, None

def failIfNotPOST(request):
	return request.method != 'POST'

def adminHome2(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	return adminHome2_x(request, adminObj, None)
def adminHome2_x(request, adminObj, extra):
	schoolList = []
	schoolListX1 = models.School.objects.all().order_by('surname', 'name', 'schoolName')
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
		'extra': extra,
		'adminId': adminObj.id,
		'userFName': adminObj.name,
		'userLName': adminObj.surname,
		'schoolList': schoolList,
	}
	return render(request, 'mainapp/adminRoot.html', context)
def adminAdminList(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	return adminAdminList_x(request, adminObj, None)
def adminAdminList_x(request, adminObj, extra):

	adminList = []
	adminListX1 = models.Admin.objects.all().order_by('surname', 'name')
	for sx1 in adminListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		adminList.append(c)

	context = {
		'extra': extra,
		'adminId': adminObj.id,
		'userFName': adminObj.name,
		'userLName': adminObj.surname,
		'adminList': adminList,
	}
	return render(request, 'mainapp/adminAdminList.html', context)
def adminAdd(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()

	context = {

	}
	return render(request, 'mainapp/adminAdd.html', context)
def adminAddSubmit(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')

	username = email[0: email.find('@')]
	password = username + '123'

	cs = models.CustomUser()
	cs.username = username
	cs.email = email
	cs.set_password(password)
	cs.first_name = fname
	cs.last_name = lname
	cs.is_superuser = True
	cs.is_staff = True
	cs.is_active = True
	cs.role = models.CustomUser.ADMIN
	cs.date_joined = now()
	cs.save()


	adm = models.Admin()
	adm.name = fname
	adm.surname = lname
	adm.email = email
	adm.user = cs
	adm.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return adminAdminList_x(request, adminObj, extra)
def adminRemove(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()

	adminDelId = request.GET.get('adminId')
	adminDelObj = models.Admin.objects.get(id=adminDelId)
	adminDelName = adminDelObj.name + ' ' + adminDelObj.surname

	context = {
		'adminDelId': adminDelId,
		'adminDelName': adminDelName,
	}
	return render(request, 'mainapp/adminRemove.html', context)
def adminRemoveSubmit(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	adminDelId = request.POST.get('adminId')
	customUserDelObj = models.Admin.objects.get(id=adminDelId).user
	customUserDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return adminAdminList_x(request, adminObj, extra)
def adminSchoolAdd(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()

	context = {

	}
	return render(request, 'mainapp/adminSchoolAdd.html', context)
def adminSchoolAddSubmit(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')
	sname = request.POST.get('sname')
	saddr = request.POST.get('saddr')

	username = email[0: email.find('@')]
	password = username + '123'

	cs = models.CustomUser()
	cs.username = username
	cs.email = email
	cs.set_password(password)
	cs.first_name = fname
	cs.last_name = lname
	cs.is_superuser = False
	cs.is_staff = False
	cs.is_active = True
	cs.role = models.CustomUser.SCHOOL
	cs.date_joined = now()
	cs.save()


	sch = models.School()
	sch.name = fname
	sch.surname = lname
	sch.email = email
	sch.schoolName = sname
	sch.schoolAddress = saddr
	sch.user = cs
	sch.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return adminHome2_x(request, adminObj, extra)
def adminSchoolRemove(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()

	schoolDelId = request.GET.get('schoolId')
	schoolDelObj = models.School.objects.get(id=schoolDelId)
	schoolDelName = schoolDelObj.schoolName

	context = {
		'schoolDelId': schoolDelId,
		'schoolDelName': schoolDelName,
	}
	return render(request, 'mainapp/adminSchoolRemove.html', context)
def adminSchoolRemoveSubmit(request):
	adminObj = getAdminId(request)
	if adminObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	schoolDelId = request.POST.get('schoolId')
	customUserDelObj = models.School.objects.get(id=schoolDelId).user
	customUserDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return adminHome2_x(request, adminObj, extra)

def schoolHome2(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	return schoolHome2_x(request, schoolObj, superUser, None)
def schoolHome2_x(request, schoolObj, superUser, extra):
	teacherList = []

	pageNum = request.GET.get('page')
	if pageNum is None:
		pageNumber = 1
	else:
		pageNumber = int(pageNum)

	displayCount = 30

	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount

	teacherListX1 = models.Teacher.objects.filter(school=schoolObj).order_by('surname', 'name')
	allCount = teacherListX1.count()

	entry_to = min(entry_to, allCount)
	teacherListX1 = teacherListX1[entry_from:entry_to]

	for sx1 in teacherListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		teacherList.append(c)



	pageRadius = 4

	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax

	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))

	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1

	context = {
		'extra': extra,
		'superUser': superUser,
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'teacherList': teacherList,

		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
	}
	return render(request, 'mainapp/schoolRoot.html', context)

def schoolTeacherAdd(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	context = {
		'schoolId': schoolObj.id,
		'superUser': superUser,
	}
	return render(request, 'mainapp/schoolTeacherAdd.html', context)
def schoolTeacherAddSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')

	username = email[0: email.find('@')]
	password = username + '123'

	cs = models.CustomUser()
	cs.username = username
	cs.email = email
	cs.set_password(password)
	cs.first_name = fname
	cs.last_name = lname
	cs.is_superuser = False
	cs.is_staff = False
	cs.is_active = True
	cs.role = models.CustomUser.TEACHER
	cs.date_joined = now()
	cs.save()


	tea = models.Teacher()
	tea.name = fname
	tea.surname = lname
	tea.email = email
	tea.user = cs
	tea.school = schoolObj
	tea.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return schoolHome2_x(request, schoolObj, superUser, extra)
def schoolTeacherRemove(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	teacherDelId = request.GET.get('teacherId')
	teacherDelObj = models.Teacher.objects.get(id=teacherDelId)
	teacherDelName = teacherDelObj.name + ' ' + teacherDelObj.surname

	context = {
		'schoolId': schoolObj.id,
		'superUser': superUser,
		'teacherDelId': teacherDelId,
		'teacherDelName': teacherDelName,
	}
	return render(request, 'mainapp/schoolTeacherRemove.html', context)
def schoolTeacherRemoveSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	teacherDelId = request.POST.get('teacherId')
	customUserDelObj = models.Teacher.objects.get(id=teacherDelId).user
	customUserDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return schoolHome2_x(request, schoolObj, superUser, extra)

def schoolStudentList(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	return schoolStudentList_x(request, schoolObj, superUser, None)
def schoolStudentList_x(request, schoolObj, superUser, extra):
	studentList = []

	pageNum = request.GET.get('page')
	if pageNum is None:
		pageNumber = 1
	else:
		pageNumber = int(pageNum)

	displayCount = 30

	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount

	studentListX1 = models.Student.objects.filter(school=schoolObj).order_by('surname', 'name')
	allCount = studentListX1.count()

	entry_to = min(entry_to, allCount)
	studentListX1 = studentListX1[entry_from:entry_to]

	for sx1 in studentListX1:
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'surname': sx1.surname,
			'email': sx1.email,
		}
		studentList.append(c)

	pageRadius = 4

	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax

	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))

	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1

	context = {
		'extra': extra,
		'superUser': superUser,
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'studentList': studentList,

		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
	}
	return render(request, 'mainapp/schoolStudentList.html', context)
def schoolStudentAdd(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	context = {
		'schoolId': schoolObj.id,
		'superUser': superUser,
	}
	return render(request, 'mainapp/schoolStudentAdd.html', context)
def schoolStudentAddSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')

	username = email[0: email.find('@')]
	password = username + '123'

	cs = models.CustomUser()
	cs.username = username
	cs.email = email
	cs.set_password(password)
	cs.first_name = fname
	cs.last_name = lname
	cs.is_superuser = False
	cs.is_staff = False
	cs.is_active = True
	cs.role = models.CustomUser.STUDENT
	cs.date_joined = now()
	cs.save()


	stu = models.Student()
	stu.name = fname
	stu.surname = lname
	stu.email = email
	stu.user = cs
	stu.school = schoolObj
	stu.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return schoolStudentList_x(request, schoolObj, superUser, extra)
def schoolStudentRemove(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	studentDelId = request.GET.get('studentId')
	studentDelObj = models.Student.objects.get(id=studentDelId)
	studentDelName = studentDelObj.name + ' ' + studentDelObj.surname

	context = {
		'schoolId': schoolObj.id,
		'superUser': superUser,
		'studentDelId': studentDelId,
		'studentDelName': studentDelName,
	}
	return render(request, 'mainapp/schoolStudentRemove.html', context)
def schoolStudentRemoveSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	studentDelId = request.POST.get('studentId')
	customUserDelObj = models.Student.objects.get(id=studentDelId).user
	customUserDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return schoolStudentList_x(request, schoolObj, superUser, extra)

def schoolSubjectList(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	return schoolSubjectList_x(request, schoolObj, superUser, None)
def schoolSubjectList_x(request, schoolObj, superUser, extra):
	subjectList = []

	pageNum = request.GET.get('page')
	if pageNum is None:
		pageNumber = 1
	else:
		pageNumber = int(pageNum)

	displayCount = 30

	entry_from = (pageNumber-1) * displayCount
	entry_to = entry_from + displayCount

	subjectListX1 = models.Subject.objects.filter(teacherId__school=schoolObj).order_by('name')

	allCount = subjectListX1.count()

	entry_to = min(entry_to, allCount)
	subjectListX1 = subjectListX1[entry_from:entry_to]

	for sx1 in subjectListX1:
		teacherx2 = sx1.teacherId
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'teacherId': teacherx2.id,
			'teacherName': teacherx2.name,
			'teacherSurname': teacherx2.surname,
		}
		subjectList.append(c)

	pageRadius = 4

	pageMax = int(allCount / displayCount) + 1
	pageLeft = pageNumber - pageRadius
	pageRight = pageNumber + pageRadius
	if pageLeft < 1:
		pageLeft = 1
	if pageRight > pageMax:
		pageRight = pageMax

	pages = []
	for p in range(pageLeft, pageRight + 1):
		pages.append(Context({'num': p, 'active': p == pageNumber}))

	if pageNumber <= 1:
		prevPage = None
	else:
		prevPage = pageNumber - 1
	if pageNumber >= pageMax:
		nextPage = None
	else:
		nextPage = pageNumber + 1

	context = {
		'extra': extra,
		'superUser': superUser,
		'userFName': schoolObj.name,
		'userLName': schoolObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList,

		'pages': pages,
		'prev': prevPage,
		'next': nextPage,
		'count_from': entry_from + 1,
		'count_to': entry_to,
		'count_all': allCount,
	}
	return render(request, 'mainapp/schoolSubjectList.html', context)
def schoolSubjectAdd(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	teacherId = request.GET.get('teacherId')
	teacherObj = models.Teacher.objects.get(id=teacherId)


	context = {
		'schoolId': schoolObj.id,
		'teacherId': teacherObj.id,
		'superUser': superUser,
	}
	return render(request, 'mainapp/schoolSubjectAdd.html', context)
def schoolSubjectAddSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	name = request.POST.get('name')
	teacherId = request.POST.get('teacherId')

	teacherObj = models.Teacher.objects.get(id=teacherId)


	sub = models.Subject()
	sub.name = name
	sub.teacherId = teacherObj
	sub.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return teacherHome2_x(request, teacherObj, True, extra)
def schoolSubjectRemove(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()


	pageSrc = request.GET.get('src')
	subjectDelId = request.GET.get('subjectId')
	subjectDelObj = models.Subject.objects.get(id=subjectDelId)
	subjectDelName = subjectDelObj.name

	context = {
		'schoolId': schoolObj.id,
		'teacherId': subjectDelObj.teacherId.id,
		'superUser': superUser,
		'subjectDelId': subjectDelId,
		'subjectDelName': subjectDelName,
		'pageSrc': pageSrc,
	}
	return render(request, 'mainapp/schoolSubjectRemove.html', context)
def schoolSubjectRemoveSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	pageSrc = request.GET.get('src')
	subjectDelId = request.POST.get('subjectId')
	subjectDelObj = models.Subject.objects.get(id=subjectDelId)
	teacherObj = subjectDelObj.teacherId
	subjectDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	if pageSrc is not None:
		return teacherHome2_x(request, teacherObj, True, extra)
	else:
		return schoolSubjectList_x(request, schoolObj, superUser, extra)
def schoolSubjectStudentAdd(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()

	sName = request.GET.get('sName')
	sSurname = request.GET.get('sSurname')
	subjectId = request.GET.get('subjectId')
	subjectObj = models.Subject.objects.get(id=subjectId)

	studentList = []

	if sName is not None and sSurname is not None:
		studentListX1 = models.Student.objects.filter(name__icontains=sName,surname__icontains=sSurname)
		for sx1 in studentListX1:
			c = {
				'id': sx1.id,
				'name': sx1.name,
				'surname': sx1.surname,
				'email': sx1.email,
			}
			studentList.append(c)

	if sName is None:
		sName = ''
	if sSurname is None:
		sSurname = ''


	context = {
		'sName': sName,
		'sSurname': sSurname,
		'teacherId': subjectObj.teacherId.id,
		'schoolId': schoolObj.id,
		'subjectId': subjectId,
		'superUser': superUser,
		'studentList': studentList,
	}
	return render(request, 'mainapp/schoolSubjectStudentAdd.html', context)
def schoolSubjectStudentAddSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()


	subjectId = request.GET.get('subjectId')
	subjectObj = models.Subject.objects.get(id=subjectId)

	studentId = request.POST.get('studentId')
	studentObj = models.Student.objects.get(id=studentId)

	teacherObj = subjectObj.teacherId


	sst = models.SubjectStudent()
	sst.subjectId = subjectObj
	sst.studentId = studentObj
	sst.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return teacherSubject_x(request, teacherObj, True, subjectId, None, extra)
def schoolSubjectStudentRemove(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()


	subjectStudentDelId = request.GET.get('subjectStudentId')
	subjectStudentDelObj = models.SubjectStudent.objects.get(id=subjectStudentDelId)

	studentDelName = subjectStudentDelObj.studentId.name + ' ' + subjectStudentDelObj.studentId.surname
	subjectDelName = subjectStudentDelObj.subjectId.name

	context = {
		'subjectStudentId': subjectStudentDelId,
		'schoolId': subjectStudentDelObj.studentId.school.id,
		'teacherId': subjectStudentDelObj.subjectId.teacherId.id,
		'subjectId': subjectStudentDelObj.subjectId.id,
		'superUser': superUser,
		'studentDelName': studentDelName,
		'subjectDelName': subjectDelName,
	}
	return render(request, 'mainapp/schoolSubjectStudentRemove.html', context)
def schoolSubjectStudentRemoveSubmit(request):
	schoolObj, superUser = getSchoolId(request)
	if schoolObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	#adminObj = getAdminId(request)
	subjectStudentDelId = request.POST.get('subjectStudentId')
	subjectStudentDelObj = models.SubjectStudent.objects.get(id=subjectStudentDelId)
	teacherObj = subjectStudentDelObj.subjectId.teacherId
	subjectId = subjectStudentDelObj.subjectId.id
	subjectStudentDelObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return teacherSubject_x(request, teacherObj, True, subjectId, None, extra)



def teacherHome2(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	return teacherHome2_x(request, teachObj, superUser, None)
def teacherHome2_x(request, teachObj, superUser, extra):
	schoolObj = teachObj.school

	subjectList = []

	subjectListX1 = models.Subject.objects.filter(teacherId=teachObj).order_by('name')
	for sx1 in subjectListX1:
		cnt = models.SubjectStudent.objects.filter(subjectId=sx1).count()
		c = {
			'id': sx1.id,
			'name': sx1.name,
			'cnt': cnt,
		}
		subjectList.append(c)



	context = {
		'superUser': superUser != ROLE_TEACHER,
		'superUserRole': superUser,
		'teacherId': teachObj.id,
		'extra': extra,
		'userFName': teachObj.name,
		'userLName': teachObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList
	}
	return render(request, 'mainapp/teacherRoot.html', context)


def teacherSubject(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	subjectId2 = request.GET.get('subjectId')
	pageSrc = request.GET.get('src')
	return teacherSubject_x(request, teachObj, superUser, subjectId2, pageSrc, None)
def teacherSubject_x(request, teachObj, superUser, subjectId2, pageSrc, extra):
	schoolObj = teachObj.school

	if pageSrc != 'sc':
		pageSrc = None

	subjectObj = models.Subject.objects.get(id=subjectId2)
	if subjectObj.teacherId != teachObj:
		return HttpResponseForbidden()
	studentList = []

	markColumsCount = 1

	srPlotData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	studentListX1 = models.SubjectStudent.objects.filter(subjectId=subjectId2).order_by('studentId__surname', 'studentId__name')
	for sx1 in studentListX1:
		stud = sx1.studentId

		markList = []
		markListX1 = models.Mark.objects.filter(idSubjectStudent=sx1).order_by('date')

		mCount = markListX1.count()
		if mCount > markColumsCount:
			markColumsCount = mCount

		sumMark = 0.0
		sumWeight = 0.0

		for mx1 in markListX1:
			mcolor = calcMarkColor(mx1.mark)
			sumMark = sumMark + float(mx1.mark) * float(mx1.weight)
			sumWeight = sumWeight + float(mx1.weight)
			c = {
				'id': mx1.id,
				'mark': str(mx1.mark).replace('.', ','),
				'color': mcolor,
			}
			markList.append(c)

		if mCount == 0:
			srMark = None
			srMarkColor = None
		else:
			mrkx = sumMark / sumWeight
			srMark = '%.1f' % (mrkx)
			srMarkColor = calcMarkColor(mrkx)
			mrkId = markValueToId(mrkx)
			srPlotData[mrkId] = srPlotData[mrkId] + 1

		c = {
			'ss_id': sx1.id,
			'id': stud.id,
			'name': stud.name,
			'surname': stud.surname,
			'email': stud.email,
			'markList': markList,
			'markCount': mCount,
			'srMark': str(srMark).replace('.', ','),
			'srMarkColor': srMarkColor,
		}
		studentList.append(c)

	for sx1 in studentList:
		sx1['markCount'] = range(markColumsCount - sx1['markCount'])



	context = {
		'teacherId': teachObj.id,
		'extra': extra,
		'superUser': superUser != ROLE_TEACHER,
		'superUserRole': superUser,
		'userFName': teachObj.name,
		'userLName': teachObj.surname,
		'subjectId': subjectId2,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'studentList': studentList,
		'markCount': range(markColumsCount),
		'markCountNum': markColumsCount,
		'srPlotData': srPlotData,
		'pageSrc': pageSrc,
	}
	return render(request, 'mainapp/teacherSubject.html', context)

def teacherAddMark(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()

	pageSrc = request.GET.get('src')
	subjectStudentId = request.GET.get('subjectStudentId')
	subjectStudentObj = models.SubjectStudent.objects.get(id=subjectStudentId)




	context = {
		'teacherId': teachObj.id,
		'schoolId': teachObj.school.id,
		'subjectId': subjectStudentObj.subjectId.id,
		'studentId': subjectStudentObj.studentId.id,
		'subjectStudentId': subjectStudentId,
		'superUser': superUser != ROLE_TEACHER,
		'superUserRole': superUser,
		'pageSrc': pageSrc,
	}
	return render(request, 'mainapp/teacherMarkAdd.html', context)
def teacherAddMarkSubmit(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()


	pageSrc = request.GET.get('src')
	subjectStudentId = request.GET.get('subjectStudentId')
	subjectStudentObj = models.SubjectStudent.objects.get(id=subjectStudentId)

	mark = request.POST.get('mark')
	weight = request.POST.get('weight')
	comment = request.POST.get('comment')

	if len(comment) == 0:
		comment = None

	markValue = markIdToValue(int(mark))

	mrk = models.Mark()
	mrk.date = now()
	mrk.mark = markValue
	mrk.weight = weight
	mrk.comment = comment
	mrk.idSubjectStudent = subjectStudentObj
	mrk.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	if pageSrc is None:
		return teacherSubject_x(request, teachObj, superUser, subjectStudentObj.subjectId.id, pageSrc, extra)
	else:
		return studentMarksView_x(request, subjectStudentObj.studentId, True, 't', subjectStudentObj.id, extra)
def teacherEditMark(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()

	pageSrc = request.GET.get('src')
	markId = request.GET.get('markId')
	markObj = models.Mark.objects.get(id=markId)

	markValue = markValueToId(float(markObj.mark))
	markDate = dateToStr(markObj.date)

	if markObj.comment is None:
		markComment = ''
	else:
		markComment = markObj.comment

	context = {
		'teacherId': teachObj.id,
		'markId': markId,
		'markDate': markDate,
		'markValue': markValue,
		'markWeight': markObj.weight,
		'markComment': markComment,
		'studentId': markObj.idSubjectStudent.studentId.id,
		'schoolId': teachObj.school.id,
		'subjectId': markObj.idSubjectStudent.subjectId.id,
		'subjectStudentId': markObj.idSubjectStudent.id,
		'superUser': superUser != ROLE_TEACHER,
		'superUserRole': superUser,
		'pageSrc': pageSrc,
	}
	return render(request, 'mainapp/teacherMarkEdit.html', context)

def teacherEditMarkSubmit(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	pageSrc = request.GET.get('src')
	markId = request.GET.get('markId')
	subjectId = request.GET.get('subjectId')
	markObj = models.Mark.objects.get(id=markId)

	mark = request.POST.get('mark')
	weight = request.POST.get('weight')
	comment = request.POST.get('comment')

	if len(comment) == 0:
		comment = None

	markValue = markIdToValue(int(mark))

	markObj.mark = markValue
	markObj.weight = weight
	markObj.comment = comment
	markObj.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	if pageSrc is None:
		return teacherSubject_x(request, teachObj, superUser, subjectId, pageSrc, extra)
	else:
		return studentMarksView_x(request, markObj.idSubjectStudent.studentId, True, 't', markObj.idSubjectStudent.id, extra)
def teacherRemoveMarkSubmit(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()

	pageSrc = request.GET.get('src')
	markId = request.GET.get('markId')
	subjectId = request.GET.get('subjectId')
	markObj = models.Mark.objects.get(id=markId)
	markObj.delete()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return teacherSubject_x(request, teachObj, superUser, subjectId, pageSrc, extra)

def teacherAddSubjectMark(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()


	subjectId = request.GET.get('subjectId')
	subjectObj = models.Subject.objects.get(id=subjectId)

	studentList = []

	markColumsCount = 1

	studentListX1 = models.SubjectStudent.objects.filter(subjectId=subjectObj).order_by('studentId__surname', 'studentId__name')
	sord = 0
	for sx1 in studentListX1:
		stud = sx1.studentId
		c = {
			'ss_id': sx1.id,
			'ord': sord,
			'id': stud.id,
			'name': stud.name,
			'surname': stud.surname,
		}
		sord = sord+1
		studentList.append(c)

	context = {
		'teacherId': teachObj.id,
		'schoolId': teachObj.school.id,
		'subjectId': subjectObj.id,
		'superUser': superUser != ROLE_TEACHER,
		'superUserRole': superUser,
		'studentList': studentList,
		'studentCount': len(studentList),
	}
	return render(request, 'mainapp/teacherSubjectMarkAdd.html', context)
def teacherAddSubjectMarkSubmit(request):
	teachObj, superUser = getTeacherId(request)
	if teachObj is None:
		return HttpResponseForbidden()
	if failIfNotPOST(request):
		return HttpResponseForbidden()



	subjectId = request.GET.get('subjectId')
	subjectObj = models.Subject.objects.get(id=subjectId)

	dateCurr = now()

	studCnt = int(request.POST.get('cnt'))
	for i in range(studCnt):
		ssid = request.POST.get('ord_'+str(i))
		smarkValue = request.POST.get('mark_'+str(i))
		sweight = request.POST.get('weight_'+str(i))
		scomment = request.POST.get('comment_'+str(i))
		smarkValue = markIdToValue(int(smarkValue))
		if len(scomment) == 0:
			scomment = None

		subjectStudentObj = models.SubjectStudent.objects.get(id=ssid)

		mrk = models.Mark()
		mrk.date = dateCurr
		mrk.mark = smarkValue
		mrk.weight = sweight
		mrk.comment = scomment
		mrk.idSubjectStudent = subjectStudentObj
		mrk.save()

	extra = {
		'caption': 'OK',
		'type': 'success',
	}
	return teacherSubject_x(request, teachObj, superUser, subjectId, None, extra)








def studentHome2(request):
	studObj, superUser = getStudentId(request)
	if studObj is None:
		return HttpResponseForbidden()

	schoolObj = studObj.school

	subjectList = []

	srPlotData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	subjectListX1 = models.SubjectStudent.objects.filter(studentId=studObj).order_by('subjectId__name')
	for sx1 in subjectListX1:
		subx2 = sx1.subjectId
		teacherx2 = subx2.teacherId

		markListX1 = models.Mark.objects.filter(idSubjectStudent=sx1)
		mCount = markListX1.count()
		sumMark = 0.0
		sumWeight = 0.0

		for mx1 in markListX1:
			sumMark = sumMark + float(mx1.mark) * float(mx1.weight)
			sumWeight = sumWeight + float(mx1.weight)

		if mCount == 0:
			srMark = None
			srMarkColor = None
		else:
			mrkx = sumMark / sumWeight
			srMark = '%.1f' % (mrkx)
			srMarkColor = calcMarkColor(mrkx)
			mrkId = markValueToId(mrkx)
			srPlotData[mrkId] = srPlotData[mrkId] + 1




		c = {
			'id': sx1.id,
			'name': subx2.name,
			'teacherName': teacherx2.name,
			'teacherSurname': teacherx2.surname,
			'markCount': mCount,
			'srMark': str(srMark).replace('.', ','),
			'srMarkColor': srMarkColor,
		}
		subjectList.append(c)



	context = {
		'studentId': studObj.id,
		'superUser': superUser != ROLE_STUDENT,
		'superUserRole': superUser,
		'userFName': studObj.name,
		'userLName': studObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectList': subjectList,
		'srPlotData': srPlotData,
	}
	return render(request, 'mainapp/studentRoot.html', context)
def studentMarksView(request):
	studentSubjectId = request.GET.get('studentSubjectId')
	studObj, superUser = getStudentAllowTeacherId(request, studentSubjectId)
	if studObj is None:
		return HttpResponseForbidden()
	pageSrc = request.GET.get('src')
	return studentMarksView_x(request, studObj, superUser, pageSrc, studentSubjectId, None)
def studentMarksView_x(request, studObj, superUser, pageSrc, studentSubjectId, extra):
	subjectStudentObj = models.SubjectStudent.objects.get(id=studentSubjectId)
	if subjectStudentObj.studentId != studObj:
		return HttpResponseForbidden()

	#studObj = subjectStudentObj.studentId

	schoolObj = studObj.school

	subjectObj = subjectStudentObj.subjectId
	subjectName = subjectObj.name

	srPlotData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


	markList = []

	markListX1 = models.Mark.objects.filter(idSubjectStudent=studentSubjectId).order_by('date')
	mCount = markListX1.count()
	sumMark = 0.0
	sumWeight = 0.0

	for sx1 in markListX1:
		sumMark = sumMark + float(sx1.mark) * float(sx1.weight)
		sumWeight = sumWeight + float(sx1.weight)
		mrkId = markValueToId(float(sx1.mark))
		srPlotData[mrkId] = srPlotData[mrkId] + 1
		c = {
			'id': sx1.id,
			'date': dateToStr(sx1.date),
			'mark': str(sx1.mark).replace('.', ','),
			'markColor': calcMarkColor(sx1.mark),
			'weight': sx1.weight,
			'comment': sx1.comment,
		}
		markList.append(c)

	if mCount == 0:
		srMark = None
		srMarkColor = None
	else:
		mrkx = sumMark / sumWeight
		srMark = '%.1f' % (mrkx)
		srMarkColor = calcMarkColor(mrkx)


	context = {
		'studentId': studObj.id,
		'superUser': superUser != ROLE_STUDENT,
		'superUserRole': superUser,
		'userFName': studObj.name,
		'userLName': studObj.surname,
		'schoolId': schoolObj.id,
		'schoolName': schoolObj.schoolName,
		'schoolAddress': schoolObj.schoolAddress,
		'subjectName': subjectName,
		'markList': markList,
		'srPlotData': srPlotData,
		'srMark': str(srMark).replace('.', ','),
		'srMarkColor': srMarkColor,
		'pageSrc': pageSrc,
		'extra': extra,
		'teacherId': subjectStudentObj.subjectId.teacherId.id,
		'subjectId': subjectStudentObj.subjectId.id,
		'subjectStudentId': subjectStudentObj.id,
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
def calcMarkColor(mr):
	if mr > 5.9:#6
		mcolor = '00f2b2'
	elif mr > 5.4:#5.5
		mcolor = '00f279'
	elif mr > 4.9:#5
		mcolor = '68de00'
	elif mr > 4.4:#4.5
		mcolor = '8bcc00'
	elif mr > 3.9:#4
		mcolor = 'a0cc00'
	elif mr > 3.4:#3.5
		mcolor = 'fcd200'
	elif mr > 2.9:#3
		mcolor = 'ff7700'
	elif mr > 2.4:#2.5
		mcolor = 'cc3a00'
	elif mr > 1.9:#2
		mcolor = 'e60000'
	else:#1
		mcolor = '800000'
	return mcolor
def markValueToId(mr):
	if mr > 5.9:#6
		mcolor = 9
	elif mr > 5.4:#5.5
		mcolor = 8
	elif mr > 4.9:#5
		mcolor = 7
	elif mr > 4.4:#4.5
		mcolor = 6
	elif mr > 3.9:#4
		mcolor = 5
	elif mr > 3.4:#3.5
		mcolor = 4
	elif mr > 2.9:#3
		mcolor = 3
	elif mr > 2.4:#2.5
		mcolor = 2
	elif mr > 1.9:#2
		mcolor = 1
	else:#1
		mcolor = 0
	return mcolor
def markIdToValue(mr):
	if mr == 9:#6
		mcolor = 6.0
	elif mr == 8:#5.5
		mcolor = 5.5
	elif mr == 7:#5
		mcolor = 5.0
	elif mr == 6:#4.5
		mcolor = 4.5
	elif mr == 5:#4
		mcolor = 4.0
	elif mr == 4:#3.5
		mcolor = 3.5
	elif mr == 3:#3
		mcolor = 3.0
	elif mr == 2:#2.5
		mcolor = 2.5
	elif mr == 1:#2
		mcolor = 2.0
	else:#1
		mcolor = 1.0
	return mcolor









##
