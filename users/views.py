from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Citizen, Emergency, Ambulance, EmergencyAssignment, EmergencyLog, Hospital, PoliceStation, FireStation, TrustedContact







ADMIN_EMAIL = "prashantbhuva085@gmail.com"


# =======================
# HOME PAGE / DASHBOARD
# =======================


def home(request):
    if 'citizen_id' not in request.session:
        return redirect('login')
    return render(request, 'citizen_dashboard.html')


# =======================
# CITIZEN DASHBOARD
# =======================
def citizen_dashboard(request):
    if 'citizen_id' not in request.session:
        return redirect('login')
    return render(request, "citizen_dashboard.html")

# =======================
# SIGNUP
# =======================
def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        citizen = Citizen.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        citizen.save()
        return redirect('login')
    return render(request, 'signup.html')





def trusted_dashboard(request):
    # Get all trusted contacts' emergencies or just pass all emergencies
    # If you want to show only for all citizens, you can remove the filter
    emergencies = Emergency.objects.all().order_by('-created_at')

    return render(request, "trusted_dashboard.html", {
        "emergencies": emergencies
    })  



# =======================
# LOGIN
# =======================
def login_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        try:
            user = Citizen.objects.get(name=name, phone=phone)
            request.session['citizen_id'] = user.id
            return redirect('home')
        except Citizen.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid Name or Phone'})
    return render(request, 'login.html')

# =======================
# LOGOUT
# =======================
def logout_user(request):
    request.session.flush()
    return redirect('login')

# =======================
# SEND EMERGENCY
  # for SMS API like Twilio or other

def send_emergency(request):
    if 'citizen_id' not in request.session:
        return redirect('login')

    citizen = Citizen.objects.get(id=request.session['citizen_id'])

    if request.method == "POST":
        emergency_type = request.POST.get("emergency_type")
        latitude = request.POST.get("latitude") or 0
        longitude = request.POST.get("longitude") or 0

        emergency = Emergency.objects.create(
            citizen=citizen,
            emergency_type=emergency_type,
            latitude=latitude,
            longitude=longitude,
            priority="High",
            status="Pending",
            approved=False
        )
        emergency.save()

        # Send email and SMS to trusted contacts immediately
        send_trusted_contact_alert(citizen, emergency_type, latitude, longitude)

    return redirect('home')

def send_trusted_contact_alert(citizen, emergency_type, latitude, longitude):
    """
    Send an emergency alert to the citizen's trusted contacts.
    Includes email and optional SMS with live location link and address.
    """
    
    # Email subject and message
    subject = f"Emergency Alert: {emergency_type.capitalize()}"
    location_link = f"https://maps.google.com/?q={latitude},{longitude}"
    
    message = f"""
Hi,

{citizen.name} has triggered an emergency alert.
Emergency Type: {emergency_type.capitalize()}
Location: {location_link}
Address: {citizen.address}

Please reach out immediately.
"""

    # -----------------------------
    # --- SEND EMAIL TO CONTACTS ---
    # -----------------------------
    recipients = []
    if getattr(citizen, "trusted_contact1_email", None):
        recipients.append(citizen.trusted_contact1_email)
    if getattr(citizen, "trusted_contact2_email", None):
        recipients.append(citizen.trusted_contact2_email)
    
    if recipients:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False
        )

    # -----------------------------
    # --- SEND SMS TO CONTACTS ----
    # -----------------------------
    # Example using Twilio
    # Ensure TWILIO_SID, TWILIO_AUTH, TWILIO_NUMBER are in settings.py
    # client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)
    
    for phone_number in [getattr(citizen, "trusted_contact1_phone", None), 
                         getattr(citizen, "trusted_contact2_phone", None)]:
        if phone_number:
            # Uncomment to send SMS
            """
            client.messages.create(
                body=message,
                from_=settings.TWILIO_NUMBER,
                to=phone_number
            )
            """
            # For now, just print to console for testing
            print(f"SMS would be sent to {phone_number}:")
            print(message)

# =======================
# PROFILE PAGE
# =======================
def profile(request):
    if 'citizen_id' not in request.session:
        return redirect('login')

    citizen = Citizen.objects.get(id=request.session['citizen_id'])

    if request.method == "POST":
        citizen.name = request.POST.get("name")
        citizen.phone = request.POST.get("phone")
        citizen.trusted_contact1_email = request.POST.get("trusted1_email")
        citizen.trusted_contact1_phone = request.POST.get("trusted1_phone")
        citizen.trusted_contact2_email = request.POST.get("trusted2_email")
        citizen.trusted_contact2_phone = request.POST.get("trusted2_phone")
        citizen.blood_group = request.POST.get("blood_group")
        citizen.medical_issue = request.POST.get("medical_issue")
        citizen.address = request.POST.get("address")
        citizen.save()
        return redirect('home')

    return render(request, "profile.html", {"citizen": citizen})


# =======================
# ADMIN DASHBOARD
# =======================
def admin_dashboard(request):
    if 'citizen_id' not in request.session:
        return redirect('login')

    user = Citizen.objects.get(id=request.session['citizen_id'])
    if not getattr(user, "is_admin", False):
        return redirect('home')

    pending_emergencies = Emergency.objects.filter(status="Pending", approved=False)
    return render(request, 'admin_dashboard.html', {'emergencies': pending_emergencies})


# =======================
# APPROVE EMERGENCY
# =======================
def approve_emergency(request, emergency_id):
    emergency = Emergency.objects.get(id=emergency_id)
    emergency.approved = True
    emergency.status = "Approved"
    emergency.save()

    # Notify trusted contacts and department
    notify_trusted_contacts(emergency)
    notify_department(emergency)

    return redirect('admin_dashboard')


# =======================
# NOTIFY TRUSTED CONTACTS
# =======================
def notify_trusted_contacts(emergency):
    citizen = emergency.citizen
    subject = f"Emergency Alert: {emergency.get_emergency_type_display()}"
    message = f"""
Hi,

{citizen.name} has triggered an emergency alert.
Emergency Type: {emergency.get_emergency_type_display()}
Location: https://maps.google.com/?q={emergency.latitude},{emergency.longitude}

Please reach out immediately.
"""
    recipients = [citizen.trusted_contact1, citizen.trusted_contact2]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

# =======================
# NOTIFY DEPARTMENT
# =======================
def notify_department(emergency):
    subject = f"Emergency Alert: {emergency.get_emergency_type_display()}"
    message = f"Emergency at location: https://maps.google.com/?q={emergency.latitude},{emergency.longitude}"

    if emergency.emergency_type == "medical":
        recipients = [h.phone for h in Hospital.objects.all()]  # ideally emails
    elif emergency.emergency_type == "fire":
        recipients = [f.phone for f in FireStation.objects.all()]
    elif emergency.emergency_type == "crime":
        recipients = [p.phone for p in PoliceStation.objects.all()]
    else:
        recipients = []

    for r in recipients:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [r])


# =======================
# OPERATOR DASHBOARD (Optional)
# =======================
def operator_dashboard(request):
    return render(request,'operator_dashboard.html')



ADMIN_EMAIL = "prashantbhuva085@gmail.com"
# ===============================
# ACCEPT EMERGENCY WITH ADMIN NOTIFICATION
# ===============================
def accept_emergency(request, emergency_id, service_type):
    emergency = Emergency.objects.get(id=emergency_id)

    EmergencyAssignment.objects.create(
        emergency=emergency,
        service_type=service_type,
        assigned_to="Department Team",
        status="Dispatched"
    )

    emergency.status = "Help On The Way"
    emergency.save()

    EmergencyLog.objects.create(
        emergency=emergency,
        status="Help On The Way"
    )

    # --- Send email to admin ---
    subject = f"Emergency Accepted: {emergency.get_emergency_type_display()}"
    message = f"""
The following emergency has been accepted:

Citizen: {emergency.citizen.name}
Type: {emergency.get_emergency_type_display()}
Status: {emergency.status}
Location: https://maps.google.com/?q={emergency.latitude},{emergency.longitude}
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ADMIN_EMAIL])

    # Redirect to correct dashboard
    if service_type == "hospital":
        return redirect("hospital_dashboard")
    elif service_type == "police":
        return redirect("police_dashboard")
    elif service_type == "fire":
        return redirect("fire_dashboard")

    return redirect("home")

# ===============================
# HOSPITAL DASHBOARD
# ===============================

def hospital_dashboard(request):

    emergencies = Emergency.objects.filter(
        emergency_type__in=['medical','accident'],
        status="Pending"
    ).order_by('-created_at')

    return render(request,"hospital_dashboard.html",{"emergencies":emergencies})


# ===============================
# POLICE DASHBOARD
# ===============================

def police_dashboard(request):
    # Fetch all 'crime' emergencies, no login checks here
    emergencies = Emergency.objects.filter(
        emergency_type='crime'
    ).order_by('-created_at')
    
    return render(request, "police_dashboard.html", {"emergencies": emergencies})

# ===============================
# FIRE DASHBOARD
# ===============================

def fire_dashboard(request):
    emergencies = Emergency.objects.filter(
        emergency_type__in=['fire', 'disaster'],
    ).exclude(status='Resolved').order_by('-created_at')

    return render(request, "fire_dashboard.html", {"emergencies": emergencies})

# ===============================
# RESOLVE EMERGENCY WITH ADMIN NOTIFICATION
# ===============================
def resolve_emergency(request, emergency_id):
    emergency = Emergency.objects.get(id=emergency_id)

    emergency.status = "Resolved"
    emergency.save()

    EmergencyLog.objects.create(
        emergency=emergency,
        status="Resolved"
    )

    # --- Send email to admin ---
    subject = f"Emergency Resolved: {emergency.get_emergency_type_display()}"
    message = f"""
The following emergency has been resolved:

Citizen: {emergency.citizen.name}
Type: {emergency.get_emergency_type_display()}
Status: {emergency.status}
Location: https://maps.google.com/?q={emergency.latitude},{emergency.longitude}
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ADMIN_EMAIL])

    return redirect(request.META.get('HTTP_REFERER'))

from django.http import JsonResponse

def emergency_live_data(request):
    if 'trusted_id' in request.session:
        contact = TrustedContact.objects.get(id=request.session['trusted_id'])
        emergencies = Emergency.objects.filter(citizen=contact.citizen).order_by("-created_at")
    else:
        emergencies = Emergency.objects.all().order_by("-created_at")
    
    data = [{
        "id": e.id,
        "citizen": e.citizen.name,
        "type": e.get_emergency_type_display(),
        "status": e.status,
        "lat": e.latitude,
        "lng": e.longitude
    } for e in emergencies]

    return JsonResponse({"emergencies": data})


def all_emergencies_dashboard(request):
    # Show all emergencies (pending, approved, resolved)
    emergencies = Emergency.objects.all().order_by('-created_at')
    return render(request, "all_emergencies_dashboard.html", {"emergencies": emergencies})
