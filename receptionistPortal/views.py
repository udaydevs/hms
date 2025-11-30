from django.http import JsonResponse
from django.db.models.functions import Concat
from django.db.models import Count
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
accepted_by_receptionist = 31
rejected_by_receptionist = 33

def view_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role.id == receptionist_id:
            appointment_data = Appointments.objects.annotate(
                status = F('appointment_status__name')
            ).values()

            patient_data = patient.objects.select_related('user').annotate(
                first_name = F("user__first_name"),
                last_name = F('user__last_name'),
                gender = F('user__gender__name'),
                D_O_B = F('user__birth_date'),
                patient_photo = F('user__profile_photo'),
                blood_group_name = F('blood_group__name')
            ).values()
                
            doctor_data = doctor.objects.annotate(
                first_name = F("user__first_name"),
                last_name = F('user__last_name'),
                gender = F('user__gender__name'),
                D_O_B = F('user__birth_date'),
                doctor_photo = F('user__profile_photo'),
                specialization_name = F('specialization__name'),
                qualification = F('qualifications__name')
            ).values()
            
            return JsonResponse({'appointment_data' : list(appointment_data), 'patient_data' : list(patient_data), 'doctor_data' : list(doctor_data)}, status  = 200)
        else:return JsonResponse({'error' : 'Please login with receptionist credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)

def update_appointments(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role.id == receptionist_id:
            appointment_id = request.GET.get('id')
            data = request.POST
            accepted = data.get('accepted')
            print((accepted))
            appointment = Appointments.objects.filter(id = appointment_id)
            if appointment.exists():    
                if accepted == 'True':
                    appointment.update(appointment_status = get_object_or_404(dropDown, id = accepted_by_receptionist))
                    return JsonResponse({'msg' : 'Appointment Status Updated'}, status = 200)
                if  accepted == 'False' and data.get('reason_for_cancel'):
                    appointment.update(appointment_status = get_object_or_404(dropDown, id = rejected_by_receptionist), reason_for_cancel = data.get('reason_for_cancel'))
                    # data = render_to_string('appointment_booked.html',{'first_name' : request.user.first_name, 'doctor' : appointment[0].doctor.user.first_name})
                    # send_mail(
                    #     subject='Your appointment has been canceled',from_email= settings.EMAIL_HOST_USER, recipient_list= [request.user],
                    #     html_message=data,message='Hello'
                    # )
                    return JsonResponse({'msg' : 'Appointment Status Updated'}, status = 200)
                else:return JsonResponse({'error' : 'Reason for cancellation is required'}, status =400)     
            else:return JsonResponse({'error' : 'Appointment does not exist'}, status = 400)
        else:return JsonResponse({'error' : 'Please login with receptionist credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)

def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role.id == receptionist_id:
            doctor_data = doctor.objects.all()
            appointment = Appointments.objects.count()
            patient_data = patient.objects.count()
            doctor_data = doctor.objects.aggregate(Count('id')).values()
            return JsonResponse({'appointment' : appointment, 'patient_data' : patient_data, 'doctor_data' : list(doctor_data)}, status  = 200)
        else:return JsonResponse({'error' : 'Please login with receptionist credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)