from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.conf import settings


class basemodel(models.Model):
    class Status(models.IntegerChoices):
        created = 0, 'Created'
        updated = 1, 'Updated'
        deleted = 2, 'Deleted'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_status  = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.created)

    class Meta:
        abstract = True
    
class dropDown(models.Model):
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING, related_name='child',null=True)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=10, unique=True)

class customUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"),unique=True)
    birth_date = models.DateField(null=True, blank=False)
    address = models.CharField(max_length=150)
    phone_no = models.BigIntegerField(null=True, blank=False, validators=[MaxValueValidator(10)])
    gender = models.ForeignKey(dropDown, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profile_photo')
    role = models.ForeignKey(dropDown, on_delete=models.DO_NOTHING, related_name='roles', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class patient(basemodel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    height = models.FloatField()
    weight = models.FloatField()
    blood_group = models.ForeignKey(dropDown, on_delete=models.CASCADE)
    medical_history = models.TextField(max_length=200)

class doctor(basemodel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_user')
    specialization = models.ForeignKey(dropDown, on_delete=models.CASCADE , related_name='specialization')
    qualifications = models.ForeignKey(dropDown, on_delete=models.CASCADE, related_name='qualifications')
    experience = models.FloatField()

