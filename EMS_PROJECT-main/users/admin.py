from django.contrib import admin
from .models import *

admin.site.register(Citizen)
admin.site.register(Emergency)

admin.site.register(Ambulance)
admin.site.register(Hospital)
admin.site.register(PoliceStation)

admin.site.register(FireStation)
admin.site.register(EmergencyLog)
admin.site.register(EmergencyAssignment)

admin.site.register(TrustedContact)
