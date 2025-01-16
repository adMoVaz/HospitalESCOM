from datetime import date
from django.db import models
from archives.models import Especialidad, Datos, Direccion


# Create your models here.

class TipoUsuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, verbose_name="ID del usuario")
    rol = models.CharField(max_length=20, verbose_name="Rol")
    rol_descripcion = models.CharField(max_length=140, verbose_name="Descripción del rol")

    def __str__(self):
        return self.rol

    class Meta:
        verbose_name = "Tipo de usuario"
        verbose_name_plural = "Tipos de usuarios"


class Paciente(models.Model):
    id_datos = models.ForeignKey(Datos, on_delete=models.CASCADE, verbose_name="Datos del paciente")
    id_paciente = models.AutoField(primary_key=True, verbose_name="ID del paciente")
    id_usuario = models.ForeignKey(
        TipoUsuario,
        on_delete=models.PROTECT,
        verbose_name="Tipo de usuario",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id_datos.nombre} {self.id_datos.apellido_paterno} {self.id_datos.apellido_materno}"


class Trabajador(models.Model):
    id_datos = models.ForeignKey(Datos, on_delete=models.CASCADE, verbose_name="Datos del trabajador")
    dni_trabajador = models.CharField(max_length=20, primary_key=True, verbose_name="DNI del trabajador")
    id_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, verbose_name="Tipo de usuario")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")

    def __str__(self):
        return f"{self.dni_trabajador} - {self.id_datos.nombre} {self.id_datos.apellido_paterno}"

    @property
    def dias_servicio(self):
        if self.fecha_inicio:
            return (date.today() - self.fecha_inicio).days
        return 0

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"


class Doctor(models.Model):
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula profesional")
    dni_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador relacionado")
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, verbose_name="Especialidad")
    estado = models.BooleanField(default=False, verbose_name="Disponible", blank=True)

    def __str__(self):
        return f"{self.dni_trabajador.id_datos.nombre} {self.dni_trabajador.id_datos.apellido_paterno} - {self.id_especialidad.nombre}"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"


class Recepcionista(models.Model):
    dni_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, verbose_name="DNI del trabajador")

    def __str__(self):
        return f"{self.dni_trabajador}"

    class Meta:
        verbose_name = "Recepcionista"
        verbose_name_plural = "Recepcionistas"
