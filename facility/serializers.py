from .models import Facility, Personnel, Patient, Condition
from rest_framework import serializers



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

class ConditionSerializer(serializers.HyperlinkedModelSerializer):
	""" 
	This class gets data from the Condtion Model
	and prepares it for serialization
	"""

	condition_doctors = PersonnelSerializer(many=True)
	class Meta:
		model = Condition
		feilds = ('condition_name', 'symptoms', 'diagnosis', 'prescription', 'condition_doctors')

class PatientSerializer(serializers.HyperlinkedModelSerializer):

	""" 
	This class gets data from the Patient Model
	and prepares it for serialization
	"""

	conditions = ConditionSerializer(many=True)
	class Meta:
		model = Patient
		feilds = ('identifier', 'first_name', 'last_name', 'sex', 'date_of_birth',
		 'address', 'contact', 'next_of_kin', 'conditions', 'facility_registered_from', 'visitation_date', 'next_visit')