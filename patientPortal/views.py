from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from authentication.models import *
from .models import appointments
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F
import json


def doctors(request):
    if request.method == 'GET':
        doctors_list = doctor.objects.annotate(
            first_name = F('user__first_name'), 
            last_name = F('user__last_name'), 
            specializations = F('specialization__name')
        ).values('id', 'first_name', 'last_name', 'specializations')
        # data = render_to_string('appointment_booked.html',{'first_name' : 'Uday', 'doctor' : 'Joe'})
        # send_mail(
        #         subject='Appointment Submission',from_email= settings.EMAIL_HOST_USER, recipient_list= ['udaysinghno2005@gmail.com'],
        #         html_message=data,message='Hello'
        #     )
        return JsonResponse(list(doctors_list),safe=False, status = 200)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)
        
    
def bookAppointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role.id == 25:
            data = request.POST
            reason_to_visit = data.get('reason_to_visit')
            doctor = data.get('doctor')
            date = data.get('date')
            time = data.get('time')
            appointment, created =  appointments.objects.get_or_create(appointment_date = date, appointment_time = time, doctor = doctor, is_approved = 0, is_rejected = False)
            if created:
                appointment.patient = request.user
                appointment.reason_to_vist = reason_to_visit
                appointment.save()
                return JsonResponse({'msg' : 'Appointment Submitted and yet to be approved'}, status = 200)
            else:return JsonResponse({'msg' : 'This slot is already boooked'}, status = 200)
        else: return JsonResponse({'error' : 'Please login with patient credentials'}, status = 401)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)