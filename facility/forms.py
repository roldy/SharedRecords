from django.forms import ModelForm
from django import forms

from facility.models import Patient, Condition

class PatientForm(ModelForm):
	class Meta:
		error_css_class = 'errorlist'
		required_css_class = 'errorlist'
		model = Patient
		fields = ('first_name', 'last_name', 'sex', 'date_of_birth', 'address', 'contact', 'next_of_kin', 
		 			'conditions', 'facility_registered_from', 'vistation_date', 'next_visit' )
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


	def __init__(self, *args, **kwargs):
		super(OtherConditionForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class':'form-control input-sm'})
