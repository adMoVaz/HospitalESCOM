from django.db import models
from datetime import date


# Create your models here.
class Datos(models.Model):
    id_datos = models.AutoField(primary_key=True, verbose_name="ID de datos")
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=20, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=20, verbose_name="Apellido materno")
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    telefono_movil = models.IntegerField(verbose_name="Teléfono móvil")
    telefono_fijo = models.IntegerField(verbose_name="Teléfono fijo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    password = models.CharField(max_length=20, verbose_name="Contraseña", null=True, blank=True)
    fecha_registro = models.DateField(verbose_name="Fecha de registro", null=True, blank=True, default=date.today)
    last_login = models.DateTimeField(verbose_name="Último inicio de sesión", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    class Meta:
        verbose_name = "Información de usuario"
        verbose_name_plural = "Información de usuarios"


class Direccion(models.Model):
    id_domicilio = models.AutoField(primary_key=True, verbose_name="ID del domicilio")
    id_datos = models.ForeignKey(
        Datos,
        on_delete=models.CASCADE,
        verbose_name="Datos relacionados",
        null=True,
        blank=True
    )
    calle = models.CharField(max_length=100, verbose_name="Calle")
    numero_exterior = models.IntegerField(verbose_name="Número exterior")
    numero_interior = models.CharField(max_length=10, verbose_name="Número interior")
    colonia = models.CharField(max_length=20, verbose_name="Colonia")
    municipio = models.CharField(max_length=25, verbose_name="Municipio")
    codigo_postal = models.IntegerField(verbose_name="Código postal")
    pais = models.CharField(max_length=15, verbose_name="País")
    entidad_federativa = models.CharField(max_length=20, verbose_name="Entidad federativa")

    def __str__(self):
        return f"{self.calle} - {self.numero_exterior}, {self.colonia}, {self.municipio}"

    class Meta:
        verbose_name = "Domicilio"
        verbose_name_plural = "Domicilios"


class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True, verbose_name="ID de especialidad")
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la especialidad")
    especialidad_descripcion = models.CharField(
        max_length=140,
        verbose_name="Descripción de la especialidad"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"


class Horario(models.Model):
    DIAS_SEMANA = [
        ('mon', 'Lunes'),
        ('tue', 'Martes'),
        ('wed', 'Miércoles'),
        ('thu', 'Jueves'),
        ('fri', 'Viernes'),
        ('sat', 'Sábado'),
        ('sun', 'Domingo'),
    ]

    id_horario = models.AutoField(primary_key=True, verbose_name="ID de horario")
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de término")
    turno = models.CharField(max_length=10, verbose_name="Turno")
    dias_trabaja = models.JSONField(verbose_name="Días que trabaja", default=list, null=True, blank=True)

    def __str__(self):
        return f"{self.id_horario} - {self.turno} - {self.hora_inicio} a {self.hora_fin}"

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"


class Consultorio(models.Model):
    id_consultorio = models.AutoField(primary_key=True, verbose_name="ID de consultorio")
    nombre = models.CharField(max_length=50, verbose_name="Nombre del consultorio", null=True, blank=True)
    id_doctor = models.ForeignKey(
        "users.Doctor",
        on_delete=models.CASCADE,
        verbose_name="Cédula de doctor asignado"
    )

    def __str__(self):
        return f"{self.id_consultorio} - {self.id_doctor}"

    class Meta:
        verbose_name = "Consultorio"
        verbose_name_plural = "Consultorios"
