import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
from facility.serializers import FacilitySerializer, PersonnelSerializer, ConditionSerializer, PatientSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest
from django.template import Context, RequestContext, loader 
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

from .models import Facility, Personnel, Patient, Condition
from .forms import PatientForm, SearchForm

class FacilityViewSet(viewsets.ModelViewSet):
	queryset = Facility.objects.all()
	serializer_class = FacilitySerializer

class PersonnelViewSet(viewsets.ModelViewSet):
	queryset = Personnel.objects.all()
	serializer_class = PersonnelSerializer

class ConditionViewSet(viewsets.ModelViewSet):
	queryset = Condition.objects.all()
	serializer_class = ConditionSerializer

class PatientViewSet(viewsets.ModelViewSet):
	queryset = Patient.objects.all()
	serializer_class = PatientSerializer

class PatientDetail(APIView):
	"""
	Retrive, update or delete Patient instance
	"""
	def get_object(self, identifier):
		try:
			return Patient.objects.get(identifier=identifier)
		except Patient.DoesNotExist:
			raise Http404

	def get(self, request, identifier, format=None):
		patient = self.get_object(identifier)
		serializer = PatientSerializer(patient)
		return Response(serializer.data)

	def put(self, request, identifier, format=None):
		patient = self.get_object(identifier)
		serializer = PatientSerializer(patient, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

	def delete(self, request, identifier, format=None):
		patient=self.get_object(identifier)
		patient.delete()
		return Response(status=status.HTTP_202_NO_CONTENT)
		

search_form = SearchForm()

def index(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('facility:home',  args=(request.user.id,)))
	template = loader.get_template('facility/signin.html')
	context = RequestContext(request, {
		'error_message':'',
        })
	return HttpResponse(template.render(context))

def login_user(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('facility:home',  args=(request.user.id,)))
		user = authenticate(username=request.POST['email'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('facility:home',  args=(user.id,)))
		else:
			return render(request, 'facility/signin.html', 
				{
				'error_message':'Please check email/password combination and try again',
				})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('facility:index'))

@login_required(login_url='/')
def home(request, user_id):
	if request.method=='POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			form.save()
			if form.save():
				messages.info(request, 'The patient was successfully created')
				return HttpResponseRedirect(reverse('facility:home', args=(request.user.id,)))
			else:
				return render(request, 'facility/home.html',
					 {'user':request.user, 'form': form, 'error_message':'Sorry the user already exists'})
	else:
		form = PatientForm()
	return render(request, 'facility/home.html', {'user': request.user, 'form':form, 'search_form': search_form})

@login_required(login_url='/')
def search_page(request):
    show_results = False
    form = PatientForm()
    search_form = SearchForm()
    patient=None
    patient_obj=None
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip().upper()
        if query:
            search_form = SearchForm({'query' : query})
            patient = \
            Patient.objects.filter(identifier__iexact=query)
            if list(patient) == []:
            	patient_obj=_get_patient_data_from_alternate_facility(query)
            	form = PatientForm(instance=patient_obj)
            	form.fields["facility_registered_from"]=patient_obj.facility_registered_from
            	# form.fields["conditions"]=patient_obj.conditions
    variables = RequestContext(request, { 'search_form': search_form,
        'found_patient': patient,
        'patient_obj': patient_obj,
        'show_results': show_results,
        'form': form
    })
    return render_to_response('facility/home.html', variables)

def _get_patient_data_from_alternate_facility(query):
	r = None
	urls = {'MBA':'http://127.0.0.1:8080/api/patient/detail/', 'MUL':'http://127.0.0.1:8001/api/patient/detail/'}
	key = query.strip()[:3].upper()
	if urls.has_key(key):
		url = urls[key]
		url=url+query
		try:
			r = requests.get(url)
		except (ConnectionError, HTTPError, Timeout), e:
			print e
		if r:
			stream = BytesIO(r.text)
			try:
				data = JSONParser().parse(stream)
			except Exception, e:
				raise e
			serializer = PatientSerializer(data=data)
			if serializer.is_valid():
				return serializer.object

@login_required(login_url='/')
def update_patient_data(request, patient_id):
	patient = get_object_or_404(Patient, pk=patient_id)
	if request.method=='POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			form.save()
			if form.save():
				messages.info(request, 'The patient information was successfully updated')
				return HttpResponseRedirect(reverse('facility:home', args=(request.user.id,)))
			else:
				return render(request, 'facility/home.html',
					 {'user':request.user, 'form': form, 
					 'error_message':'Please check the patient information and try again'})
	else:
		form = PatientForm(instance=patient)
	return render(request, 'facility/home.html', {'user': request.user, 'form':form, 'search_form': search_form})

		
	