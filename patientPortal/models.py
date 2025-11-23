from django.db import models
from enum import Enum
from authentication.models import *

class appointments(models.Model):
    class approvalStatus(models.IntegerChoices):
        applied = 0, 'applied by patient'
        recep_approval = 1,'Approved by Receptionist'
        doct_approval = 2, 'Approved by Doctor'
    patient = models.ForeignKey(patient, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(doctor, on_delete=models.DO_NOTHING)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_to_vist = models.CharField(max_length=230)
    is_approved = models.PositiveSmallIntegerField(choices=approvalStatus.choices, default= approvalStatus.applied)
    is_rejected = models.BooleanField(default=False)
    reason_for_cancel = models.TextField()
