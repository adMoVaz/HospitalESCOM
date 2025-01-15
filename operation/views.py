from django.shortcuts import render, redirect, get_object_or_404
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


def perfil(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('operation:login')  # Redirigir al login si no hay sesión

    data = Datos.objects.get(id_datos=usuario_id)
    return render(request, 'archives/mostrardatos.html', {'datos': data})


def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            usuario = Datos.objects.get(email=email)
            if usuario.password == password:
                request.session['usuario_id'] = usuario.id_datos
                return redirect('operation:perfil')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Datos.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'operation/login.html')


def cerrar_sesion(request):
    request.session.flush()  # Eliminar toda la sesión
    return redirect('operation:login')
