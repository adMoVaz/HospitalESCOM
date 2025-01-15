from django.contrib.auth.backends import BaseBackend
from archives.models import Datos


class DatosAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Datos.objects.get(email=username)
            print(f"Usuario encontrado: {usuario.email}")
            if usuario.password == password:
                print("Contraseña correcta")
                return usuario
            else:
                print("Contraseña incorrecta")
        except Datos.DoesNotExist:
            print("Usuario no encontrado")
            return None

    def get_user(self, user_id):
        try:
            return Datos.objects.get(pk=user_id)
        except Datos.DoesNotExist:
            return None
