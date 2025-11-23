from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from authentication.models import *
from .models import appointments
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F
import json, datetime


def doctors(request):
    if request.method == 'GET':
        doctors_list = doctor.objects.annotate(
            first_name = F('user__first_name'), 
            last_name = F('user__last_name'), 
            specializations = F('specialization__name')
        ).values('id', 'first_name', 'last_name', 'specializations')
        return JsonResponse(list(doctors_list),safe=False, status = 200)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)
        
    
def bookAppointment(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role.id == 25:
            data = request.POST
            reason_to_visit = data.get('reason_to_visit')
            doctor_id = data.get('doctor')
            date = data.get('date')
            time = data.get('time')
            if not (datetime.datetime.strptime(date, '%Y-%m-%d')  > (datetime.datetime.today() + datetime.timedelta(days = 7))):
                return JsonResponse({'error' : "Please choose a valid date"},status = 400)
            if not doctor_id:
                return JsonResponse({'error' : 'Please choose a doctor'},status = 400)
            if not reason_to_visit:
                return JsonResponse({'error' : 'Reason to visit is required'}, status = 400)
            appointment, created =  appointments.objects.get_or_create(
                appointment_date = date, 
                appointment_time = time, 
                doctor = doctor.objects.get(id = doctor_id), 
                appointment_status = dropDown.objects.get(id = 30)
            )
            if created:
                appointment.patient = patient.objects.get(user = request.user.id)
                appointment.reason_to_vist = reason_to_visit
                appointment.save()
                data = render_to_string('appointment_booked.html',{'first_name' : 'Uday', 'doctor' : 'Joe'})
                send_mail(
                    subject='Appointment Submission',from_email= settings.EMAIL_HOST_USER, recipient_list= [request.user],
                    html_message=data,message='Hello'
                )
                return JsonResponse({'msg' : 'Appointment Submitted'}, status = 200)
            else:return JsonResponse({'msg' : 'This slot is already boooked'}, status = 400)
        else: return JsonResponse({'error' : 'Please login with patient credentials'}, status = 401)
    elif request.method == 'GET':
        if request.user.is_authenticated and request.user.role.id == 25:
            appointments_data = appointments.objects.annotate(status = F('appointment_status__name')).filter(patient__user = request.user.id).values()                
            return JsonResponse(list(appointments_data),safe=False, status = 200)
        else:return JsonResponse({'error' : 'Please login with patient credentials'}, status = 400)
    else:return JsonResponse({'error' : 'Invalid request method'}, status = 405)


