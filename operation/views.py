from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import *


def datos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        curp = request.POST.get('curp')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono_movil = request.POST.get('telefono_movil')
        telefono_fijo = request.POST.get('telefono_fijo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fecha_registro = request.POST.get('fecha_registro')

        dato = Datos(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            curp=curp,
            fecha_nacimiento=fecha_nacimiento,
            telefono_movil=telefono_movil,
            telefono_fijo=telefono_fijo,
            email=email,
            fecha_registro=fecha_registro,
            password=password
        )
        dato.save()

        return redirect('operation:domicilio', id_datos=dato.id_datos)

    return render(request, 'archives/datos.html')


def domicilio(request, id_datos):
    if request.method == 'POST':
        calle = request.POST.get('calle')
        numero_exterior = request.POST.get('numero_exterior')
        numero_interior = request.POST.get('numero_interior')
        colonia = request.POST.get('colonia')
        municipio = request.POST.get('municipio')
        codigo_postal = request.POST.get('codigo_postal')
        pais = request.POST.get('pais')
        entidad_federativa = request.POST.get('entidad_federativa')

        data = Datos.objects.get(id_datos=id_datos)

        direccion = Direccion(
            id_datos=data,
            calle=calle,
            numero_exterior=numero_exterior,
            numero_interior=numero_interior,
            colonia=colonia,
            municipio=municipio,
            codigo_postal=codigo_postal,
            pais=pais,
            entidad_federativa=entidad_federativa
        )
        direccion.save()

        tipo_usuario = TipoUsuario.objects.get(id_usuario=1)

        paciente = Paciente(
            id_datos=data,
            id_usuario=tipo_usuario
        )
        paciente.save()

        return redirect('core:core')

    return render(request, 'archives/domicilio.html')


def mostrar_datos(request, id_datos):
    dat = get_object_or_404(Datos, id_datos=id_datos)
    return render(request, 'archives/mostrardatos.html', {'datos': dat})


def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user, backend='users.backends.DatosAuthBackend')
            return redirect('core:core')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'operation/login.html')


