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
        else:return JsonResponse({'error' : 'Please login with receptionist credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)

def update_appointments(request):
    if request.user == 'POST':
        appointment_id = request.GET.get('id')
        data = request.POST
        accepted = data.get('accepted')
        appointment = Appointments.objects.filter(id = appointment_id)
        print(appointment)
        if appointment.exists():    
            if accepted:
                appointment.update(appointment_status = get_object_or_404(dropDown, 31))
            if not accepted and data.get('reason_for_cancel'):
                appointment.update(appointment)
                data = render_to_string('appointment_booked.html',{'first_name' : request.user.first_name, 'doctor' : appointment[0].doctor.user.first_name})
                send_mail(
                    subject='Your appointment has been canceled',from_email= settings.EMAIL_HOST_USER, recipient_list= [request.user],
                    html_message=data,message='Hello'
                )
        else:return JsonResponse({'error' : 'Appointment does not exist'}, status = 400)
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)