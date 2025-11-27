from django.db import models
from authentication.models import *
from authentication.constants import *


class PatientPresciption(basemodel):
    patient_data = models.ForeignKey(patient,on_delete=models.DO_NOTHING)
    doctor_data = models.ForeignKey(doctor, on_delete=models.DO_NOTHING)
    


