from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from patientPortal.models import *
from authentication.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F,Q
import json
import io
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from django.http import FileResponse
from reportlab.pdfgen import canvas


def appointments(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role == get_object_or_404(dropDown, key = 'Doc'):
            appointment_id = request.GET.get('appointment_id')
            data = request.POST
            accepted = data.get('accepted')
            appointment = Appointments.objects.filter(id = appointment_id)
            if appointment.exists() and appointment[0].appointment_status.key == 'ABR':    
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
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    data = {
        "Hello" : "Uday Singh",
        "Pranshu" : "Singh"
    }
    p.drawString(0, 10, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")