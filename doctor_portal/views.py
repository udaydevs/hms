from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from patientPortal.models import *
from authentication.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from authentication.functions import prescription_letter
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def appointments(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role == get_object_or_404(dropDown, key = 'Doc'):
            appointment_id = request.GET.get('appointment_id')
            data = request.POST
            accepted = data.get('accepted')
            appointment = Appointments.objects.filter(id = appointment_id)
            if appointment.exists() and appointment[0].appointment_status.key == 'ABR': 
                if appointment[0].doctor.id != request.user.id:
                    return JsonResponse({'error' : 'Only the concerned doctor can update the status'}, status = 401)   
                if accepted:
                    appointment.update(appointment_status = get_object_or_404(dropDown, 32))
                if not accepted and data.get('reason_for_cancel'):
                    appointment.update(appointment)
                    data = render_to_string('appointment_booked.html',{'first_name' : request.user.first_name, 'doctor' : appointment[0].doctor.user.first_name})
                    send_mail(
                        subject='Your appointment has been canceled',from_email= settings.EMAIL_HOST_USER, recipient_list= [request.user],
                        html_message=data,message='Hello'
                    )
                else:return JsonResponse({'error' : 'Reason for cancelation is required'}, status = 400)
            else:return JsonResponse({'error' : 'Appointment does not exist'}, status = 400)
        else:return JsonResponse({'error' : ''})
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)


def prescription(request):
     pres = prescription_letter("hello")
     return pres


