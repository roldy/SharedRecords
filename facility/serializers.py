from .models import Facility, Personnel, Patient, Condition, OtherCondition
from rest_framework import serializers
from rest_framework import renderers
from rest_framework.decorators import link


class FacilitySerializer(serializers.ModelSerializer):
	""" 
	This class gets data from the Facility Model
	and prepares it for serialization
	"""
	
	class Meta:
		model = Facility
		feilds = ('name', 'address', 'district', 'town', 'tel', 'email', 'website', 'facility_head')

class PersonnelSerializer(serializers.ModelSerializer):
	""" 
	This class gets data from the Personnel Model
	and prepares it for serialization
	"""

	class Meta:
		model = Personnel
		exclude = ('password', 'last_login', 'date_of_birth', 'is_admin', 'is_active')

class ConditionSerializer(serializers.HyperlinkedModelSerializer):
	""" 
	This class gets data from the Condtion Model
	and prepares it for serialization
	"""
	condition_name = serializers.Field(source='condition_name')
	condition_doctors = PersonnelSerializer(many=True)
	class Meta:
		model = Condition

	@link(renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, request, *args, **kwargs):
		condition = self.get_object()
		return Response(condition.highlighted)

class PatientSerializer(serializers.HyperlinkedModelSerializer):

	""" 
	This class gets data from the Patient Model
	and prepares it for serialization
	"""
	facility_registered_from = serializers.Field(source='facility_registered_from.name')
	conditions = ConditionSerializer(many=True)
	class Meta:
		model = Patient
		fields = ('id', 'identifier', 'first_name', 'last_name', 'sex', 'date_of_birth',
		 'address', 'contact', 'next_of_kin', 'conditions', 'facility_registered_from',
		 	 'vistation_date', 'next_visit')
		exclude = ('url',)

class OtherConditionSerializer(serializers.ModelSerializer):
	class Meta:
		model = OtherCondition