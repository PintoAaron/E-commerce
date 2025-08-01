from django.core.management.base import BaseCommand
from shop.models import Collection


class Command(BaseCommand):
    help = 'Create default collections for the shop'

    def handle(self, *args, **options):
        collections_data = [
            {
                'title': 'Electronics',
                'icon': 'laptop',
                'color': '#3498db',
                'background_color': '#ecf0f1'
            },
            {
                'title': 'Clothing',
                'icon': 'tshirt-crew',
                'color': '#e74c3c',
                'background_color': '#fadbd8'
            },
            {
                'title': 'Books',
                'icon': 'book-open-page-variant',
                'color': '#2ecc71',
                'background_color': '#d5f4e6'
            },
            {
                'title': 'Home & Garden',
                'icon': 'home-variant',
                'color': '#f39c12',
                'background_color': '#fef9e7'
            },
            {
                'title': 'Sports & Outdoors',
                'icon': 'soccer',
                'color': '#9b59b6',
                'background_color': '#f4ecf7'
            },
            {
                'title': 'Beauty & Health',
                'icon': 'heart-pulse',
                'color': '#e91e63',
                'background_color': '#fce4ec'
            },
            {
                'title': 'Toys & Games',
                'icon': 'toy-brick',
                'color': '#ff9800',
                'background_color': '#fff3e0'
            },
            {
                'title': 'Automotive',
                'icon': 'car',
                'color': '#607d8b',
                'background_color': '#eceff1'
            },
            {
                'title': 'Food & Beverages',
                'icon': 'food-apple',
                'color': '#4caf50',
                'background_color': '#e8f5e8'
            },
            {
                'title': 'Jewelry & Accessories',
                'icon': 'diamond-stone',
                'color': '#673ab7',
                'background_color': '#f3e5f5'
            }
        ]

        created_count = 0
        
        for collection_data in collections_data:
            collection, created = Collection.objects.get_or_create(
                title=collection_data['title'],
                defaults={
                    'icon': collection_data['icon'],
                    'color': collection_data['color'],
                    'background_color': collection_data['background_color']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created collection: {collection.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Collection already exists: {collection.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nCommand completed! Created {created_count} new collections.')
        )