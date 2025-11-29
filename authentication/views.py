from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from .functions import check_regex
from .constants import mail_regex,pass_regex
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F,Q
import json

max_image = 1
min_value = 1
contentType = ['image/png','image/jpeg','image/jpg', 'image/webp']
receptionist_role_id = 27
doctor_role_id = 26
patient_role_id = 25

def signUp(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'error' : 'Please send a valid json data'}, status = 400)
        data = request.POST
        user_type = request.GET.get('role')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_no = data.get('phone_no')
        gender = data.get('gender')
        dob = data.get('dob')
        address = data.get('address')
        profile_photo = request.FILES.get('photo')
        password = data.get('password')
        conf_password = data.get('confirm_password')
        if not email or (check_regex(mail_regex, data.get('email')) is None ):
            return JsonResponse({"error" : "Email is required in a valid format"}, status = 400)
        if not password  or ((check_regex(pass_regex, data.get('password')) is None)):
            return JsonResponse({"error" : "Password is required in a valid format"}, status = 400)
        if not conf_password or (data.get('password') != data.get('confirm_password')):
            return JsonResponse({ "error" : "Confirm password should be same as password or confirm password field is missing"}, status = 400)
        if not profile_photo:
            return JsonResponse({'error' : 'Profile photo is required'}, status =400)
        if profile_photo.content_type not in contentType:
            return JsonResponse({'error': 'Invalid image format'}, status=400)
        user, created= customUser.objects.get_or_create(email = email)
        if not created:
            return JsonResponse({'error' : 'User already exists'}, status = 400)
        user.set_password(password)
        user.first_name = first_name
        if last_name: user.last_name = last_name
        user.birth_date = dob
        user.address = address
        user.phone_no = phone_no
        user.gender = dropDown.objects.get(id = gender)
    
        user.profile_photo = profile_photo
        if user_type == 'patient':
            user.role = get_object_or_404(dropDown, id = patient_role_id)
            if int(data.get('height')) < min_value or int(data.get('weight')) < min_value:
                return JsonResponse({'error' : 'Height or weight should be a positive value'}, status = 400)  
            height = data.get('height')
            weight = data.get('weight')
            blood_group = data.get('blood_group')
            medical_history = data.get('medical_history')
            user.save()
            patient_data = patient.objects.create(
                user= user, 
                height = height, 
                weight = weight,
                blood_group = get_object_or_404(dropDown,id = blood_group)
            )
            if medical_history:
                patient_data.medical_history = medical_history
            patient_data.save()

            data = render_to_string('patient_reg.html',{'first_name' : first_name})
            send_mail(
                subject='Registered Successfully',from_email= settings.EMAIL_HOST_USER, recipient_list= [email],
                html_message=data,message='Hello'
            )
            return JsonResponse({'msg' : 'Patient registered successfully'}, status = 201)
        elif user_type == 'doctor':
            user.role = get_object_or_404(dropDown ,id = doctor_role_id)
            specialization = data.get('specialization')
            qualification= data.get('qualification')
            experience = data.get('experience')
            user.save()

            doctor.objects.create(
                user = user, 
                specialization = get_object_or_404(dropDown ,id = specialization), 
                qualifications = get_object_or_404(dropDown,id = qualification), 
                experience = experience 
            )
            data = render_to_string('doctor_reg.html',{'first_name' : first_name})
            send_mail(
                subject='Registered Successfully',from_email= settings.EMAIL_HOST_USER, recipient_list= [email],
                html_message=data,message='Hello'
            )
            return JsonResponse({'msg' : 'Doctor registered successfully'}, status = 201)
        else:return JsonResponse({'error' : 'Invalid user type'}, status = 400)
    else:return JsonResponse({'error' : 'Invalid Method'}, status = 405)

def signIn(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({"error" : "Please Use the proper json format to send the data"}, status = 400)
        data = json.loads(request.body)
        if ('email' not in (data.keys()) or 'password' not in (data.keys())):
            return JsonResponse({"error" : "Please give me all the required fields"}, status = 400)
        user = authenticate(request, email = data.get('email') , password = data.get('password'))
        if user is not None: 
            login(request,user)   
            role = request.user.role.name
            return JsonResponse({"msg":"Logged In Successfully", 'role' : role}, status = 200)
        else:return JsonResponse({"error":"Wrong Credentials"}, status = 401)
    else:return JsonResponse({"error":"Invalid Method"} ,status = 405) 

def signOut(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'msg' : 'Logged out successfully'}, status =400)
        else:return JsonResponse({'error' : 'No Active User'}, status = 400)
    else:return JsonResponse({'error' : 'Invalid Method'}, status = 405)

def dropDowns(request):
    if request.method == 'GET':
        data = dropDown.objects.all()
        gender = data.filter(parent = 1).values('name' , 'key','id')
        blood_group = data.filter(parent = 5).values('name', 'key', 'id')
        specialization = data.filter(parent = 14).values('name', 'key', 'id')
        qualifications = data.filter(parent = 20).values('name', 'key', 'id')
        roles = data.filter(parent = 24).values('name', 'key', 'id')
        return JsonResponse({
            'genders' :list(gender), 
            'blood_groups' : list(blood_group), 
            'specializations' : list(specialization),
            'qualifications' : list(qualifications),
            'roles' : list(roles)
        }, safe=False, status = 200)
    else:return JsonResponse({'error' : 'Invalid Method'}, status = 405)

def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated: 
            if request.user.role.id == patient_role_id:
                # userdata = patient.objects.values(status = F('current_status'))
                # print(userdata)
                user = patient.objects.select_related('user').filter(user = request.user)[0]
                data = {
                    'first_name' : user.user.first_name,
                    'last_name' : user.user.last_name,
                    'birth_date': user.user.birth_date,
                    'email' : user.user.email,
                    'gender' : user.user.gender.name,
                    'phone_no': user.user.phone_no,
                    'address' : user.user.address,
                    'profile_photo' : user.user.profile_photo.url,
                    'height' : user.height,
                    'weight' : user.weight,
                    'blood_group' : user.blood_group.name,
                    'medical_history' : user.medical_history,
                    'role' : request.user.role.name
                }
            elif request.user.role.id == doctor_role_id:
                # userdata = patient.objects.values(status = F('current_status'))
                # print(userdata)
                # userdata = doctor.objects.annotate(status = basemodel.Status(F('current_status')).label).values()
                # print(userdata)
                user = doctor.objects.select_related('user').filter(user = request.user)[0]
                data = {
                    'first_name' : user.user.first_name,
                    'last_name' : user.user.last_name,
                    'birth_date': user.user.birth_date,
                    'email' : user.user.email,
                    'phone_no': user.user.phone_no,
                    'gender' : user.user.gender.name,
                    'address' : user.user.address,
                    'profile_photo' : user.user.profile_photo.url,
                    'specialization' : user.specialization.name,
                    'qualifications' : user.qualifications.name,
                    'experience' : user.experience,
                    'role' : request.user.role.name
                }
            elif request.user.role.id == receptionist_role_id:
                user = doctor.objects.select_related('user').filter(user = request.user)[0]
                data = {
                    'first_name' : user.user.first_name,
                    'last_name' : user.user.last_name,
                    'birth_date': user.user.birth_date,
                    'email' : user.user.email,
                    'phone_no': user.user.phone_no,
                    'gender' : user.user.gender.name,
                    'address' : user.user.address,
                    'profile_photo' : user.user.profile_photo.url,
                    'role' : request.user.role.name
                }
            else:return JsonResponse({'error':"User with invalid role"}, status = 401)
            return JsonResponse(data, status = 200)
        else:return JsonResponse({"error" : "Please Log In "},status = 401)
    else:return JsonResponse({'error' : 'Invalid Method'}, status = 405)