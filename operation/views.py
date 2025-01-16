from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import *
from archives.models import *
from operation.models import *


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

    return redirect('operation:login/select')


def agendar_cita(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('operation:login/paciente')

    if request.method == 'POST':
        try:
            especialidad_id = request.POST.get('especialidad')
            doctor_id = request.POST.get('doctor')
            consultorio_id = request.POST.get('consultorio')
            fecha = request.POST.get('fecha')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fin = request.POST.get('hora_fin')
            print(f"Especialidad: {especialidad_id}, Doctor: {doctor_id}, Consultorio: {consultorio_id}")
            print(f"Fecha: {fecha}, Hora Inicio: {hora_inicio}, Hora Fin: {hora_fin}")
            doctor = Doctor.objects.get(id=doctor_id)
            consultorio = Consultorio.objects.get(id_consultorio=consultorio_id)
            paciente = Paciente.objects.get(id_datos=usuario_id)

            cita = Citas(
                id_doctor=doctor,
                id_paciente=paciente,
                id_consultorio=consultorio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estatus=False
            )
            cita.save()

            return redirect('operation:perfil/paciente')
        except Doctor.DoesNotExist:
            messages.error(request, "El doctor seleccionado no existe")
        except Consultorio.DoesNotExist:
            messages.error(request, "El consultorio seleccionado no existe")
        except Paciente.DoesNotExist:
            messages.error(request, "El paciente no se encontró")
        except Exception as e:
            print(f"Error al agendar cita: {e}")

    especialidades = Especialidad.objects.all()
    doctores = Doctor.objects.all()
    consultorios = Consultorio.objects.all()

    return render(request, 'operation/agendar_cita.html', {
        'especialidades': especialidades,
        'doctores': doctores,
        'consultorios': consultorios
    })


def consultar_citas_paciente(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para consultar tus citas")
        return redirect('operation:login/paciente')

    try:
        paciente = Paciente.objects.get(id_datos=usuario_id)
        citas = Citas.objects.filter(id_paciente=paciente).select_related(
            'id_doctor', 'id_doctor__id_especialidad', 'id_consultorio'
        ).order_by('fecha', 'hora_inicio')

    except Paciente.DoesNotExist:
        messages.error(request, "No se encontró el paciente.")
        return redirect('operation:login/paciente')

    return render(request, 'operation/consultar_citas_paciente.html', {'citas': citas})


def eliminar_cita(request, cita_id):
    try:
        cita = get_object_or_404(Citas, id_cita=cita_id, id_paciente__id_datos=request.session.get('usuario_id'))
        cita.delete()
        messages.success(request, "La cita ha sido eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al intentar eliminar la cita: {str(e)}")
    return redirect('operation:citas/consultar/paciente')


def modificar_datos_paciente(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para modificar tus datos.")
        return redirect('operation:login/paciente')

    datos = get_object_or_404(Datos, id_datos=usuario_id)
    try:
        direccion = Direccion.objects.get(id_datos=datos)
    except Direccion.DoesNotExist:
        direccion = None

    if request.method == 'POST':
        datos.nombre = request.POST.get('nombre', datos.nombre)
        datos.apellido_paterno = request.POST.get('apellido_paterno', datos.apellido_paterno)
        datos.apellido_materno = request.POST.get('apellido_materno', datos.apellido_materno)
        datos.fecha_nacimiento = request.POST.get('fecha_nacimiento', datos.fecha_nacimiento)
        datos.curp = request.POST.get('curp', datos.curp)
        datos.telefono_movil = request.POST.get('telefono_movil', datos.telefono_movil)
        datos.telefono_fijo = request.POST.get('telefono_fijo', datos.telefono_fijo)
        datos.email = request.POST.get('email', datos.email)

        if direccion:
            direccion.calle = request.POST.get('calle', direccion.calle)
            direccion.numero_exterior = request.POST.get('numero_exterior', direccion.numero_exterior)
            direccion.numero_interior = request.POST.get('numero_interior', direccion.numero_interior)
            direccion.colonia = request.POST.get('colonia', direccion.colonia)
            direccion.codigo_postal = request.POST.get('codigo_postal', direccion.codigo_postal)
            direccion.municipio = request.POST.get('municipio', direccion.municipio)
            direccion.entidad_federativa = request.POST.get('entidad_federativa', direccion.entidad_federativa)
            direccion.pais = request.POST.get('pais', direccion.pais)

        datos.save()
        if direccion:
            direccion.save()

        messages.success(request, "Tus datos han sido actualizados correctamente.")
        return redirect('operation:perfil/paciente')

    return render(request, 'operation/modificar_perfil_paciente.html', {'datos': datos, 'direccion': direccion})


def modificar_cita(request, cita_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para modificar una cita")
        return redirect('operation:login/paciente')

    # Obtener la cita existente
    cita = get_object_or_404(Citas, id_cita=cita_id, id_paciente__id_datos=usuario_id)

    if request.method == 'POST':
        try:
            especialidad_id = request.POST.get('especialidad')
            doctor_id = request.POST.get('doctor')
            consultorio_id = request.POST.get('consultorio')
            fecha = request.POST.get('fecha')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fin = request.POST.get('hora_fin')

            if hora_inicio >= hora_fin:
                messages.error(request, "La hora de inicio debe ser anterior a la hora de fin.")
                return render(request, 'operation/modificar_cita_paciente.html', {
                    'cita': cita,
                    'especialidades': Especialidad.objects.all(),
                    'doctores': Doctor.objects.all(),
                    'consultorios': Consultorio.objects.all()
                })

            cita.id_doctor = Doctor.objects.get(id=doctor_id)
            cita.id_consultorio = Consultorio.objects.get(id_consultorio=consultorio_id)
            cita.fecha = fecha
            cita.hora_inicio = hora_inicio
            cita.hora_fin = hora_fin
            cita.save()

            messages.success(request, "Cita modificada exitosamente.")
            return redirect('operation:perfil/paciente')
        except Doctor.DoesNotExist:
            messages.error(request, "El doctor seleccionado no existe.")
        except Consultorio.DoesNotExist:
            messages.error(request, "El consultorio seleccionado no existe.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al intentar modificar la cita: {e}")

    especialidades = Especialidad.objects.all()
    doctores = Doctor.objects.all()
    consultorios = Consultorio.objects.all()

    return render(request, 'operation/modificar_cita_paciente.html', {
        'cita': cita,
        'especialidades': especialidades,
        'doctores': doctores,
        'consultorios': consultorios
    })
