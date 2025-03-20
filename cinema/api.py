from ninja import NinjaAPI, Schema
from sales.models import *
from typing import List
from datetime import date

api = NinjaAPI()

class PeliculaOut(Schema):
    titol : str
    durada : int
    descripcio : str
    genere : str
    data_estrena: date 

class PeliculaIn(Schema):
    titol = str
    durada = int
    descripcio = str
    genere = str
    data_estrena = date

@api.get("/pelis", response=List[PeliculaOut])
def pelicules(request):
    pelicules = Pelicula.objects.all()
    return pelicules

@api.post("/peli")
def create_employee(request, payload: PeliculaIn):
    peli = Pelicula.objects.create(**payload.dict())
    return {"id": peli.id}
