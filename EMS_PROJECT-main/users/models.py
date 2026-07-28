from django.db import models

# -------------------------------
# Citizen Table
# -------------------------------
from django.db import models
from django.shortcuts import render

class TrustedContact(models.Model):
    citizen = models.ForeignKey('Citizen', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    relation = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
    

class Citizen(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Trusted contacts (both email & phone)
    trusted_contact1_email = models.EmailField(blank=True)
    trusted_contact1_phone = models.CharField(max_length=15, blank=True)
    trusted_contact2_email = models.EmailField(blank=True)
    trusted_contact2_phone = models.CharField(max_length=15, blank=True)

    blood_group = models.CharField(max_length=10, blank=True)
    medical_issue = models.TextField(blank=True)

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# -------------------------------
# Emergency Table
# -------------------------------
class Emergency(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)

    EMERGENCY_TYPES = [
        ('medical', 'Medical Emergency'),
        ('accident', 'Road Accident'),
        ('fire', 'Fire Emergency'),
        ('crime', 'Crime Emergency'),
        ('disaster', 'Natural Disaster'),
    ]
    emergency_type = models.CharField(max_length=50, choices=EMERGENCY_TYPES)

    STATUS_TYPES = [
    ('Pending','Pending'),
    ('Approved','Approved'),
    ('Help On The Way','Help On The Way'),
    ('Resolved','Resolved'),
]

    status = models.CharField(max_length=50, choices=STATUS_TYPES, default="Pending")

    latitude = models.FloatField()
    longitude = models.FloatField()

    status = models.CharField(max_length=50, default="Pending")  # Pending, Approved, Completed
    priority = models.CharField(max_length=50)

    approved = models.BooleanField(default=False)  # Admin approval
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emergency_type} - {self.citizen.name}"


# -------------------------------
# Ambulance Table
# -------------------------------
class Ambulance(models.Model):
    driver_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)
    current_location = models.CharField(max_length=200)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_number


# -------------------------------
# Hospital Table
# -------------------------------
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.hospital_name


# -------------------------------
# Police Station Table
# -------------------------------
class PoliceStation(models.Model):
    station_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.station_name


# -------------------------------
# Fire Station Table
# -------------------------------
class FireStation(models.Model):
    station_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.station_name


# -------------------------------
# Emergency Assignment Table
# -------------------------------
class EmergencyAssignment(models.Model):
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE)

    SERVICE_TYPES = [
        ('ambulance', 'Ambulance'),
        ('police', 'Police'),
        ('fire', 'Fire Service'),
        ('hospital', 'Hospital'),
    ]
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    assigned_to = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.service_type


# -------------------------------
# Emergency Status Log
# -------------------------------
class EmergencyLog(models.Model):
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):



        return self.status
    

    # ===============================
# HOSPITAL DASHBOARD
# ===============================
