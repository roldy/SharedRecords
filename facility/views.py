from django.shortcuts import render

from .models import Facility, Personnel, Patient, Condition
from facility.serializers import FacilitySerializer, PersonnelSerializer, ConditionSerializer, PatientSerializer
from rest_framework import permissions
from rest_framework import viewsets


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
