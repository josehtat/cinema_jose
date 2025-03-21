from ninja import NinjaAPI, Schema
from sales.models import *
from typing import List
from datetime import date
from ninja.security import HttpBasicAuth, HttpBearer
from django.contrib.auth import authenticate as djangoauth
import secrets


api = NinjaAPI()

class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = djangoauth(username=username, password=password)
        if user:
            # Genera un token simple
            token = secrets.token_hex(16)
            user.auth_token = token
            user.save()
            return token
        return None
    
# Autenticació per Token Bearer
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = Usuari.objects.get(auth_token=token)
            return user
        except Usuari.DoesNotExist:
            return None

class PeliculaOut(Schema):
    titol : str
    descripcio : str
    data_estrena: date 

class PeliculaIn(Schema):
    titol = str
    durada = int
    descripcio = str
    genere = str
    data_estrena = date

class ButacaOut(Schema):
    fila : int
    numero : int
    tipus : str

class SalaOut(Schema):
    nom : str
    capacitat : int
    butaca_set : List[ButacaOut]



@api.get("/pelis", response=List[PeliculaOut])
def pelicules(request):
    pelicules = Pelicula.objects.all()
    return pelicules

@api.get("/salas", response=List[SalaOut], auth=AuthBearer())
def salas(request):
    salas = Sala.objects.all()
    return salas

@api.post("/peli")
def create_employee(request, payload: PeliculaIn):
    peli = Pelicula.objects.create(**payload.dict())
    return {"id": peli.id}
