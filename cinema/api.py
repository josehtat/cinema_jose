from ninja import NinjaAPI, Schema
from sales.models import *
from typing import List
from datetime import date

api = NinjaAPI()

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
    butaca : List[ButacaOut]



@api.get("/pelis", response=List[PeliculaOut])
def pelicules(request):
    pelicules = Pelicula.objects.all()
    return pelicules

@api.get("/salas", response=List[SalaOut])
def salas(request):
    salas = Sala.objects.all()
    return salas

@api.post("/peli")
def create_employee(request, payload: PeliculaIn):
    peli = Pelicula.objects.create(**payload.dict())
    return {"id": peli.id}
