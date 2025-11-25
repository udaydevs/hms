from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import F,Q
import json

def appointments(request):
    pass
