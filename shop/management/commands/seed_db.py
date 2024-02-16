from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
            print('Seeding database')
            current_dir = os.path.dirname(__file__)
            file_path  = os.path.join(current_dir, 'seed.sql')
            sql = Path(file_path).read_text()
            
            with connection.cursor() as cursor:
                cursor.execute(sql)
            
            print('Database seeded')
            
        