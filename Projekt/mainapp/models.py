from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
	ADMIN = 1
	SCHOOL = 2
	TEACHER = 3
	STUDENT = 4

	ROLE_CHOICES = (
		(ADMIN, 'Admin'),
		(SCHOOL, 'School'),
		(TEACHER, 'Teacher'),
		(STUDENT, 'Student')
	)

	role = models.PositiveSmallIntegerField(
		choices=ROLE_CHOICES,
		blank=True,
		null=True
	)

class Admin(models.Model):
	name = models.CharField(max_length=100, null=False)
	surname = models.CharField(max_length=100, null=False)
	email = models.CharField(max_length=100, null=False)

	user = models.OneToOneField(
		CustomUser,
		on_delete=models.CASCADE
	)

	def __str__(self):
		return self.name

class School(models.Model):
	name = models.CharField(max_length=100, null=False)
	surname = models.CharField(max_length=100, null=False)
	email = models.CharField(max_length=100, null=False)
	schoolName = models.CharField(max_length=100, null=False)
	schoolAddress = models.CharField(max_length=100, null=False)

	user = models.OneToOneField(
		CustomUser,
		on_delete=models.CASCADE
	)

	def __str__(self):
		return self.name

class Teacher(models.Model):
	name = models.CharField(max_length=100, null=False)
	surname = models.CharField(max_length=100, null=False)
	email = models.CharField(max_length=100, null=False)

	user = models.OneToOneField(
		CustomUser,
		on_delete=models.CASCADE
	)

	school = models.ForeignKey(
		School,
		on_delete = models.CASCADE
	)

	def __str__(self):
		return self.name

class Student(models.Model):
	name = models.CharField(max_length=100, null=False)
	surname = models.CharField(max_length=100, null=False)
	email = models.CharField(max_length=100, null=False)

	user = models.OneToOneField(
		CustomUser,
		on_delete=models.CASCADE
	)

	school = models.ForeignKey(
		School,
		on_delete = models.CASCADE
	)

	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=100, null=False)

	teacherId = models.ForeignKey(
		Teacher,
		on_delete = models.CASCADE
	)

	def __str__(self):
		return self.name

class SubjectStudent(models.Model):

	subjectId = models.ForeignKey(
		Subject,
		on_delete = models.CASCADE
	)

	studentId = models.ForeignKey(
		Student,
		on_delete = models.CASCADE
	)

	def __str__(self):
		return ''


class Mark(models.Model):
	date = models.DateTimeField()
	mark = models.FloatField()
	weight = models.IntegerField()
	comment = models.TextField(null=True)

	idSubjectStudent = models.ForeignKey(
		SubjectStudent,
		on_delete = models.CASCADE
	)

	def __str__(self):
		return self.name
