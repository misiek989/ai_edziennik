from django.shortcuts import render
from django.http import HttpResponse
from mainapp import models
from django.utils.timezone import now

# Create your views here.

def mainPage(request):
	if request.method != 'POST':
		return mainPageRender(request)
	else:
		mode = request.POST.get('mode')
		if mode == 'c':
			return addAdmin(request)
		else:
			return removeAdmin(request)

def mainPageRender(request):
	adminList = []
	adminList2 = models.Admin.objects.all().order_by('surname', 'name')
	for it in adminList2:
		c = {
			'id': it.id,
			'name': it.name,
			'surname': it.surname,
			'email': it.email,
		}
		adminList.append(c)
	
	context = {
		'adminList': adminList,
	}
	return render(request, 'adminList.html', context)


def addAdmin(request):
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
	
	return mainPageRender(request)
def removeAdmin(request):
	delId = request.POST.get('id')
	customUserDelObj = models.Admin.objects.get(id=delId).user
	customUserDelObj.delete()
	
	return mainPageRender(request)

