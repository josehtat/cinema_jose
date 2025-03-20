from django.core.management.base import BaseCommand
from faker import Faker
from sales.models import Sala
    
class Command(BaseCommand):
    help = 'Crea una sala amb un nom únic i capacitat aleatòria'

    def add_arguments(self, parser):
        # No cal arguments per aquest seeder, però podem afegir algun paràmetre si volem
        parser.add_argument('--intents', type=int, default=5, help='Nombre màxim d\'intents per generar un nom únic')

    def handle(self, *args, **options):
        fake = Faker(["es_CA", "es_ES"])  # Faker en català i espanyol

        def generar_nom_sala(intentos=options['intents']):
            """Genera un nom de sala únic fins a un màxim de intents"""
            for _ in range(intentos):
                nom = fake.word().capitalize() + " " + fake.word().capitalize()
                if not Sala.objects.filter(nom=nom).exists():
                    return nom
            return None  # Si no troba un nom únic després de 5 intents, retorna None

        def crear_sala():
            """Crea una sala amb un nom únic i una capacitat aleatòria."""
            nom_sala = generar_nom_sala()
            if nom_sala is None:
                self.stdout.write(self.style.ERROR("❌ No s'ha pogut generar un nom de sala únic després de 5 intents."))
                return

            # Crear la sala amb Faker
            sala = Sala.objects.create(
                nom=nom_sala,
                capacitat=fake.random_int(min=50, max=200)  # Capacitat entre 50 i 200
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Sala creada: {sala.nom} - Capacitat: {sala.capacitat}"))

        # Executar la creació de la sala
        self.stdout.write("🌱 Omplint la base de dades amb dades falses...")
        crear_sala()
        self.stdout.write(self.style.SUCCESS("✅ Dades generades correctament!"))