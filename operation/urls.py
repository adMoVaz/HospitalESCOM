from django.urls import path
from . import views

app_name = 'operation'

urlpatterns = [
    path('signup/datos/', views.datos, name='signup'),
    path("signup/domicilio/", views.domicilio, name="domicilio"),
    path("login/select", views.inicio_sesion_selector, name='login/select'),
    path("login/paciente", views.iniciar_sesion_paciente, name="login/paciente"),
    path("perfil/select", views.perfil_selector, name='perfil/select'),
    path("perfil/paciente", views.perfil_paciente, name="perfil/paciente"),
    path("login/doctor", views.iniciar_sesion_doctor, name="login/doctor"),
    path("perfil/doctor", views.perfil_doctor, name="perfil/doctor"),
    path("logout/", views.cerrar_sesion, name="logout"),
]
