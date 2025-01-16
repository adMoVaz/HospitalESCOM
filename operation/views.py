from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import *
from archives.models import *


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


def perfil_paciente(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('operation:login/paciente')
    data = Datos.objects.get(id_datos=usuario_id)
    try:
        direccion = Direccion.objects.get(id_datos=usuario_id)
    except Direccion.DoesNotExist:
        direccion = None
    return render(request, 'archives/perfil_paciente.html', {'datos': data, 'direccion': direccion})


def inicio_sesion_selector(request):
    return render(request, 'operation/login_main.html')


def iniciar_sesion_paciente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            usuario = Datos.objects.get(email=email)
            if usuario.password == password:
                request.session['usuario_id'] = usuario.id_datos
                return redirect('operation:perfil/paciente')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Datos.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'operation/login_paciente.html')


def iniciar_sesion_doctor(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        password = request.POST.get('password')
        try:
            doctor = Doctor.objects.get(cedula=cedula)
            usuario = doctor.dni_trabajador.id_datos
            if usuario.password == password:
                request.session['doctor_id'] = doctor.id
                request.session['doctor_nombre'] = f"{usuario.nombre} {usuario.apellido_paterno}"
                return redirect('operation:perfil/doctor')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor con esta cédula no encontrado')
    return render(request, 'operation/login_doctor.html')


def perfil_doctor(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        messages.error(request, 'Debes iniciar sesión primero')
        return redirect('operation:login/doctor')
    doctor = Doctor.objects.get(id=doctor_id)
    datos = doctor.dni_trabajador.id_datos
    try:
        direccion = Direccion.objects.get(id_datos=datos.id_datos)
    except Direccion.DoesNotExist:
        direccion = None
    return render(request, 'archives/perfil_doctor.html', {'doctor': doctor, 'datos': datos, 'direccion': direccion})


def cerrar_sesion(request):
    request.session.flush()
    return redirect('operation:login/select')


def perfil_selector(request):
    try:
        if 'usuario_id' in request.session:
            return redirect('operation:perfil/paciente')

        elif 'doctor_id' in request.session:
            return redirect('operation:perfil/doctor')

    except Exception as e:
        messages.error(request, 'Ocurrió un error. Por favor, inicia sesión nuevamente.')
        return redirect('operation:login/select')

    messages.error(request, 'Debes iniciar sesión primero')
    return redirect('operation:login/select')
