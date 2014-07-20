from django.forms import ModelForm
from django import forms

from facility.models import Patient, Condition, Facility

from functools import partial 



DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class PatientForm(ModelForm):

	facility_registered_from = forms.ModelChoiceField(queryset=Facility.objects.all(),widget=forms.HiddenInput())
	class Meta:
		model = Patient
		exclude = ('identifier',)
		help_texts = {
			'date_of_birth': ('Please use the following format: <em>YYYY-MM-DD</em>',),
			'vistation_date': ('Please use the following format: <em>YYYY-MM-DD</em>',),
			'next_visit': ('Please use the following format: <em>YYYY-MM-DD</em>',)
		}

	def __init__(self, *args, **kwargs):
		super(PatientForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class':'form-control input-sm'})


class ConditionForm(ModelForm):
	class Meta:
		model = Condition

	def __init__(self, *args, **kwargs):
		super(ConditionForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class':'form-control input-sm'})


class SearchForm(forms.Form):
	query = forms.CharField(
		label='',
		widget=forms.TextInput(attrs={ 
			'class': 'form-control', 
			'placeholder': 'Search Patient...'})
		)

class OtherConditionForm(forms.Form):
	conditions = forms.ModelMultipleChoiceField(queryset=Condition.objects.all())
	date_of_visit = forms.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>')
	next_visit = forms.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>')
	patient_identifier = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		super(OtherConditionForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class':'form-control input-sm'})
		
