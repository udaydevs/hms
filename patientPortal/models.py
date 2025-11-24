from django.db import models
from enum import Enum
from authentication.models import *

class Appointments(models.Model):
    patient = models.ForeignKey(patient, on_delete=models.DO_NOTHING, null=True, related_name='patient')
    doctor = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, related_name='doctor')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_to_vist = models.CharField(max_length=230)
    appointment_status = models.ForeignKey(dropDown, on_delete=models.SET_DEFAULT, default=30)
    reason_for_cancel = models.TextField()
