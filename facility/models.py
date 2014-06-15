import random
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

SEX = (
		('M', 'Male'),
		('F', 'Female'))

class Facility(models.Model):
	"""
	 This class defines the details about a health facility
	"""	
	name = models.CharField(max_length=50, primary_key=True)
	address = models.CharField(max_length=50)
	district = models.CharField(max_length=50)
	town = models.CharField(max_length=50)
	tel = models.CharField(max_length=50)
	email = models.EmailField()
	website = models.URLField()
	facility_head = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Facilities"

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Facility, self).save(*args, **kwargs)


class MyPersonnelManager(BaseUserManager):
	"""
	Overides default Django User class to implement
	custom Personnel User Model.
	"""

	def create_user(self, email, first_name, last_name, sex, 
		date_of_birth, address, qualification, is_doctor, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth, etc and password.
		"""
		if not email:
			raise ValueError('Users must have a valid email address')

		user = self.model(
			email = self.normalize_email(email),
			first_name = first_name,
			last_name = last_name,
			sex = sex,
			date_of_birth = date_of_birth,
			address = address,
			qualification = qualification,
			is_doctor = is_doctor,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,  email, first_name, last_name, sex,
			 date_of_birth, address, qualification, is_doctor, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""

		user = self.create_user(email,
			password=password,
			first_name = first_name,
			last_name = last_name,
			sex=sex,
			date_of_birth= date_of_birth,
			address=address,
			qualification=qualification,
			is_doctor=is_doctor
			)
		user.is_admin = True
		user.save(using=self._db)
		return user

class Personnel(AbstractBaseUser):
	
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	sex = models.CharField(max_length=1, choices=SEX)
	date_of_birth = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>')
	address = models.CharField(max_length=50)
	email = models.EmailField(
		verbose_name=u'email address',
		max_length=255,
		unique=True)
	qualification = models.CharField(max_length=50)
	is_doctor = models.BooleanField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyPersonnelManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'sex', 'date_of_birth',
	 'address', 'qualification', 'is_doctor']

	def _get_full_name(self):
		"Returns personnel's full name"
		return '%s, %s' % (self.first_name, self.last_name)
	full_name = property(_get_full_name)

	def get_full_name(self):
		# The user is identified by their full name
		return self.full_name

	def get_short_name(self):
		# The user is identified by their first name
		return self.first_name

	def has_perm(self, perm, obj=None):
		"Does the user have specific permissions"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app 'app_label'?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	class Meta:
		verbose_name_plural = "Personnel"

	def __unicode__(self):
		return self.email

class Condition(models.Model):
	condition_name = models.CharField(max_length=80, primary_key=True)
	symptoms = models.TextField()
	diagnosis = models.TextField()
	prescription = models.TextField()
	condition_doctors = models.ManyToManyField(Personnel, limit_choices_to={'is_doctor': True})

	def __unicode__(self):
		return self.condition_name

class Patient(models.Model):
	identifier = models.CharField(unique=True, max_length=255)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	sex = models.CharField(max_length=1, choices=SEX)
	date_of_birth = models.DateField()
	address = models.CharField(max_length=50)
	contact = models.CharField(max_length=50)
	next_of_kin = models.CharField(max_length=50)
	conditions = models.ManyToManyField(Condition)
	facility_registered_from = models.ForeignKey(Facility)
	vistation_date = models.DateField()
	next_visit = models.DateField()

	def _get_full_name(self):
		"Returns personnel's full name"
		return '%s %s' % (self.first_name, self.last_name)
	full_name = property(_get_full_name)

	def __unicode__(self):
		return self.full_name

	def save(self, *args, **kwargs):
		if self.facility_registered_from:
			first_three_facility_letters=self.facility_registered_from.name
			self.identifier = first_three_facility_letters.strip()[:3].upper()+"-"+str(random.randrange(1, 999, 3))+\
			"-"+str(random.randrange(1, 999, 3))
		super(Patient, self).save(*args, **kwargs)
