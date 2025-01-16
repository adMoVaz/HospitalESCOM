from django.db import models

from users.models import Doctor, Paciente
from archives.models import Consultorio


class Citas(models.Model):
    id_cita = models.AutoField(primary_key=True, verbose_name="ID de la cita")
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    id_consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, verbose_name="Consultorio", null=True, blank=True)
    estatus = models.BooleanField(default=False, verbose_name="Estatus de la cita")
    fecha = models.DateField(verbose_name="Fecha de la cita")
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de fin")

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True, verbose_name="ID del pago")
    fecha_pago = models.DateField(verbose_name="Fecha del pago")
    hora_pago = models.TimeField(verbose_name="Hora del pago")
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto del pago")
    estatus_pago = models.BooleanField(default=False, verbose_name="Estatus del pago")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"{self.id_pago} - {self.estatus_pago}"


class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True, verbose_name="ID de la receta")
    id_tratamiento = models.ForeignKey('Tratamiento', on_delete=models.CASCADE, verbose_name="Tratamiento", null=True, blank=True)
    estatus = models.BooleanField(default=False, verbose_name="Estatus de la receta")

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return f"{self.id_receta} - {self.id_tratamiento}"


class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True, verbose_name="ID del diagnóstico")
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE, verbose_name="Receta", null=True, blank=True)
    diagnostico_descripcion = models.CharField(max_length=500, verbose_name="Descripción del diagnóstico")

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"

    def __str__(self):
        return f"{self.id_diagnostico} - {self.id_receta} - {self.id_doctor}"


class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True, verbose_name="ID del medicamento")
    nombre = models.CharField(max_length=30, verbose_name="Nombre del medicamento")
    tipo_medicamento = models.CharField(max_length=20, verbose_name="Tipo de medicamento")
    medicamento_descripcion = models.CharField(max_length=200, verbose_name="Descripción del medicamento")
    precio_medicamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del medicamento")

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nombre


class Tratamiento(models.Model):
    id_tratamiento = models.AutoField(primary_key=True, verbose_name="ID del tratamiento")
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE, verbose_name="Receta", null=True, blank=True)
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name="Medicamento")
    tratamiento_descripcion = models.CharField(max_length=500, verbose_name="Descripción del tratamiento")

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"

    def __str__(self):
        return f"{self.id_tratamiento} - {self.id_receta}"


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True, verbose_name="ID del inventario")
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name="Nombre del medicamento")
    cantidad = models.IntegerField(verbose_name="Cantidad en Inventario")

    def __str__(self):
        return f"Inventario {self.id_inventario}"


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True, verbose_name="Tipo de servicio")
    nombre_servicio = models.CharField(max_length=25, verbose_name="Servicio")
    descripcion = models.TextField(verbose_name="Descripción del Servicio")
    precio_servicio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del servicio")

    def __str__(self):
        return f"{self.nombre_servicio}"


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True, verbose_name="ID de venta")
    id_medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name="ID del medicamento")
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="ID del servicio")
    Fecha_venta = models.DateField(verbose_name="Fecha de la venta")
    hora_venta = models.TimeField(verbose_name="Hora de la venta")

    def __str__(self):
        return f"{self.id_venta} - {self.id_servicio}"
