from .models import Facility, Personnel, Patient, Condition
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
		feilds = ('email', 'first_name', 'last_name', 'sex', 'date_of_birth',
		 'address', 'qualification', 'is_doctor', 'is_admin')
		exclude = ('password', 'last_login', 'date_of_birth', 'is_admin', 'is_active')

class ConditionSerializer(serializers.HyperlinkedModelSerializer):
	""" 
	This class gets data from the Condtion Model
	and prepares it for serialization
	"""

	condition_doctors = PersonnelSerializer(many=True)
	class Meta:
		model = Condition
		feilds = ('condition_name', 'symptoms', 'diagnosis', 'prescription',
		 			'condition_doctors')

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
		feilds = ('identifier', 'first_name', 'last_name', 'sex', 'date_of_birth',
		 'address', 'contact', 'next_of_kin', 'conditions', 'facility_registered_from',
		 	 'visitation_date', 'next_visit')
		exclude = ('url',)