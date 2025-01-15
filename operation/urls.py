from django.urls import path
from . import views

app_name = 'operation'

urlpatterns = [
    path('signup/datos/', views.datos, name='signup'),
    path("signup/domicilio/<int:id_datos>/", views.domicilio, name="domicilio"),
    path("misdatos/<int:id_datos>/", views.mostrar_datos, name='misdatos'),
    path("login/", views.iniciar_sesion, name="login"),
]
