from django.contrib import admin
from .models import Department, PatientRecord, Doctor, Patient


# Register your models here.
admin.site.register(Department)
admin.site.register(PatientRecord)
admin.site.register(Doctor)
admin.site.register(Patient)
