# views.py

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Department, PatientRecord, Doctor, Patient
from .serializers import DepartmentSerializer, PatientRecordSerializer, UserSerializer,DoctorSerializer, PatientSerializer

# Department Views
class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def department_doctors(request, pk):
    department = Department.objects.get(pk=pk)
    if request.user.groups.filter(name='Doctors').exists():
        doctors = Doctor.objects.filter(department=department)
        serializer = UserSerializer([doc.user for doc in doctors], many=True)
        return Response(serializer.data)
    return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def department_patients(request, pk):
    department = Department.objects.get(pk=pk)
    if request.user.groups.filter(name='Doctors').exists():
        patients = Patient.objects.filter(department=department)
        serializer = UserSerializer([pat.user for pat in patients], many=True)
        return Response(serializer.data)
    return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

# Patient Records Views
class PatientRecordListCreate(generics.ListCreateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Doctors').exists():
            # Doctor can view records in their department
            return PatientRecord.objects.filter(department__in=user.doctor.department_set.all())
        elif user.groups.filter(name='Patients').exists():
            # Patient can view their own records
            return PatientRecord.objects.filter(patient__user=user)
        return PatientRecord.objects.none()

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def patient_record_detail(request, pk):
    try:
        record = PatientRecord.objects.get(pk=pk)
    except PatientRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user.groups.filter(name='Doctors').exists():
        # Doctor can view and modify records in their department
        if record.department not in user.doctor.department_set.all():
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)
    elif user.groups.filter(name='Patients').exists():
        # Patient can only access their own records
        if record.patient.user != user:
            return Response({"error": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = PatientRecordSerializer(record)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PatientRecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# User Views
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]




# View to list and create doctors
class DoctorListCreate(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

# View to get, update, or delete a particular doctor
class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]



# View to list and create patients
class PatientListCreate(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

# View to get, update, or delete a particular patient
class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]



@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token or user already logged out."}, status=status.HTTP_400_BAD_REQUEST)
