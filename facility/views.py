import requests
import json
from requests.exceptions import ConnectionError, HTTPError, Timeout
from facility.serializers import FacilitySerializer, PersonnelSerializer, ConditionSerializer, PatientSerializer, OtherConditionSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import BytesIO

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, HttpResponseBadRequest
from django.template import Context, RequestContext, loader 
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Facility, Personnel, Patient, Condition
from .forms import PatientForm, SearchForm, ConditionForm, OtherConditionForm

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
	
class OtherConditionList(APIView):
	"""
	Retrive, update or delete other patient's conditions based on 
	Patient instance
	"""
	def get_objects(self, pk):
		try:
			return OtherCondition.objects.filter(patient__pk=pk)
		except OtherCondition.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		other_conditions = OtherCondition.objects.filter(patient__pk=pk)
		serializer = OtherConditionSerializer(other_conditions, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = OtherConditionSerializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


search_form = SearchForm()
condition_form = ConditionForm()
form = PatientForm()

# urls dictionary that holds urls to connected facilities
urls = {'MBA':'http://127.0.0.1:8080/api/patient/', 'MUL':'http://127.0.0.1:8001/api/patient/'}

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
	condition_form = ConditionForm()
	form = PatientForm()
	patients_list=Patient.objects.all().order_by('-next_visit')
	paginator = Paginator(patients_list, 2)
	page = request.GET.get('page')
	try:
		patients = paginator.page(page)
	except PageNotAnInteger:
		patients = paginator.page(1)
	except EmptyPage:
		patients = paginator.page(paginator.num_pages)

	variables = RequestContext(request, {'user': request.user, 
				'form':form, 
				'search_form': search_form,
				'condition_form': condition_form,
				'patients_list':patients
				})
	return render_to_response('facility/home.html', variables)

@login_required(login_url='/')
def patient_details(request, patient_id):
	patient =get_object_or_404(Patient, pk=patient_id)
	variables=RequestContext(request, {
			'patient_details': patient,
			'user': request.user,
			'search_form': search_form,
			'condition_form': ConditionForm()
			})
	return render_to_response('facility/home.html', variables)

@login_required(login_url='/')
def add_condition(request):
	if request.method=='POST':
		condition_form = ConditionForm(request.POST)
		if condition_form.is_valid():
			condition_form.save()

			# Only executed with jQuery form request
			if request.is_ajax():
				return HttpResponse('Condition was added')
			else:
				# redirect to results ok, or similar may go here
				pass
		else:
			if request.is_ajax():
				errors_dict = {}
				if condition_form.errors:
					for error in condition_form.errors:
						e = condition_form.errors[error]
						errors_dict[error] = unicode(e)
				return HttpResponseBadRequest(json.dumps(errors_dict))
			else:
				# render() form with errors (No AJAX)
				pass
	return render(request, 'facility/home.html', {'user': request.user, 'form':form, 'search_form': search_form, 
				'condition_form': condition_form})

@login_required(login_url='/')
def add_patient(request):
	form = PatientForm()
	if request.method=='POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			patient=form.save()
			if form.save():
				messages.info(request, 'The patient was successfully added')
				return HttpResponseRedirect(reverse('facility:details', args=(patient.pk,)))
			else:
				return render(request, 'facility/home.html',
					 {'user':request.user, 'form': form, 'error_message':'Sorry the user already exists'})
		messages.error(request, 'Please correct the errors and try again')

	variables = RequestContext(request, {'user': request.user, 
				'form':form, 
				'search_form': search_form,
				'condition_form': ConditionForm(),
				})
	return render_to_response('facility/home.html', variables)

@login_required(login_url='/')
def search_page(request):
    show_results = False
    form = PatientForm()
    search_form = SearchForm()
    patient=None
    patient_obj=None
    fac = None
    conditions= None
    other_conditions= None
    patient_id = None
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip().upper()
        if query:
            search_form = SearchForm({'query' : query})
            patient = \
            Patient.objects.filter(identifier__iexact=query)
            if list(patient) == []:
            	patient_obj, msg, fac, conditions, other_conditions, patient_id=_get_patient_data_from_alternate_facility(query)
            	if patient_obj == None:
            		messages.error(request, msg)
            	else:
            		messages.info(request, msg)

    variables = RequestContext(request, { 'search_form': search_form,
        'found_patient': patient,
        'patient_obj': patient_obj,
        'show_results': show_results,
        'form': form,
        'condition_form': condition_form,
        'fac':fac,
        'conditions':conditions,
        'other_conditions': other_conditions,
        'patient_id': patient_id,
        'other_condition_form': OtherConditionForm()
    })
    return render_to_response('facility/home.html', variables)

def _get_patient_data_from_alternate_facility(query):
	r = None
	obj = None
	msg= None
	fac = None
	c_msg = None
	conditions = None
	other_conditions = None
	patient_id = None
	key = query.strip()[:3].upper()
	if urls.has_key(key):
		raw_url = urls[key]
		url=raw_url+'detail/'+query
		try:
			r = requests.get(url)
			if not r:
				msg = "Sorry the patient was not found."
		except (ConnectionError, HTTPError, Timeout), e:
			print e, "\n\n"
			msg = "Sorry there was a problem in the connection. Try Again later..."
		if r:
			stream = BytesIO(r.text)
			try:
				data = JSONParser().parse(stream)	
			except Exception, e:
				raise e
			serializer = PatientSerializer(data=data, partial=True)
			if serializer.is_valid():
				obj = serializer.object
				fac = data['facility_registered_from']
				conditions = data['conditions']
				msg = "Patient information was found at  %s" % str(fac.capitalize())
				patient_id = data['id']
				other_conditions_url = raw_url+'conditions/'+str(patient_id)
				other_conditions, c_msg = _get_other_conditions(other_conditions_url)
				

	else:
		msg = "Sorry the facility with the input search is not available."
	return (obj, msg, fac, conditions, other_conditions, patient_id)

def _get_other_conditions(url):
	c_msg = None
	try:
		r = requests.get(url)
		if not r:
			c_msg = "Sorry the patient was not found."
	except (ConnectionError, HTTPError, Timeout), e:
		print e, "\n\n"
		c_msg = "Sorry there was a problem in the connection. Try Again later..."
	if r:
		stream = BytesIO(r.text)
		try:
			data = JSONParser().parse(stream)	
		except Exception, e:
			raise e
	return (data, c_msg)

@login_required(login_url='/')
def update_patient_data(request, patient_id):
	patient = get_object_or_404(Patient, pk=patient_id)
	if request.method=='POST':
		update_form = PatientForm(request.POST)
		if update_form.is_valid():
			update_form = PatientForm(request.POST, instance=patient)	
			update_form.save()
			if update_form.save():
				messages.info(request, 'The patient information was successfully updated')
				return HttpResponseRedirect(reverse('facility:details', args=(patient.pk,)))

		messages.error(request, 'Please correct the errors and try again')
	
	variables = RequestContext(request, {'user': request.user, 
				'update_form': PatientForm(instance=patient), 
				'search_form': search_form,
				'condition_form': ConditionForm(),
				'patient_id':patient.id
				})
	return render_to_response('facility/home.html', variables)	
	
def add_patient_data_from_alternate_facility(request, patient_id):
	if request.method=='POST':
		pass