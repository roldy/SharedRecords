from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from facility.models import Facility, Personnel, Condition, Patient


class PersonnelCreationForm(forms.ModelForm):
	"""
	A form for creating new users. Includes all the required
	fields, plus a repeated password.
	"""
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Personnel
		fields = ('email', 'first_name', 'last_name','sex', 'date_of_birth', 'address',
		 'qualification', 'is_doctor')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(PersonnelCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class PersonnelChangeForm(forms.ModelForm):
	"""
	A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.

	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Personnel
		fields = ('email', 'first_name', 'last_name','sex', 'date_of_birth', 'address', 'qualification', 'is_doctor',
					'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

class PersonnelAdmin(UserAdmin):
	# The forms to add and change user instances
	form = PersonnelChangeForm
	add_form = PersonnelCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'full_name', 'is_doctor', 'is_admin')
	list_filter = ('is_doctor',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'sex', 'date_of_birth', 
			'address', 'qualification')}),
		('Permissions', {'fields':('is_doctor', 'is_admin')}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'first_name', 'last_name','sex', 'date_of_birth', 'address', 'qualification', 'is_doctor',
					'is_admin', 'password1', 'password2')}
			),
		)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


class FacilityAdmin(admin.ModelAdmin):
	list_display = ('name', 'facility_head', 'district', 'website')
	list_filter = ('district',)
	search_fields = ('name',)
	ordering = ('name',)


class ConditionAdmin(admin.ModelAdmin):
	list_display = ('condition_name', 'symptoms', 'prescription')
	list_filter = ('condition_name',)
	search_fields = ('condition_name',)
	ordering = ('condition_name',)


class PatientAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'sex', 'address', 'identifier', 'vistation_date', 'next_visit')
	fieldsets = (
		(None, {'fields': ('facility_registered_from', 'conditions')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'sex', 'date_of_birth')}),
		('Conatacts', {'fields':('address', 'contact', 'next_of_kin',)}),
		('Visitation', {'fields':('vistation_date', 'next_visit')}),
	)


admin.site.register(Facility, FacilityAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Patient, PatientAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)