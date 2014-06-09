from facility.serializers import FacilitySerializer, PersonnelSerializer, ConditionSerializer, PatientSerializer
from rest_framework import permissions
from rest_framework import viewsets

from django.http import HttpResponse, HttpResponseRedirect, Http404
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



def search_page(request):
    show_results = False
    form = PatientForm()
    patient=None
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query']
        if query:
            form = SearchForm({'query' : query})
            patient = \
            Patient.objects.filter(identifier__iexact=query)
    variables = RequestContext(request, { 'search_form': search_form,
        'found_patient': patient,
        'show_results': show_results,
        'form': form
    })
    return render_to_response('facility/home.html', variables)

