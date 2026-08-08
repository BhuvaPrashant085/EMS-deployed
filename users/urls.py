from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    
    path('login/', views.login_user, name='login'),
     path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('operator/', views.operator_dashboard, name='operator_dashboard'),
    path('send_emergency/', views.send_emergency, name='send_emergency'),
    path('profile/', views.profile, name='profile'),
    path('approve_emergency/<int:emergency_id>/', views.approve_emergency, name='approve_emergency'),
    path("hospital-dashboard/", views.hospital_dashboard, name="hospital_dashboard"),
path("police-dashboard/", views.police_dashboard, name="police_dashboard"),
path("fire-dashboard/", views.fire_dashboard, name="fire_dashboard"),
path(
"accept-emergency/<int:emergency_id>/<str:service_type>/",
views.accept_emergency,
name="accept_emergency"
),
path("resolve-emergency/<int:emergency_id>/", views.resolve_emergency, name="resolve_emergency"),
path("emergency-live/", views.emergency_live_data, name="emergency_live"),
 path('trusted-dashboard/', views.trusted_dashboard, name='trusted_dashboard'),
 path('all-emergencies/', views.all_emergencies_dashboard, name='all_emergencies_dashboard'),





]
