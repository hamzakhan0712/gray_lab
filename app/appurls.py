from django.urls import path
from .views import (
    DepartmentListCreate,
    DepartmentDetail,
    department_doctors,
    department_patients,
    PatientRecordListCreate,
    patient_record_detail,
    UserListCreate,
    UserDetail,
    register,
    login,
    logout,
    DoctorListCreate,
    DoctorDetail,
    PatientListCreate,
    PatientDetail
)

urlpatterns = [
    # Department URLs
    path('departments/', DepartmentListCreate.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('departments/<int:pk>/doctors/', department_doctors, name='department-doctors'),
    path('departments/<int:pk>/patients/', department_patients, name='department-patients'),

    # Patient Record URLs
    path('patient_records/', PatientRecordListCreate.as_view(), name='patient-record-list-create'),
    path('patient_records/<int:pk>/', patient_record_detail, name='patient-record-detail'),

    # User URLs
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    # Doctor URLs
    path('doctors/', DoctorListCreate.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),

    # Patient URLs
    path('patients/', PatientListCreate.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetail.as_view(), name='patient-detail'),
]
