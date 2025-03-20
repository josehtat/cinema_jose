from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Butaca)
admin.site.register(Sessio)
admin.site.register(Entrada)