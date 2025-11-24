from django.http import JsonResponse
from django.db.models.functions import Concat
from django.db.models import CharField,Value as V
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from authentication.models import *
from patientPortal.models import *
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F
import json, datetime

receptionist_id = 27
patient_id = 25

def view_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role.id == receptionist_id:
            data = Appointments.objects.annotate(
                patient_name =Concat('patient__user__first_name', V(" ") ,'patient__user__last_name', output_field=CharField()),
                doctor_name = Concat('doctor__user__first_name', V(" ") ,'doctor__user__last_name', output_field=CharField())
            ).values()
            return JsonResponse(list(data), safe=False, status  = 200)
        else:return JsonResponse({'error' : 'Please login with receptionist credentials'}, status = 401)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)