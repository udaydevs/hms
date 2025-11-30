from django.http import JsonResponse,FileResponse
from django.shortcuts import get_object_or_404
from patientPortal.models import *
from authentication.models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from io import BytesIO
from django.db.models import F




def dashboard(request):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.role == get_object_or_404(dropDown, key = 'Doc'):
            appointmnet_data = Appointments.objects.filter(doctor = request.user.id).annotate(patient_name = F('patient__user__first_name')).values()
            return JsonResponse(list(appointmnet_data), safe=False, status = 200)
        else:return JsonResponse({'error' : 'Please login with doctor credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)

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
                if accepted == 'True':
                    appointment.update(appointment_status = get_object_or_404(dropDown, 32))
                if accepted == 'False' and data.get('reason_for_cancel'):
                    appointment.update(appointment)
                    data = render_to_string('appointment_booked.html',{'first_name' : request.user.first_name, 'doctor' : appointment[0].doctor.user.first_name})
                    send_mail(
                        subject='Your appointment has been canceled',from_email= settings.EMAIL_HOST_USER, recipient_list= [request.user],
                        html_message=data,message='Hello'
                    )
                else:return JsonResponse({'error' : 'Reason for cancelation is required'}, status = 400)
            else:return JsonResponse({'error' : 'Appointment does not exist'}, status = 400)
        else:return JsonResponse({'error' : 'Please login with doctor credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)


def prescription(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role == get_object_or_404(dropDown, key = 'Doc'):
            appointment = get_object_or_404(Appointments, id=14)
            pdf_file = BytesIO()
            context = {
                "doctor_name": appointment.doctor.user.get_full_name(),
                'specialization' : appointment.doctor.specialization.name,
                "patient_name": appointment.patient.user.get_full_name(),
                "gender": appointment.patient.user.gender.name,
                "weight": appointment.patient.weight,
                "phone": appointment.patient.user.phone_no,
                "diagnosis": appointment.reason_to_vist,
                "date": appointment.appointment_date,
            }
            html_string = render_to_string("prescription.html", context,request)
            HTML(string=html_string).write_pdf(target = pdf_file)
            pdf_file.seek(0)
            return FileResponse(pdf_file, as_attachment=True,filename='prescription.pdf' )
        else:return JsonResponse({'error' : 'Please login with doctor credentials'}, status = 403)
    else:return JsonResponse({'error' : 'Method not allowed'}, status = 405)



