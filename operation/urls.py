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
    path("citas/agendar", views.agendar_cita, name='citas/agendar'),
    path("citas/consultar/paciente", views.consultar_citas_paciente, name='citas/consultar/paciente'),
    path("citas/consultar/doctor", views.consultar_citas_doctor, name="citas/consultar/doctor"),
    path("citas/consultar/paciente/eliminar/<int:cita_id>/", views.eliminar_cita, name='citas/consultar/paciente/eliminar'),
    path("citas/modificar/<int:cita_id>/", views.modificar_cita, name="citas/modificar"),
    path("perfil/paciente/modificar", views.modificar_datos_paciente, name="perfil/paciente/modificar"),
    path("citas/atender/<int:cita_id>/", views.atender_cita, name="citas/atender"),
    path('recetas/crear/', views.crear_receta, name='recetas_crear'),
    path('recetas/listar/', views.listar_recetas, name='recetas_listar'),
]
