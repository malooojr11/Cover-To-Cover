from django.core.management.base import BaseCommand
from store.models import Category, Author, Product, Slider
import random
import os

class Command(BaseCommand):
    help = 'Seed the database with bookstore data'

    def handle(self, *args, **kwargs):
        self.seed_categories()
        self.seed_authors()
        self.seed_products()
        self.seed_sliders()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def seed_categories(self):
        categories = [
            {"name": "Fiction", "featured": True, "order": 1},
            {"name": "Non-Fiction", "featured": True, "order": 2},
            {"name": "Fantasy", "featured": True, "order": 3},
            {"name": "History", "featured": False, "order": 4},
            {"name": "Science", "featured": False, "order": 5},
            {"name": "Biographies", "featured": False, "order": 6},
            {"name": "Romance", "featured": False, "order": 7},
            {"name": "Self-Help", "featured": False, "order": 8},
        ]
        for category_data in categories:
            Category.objects.get_or_create(name=category_data['name'], defaults=category_data)

    def seed_authors(self):
        authors = [
            {"name": "J.K. Rowling", "bio": "Author of the Harry Potter series, known for her fantasy novels."},
            {"name": "George R.R. Martin", "bio": "Famous for his epic fantasy series, 'A Song of Ice and Fire'."},
            {"name": "Stephen King", "bio": "Renowned author of horror, supernatural fiction, and suspense."},
            {"name": "Malcolm Gladwell", "bio": "Author of influential non-fiction books on social science."},
            {"name": "Yuval Noah Harari", "bio": "Historian and author known for 'Sapiens' and 'Homo Deus'."},
            {"name": "Jane Austen", "bio": "Classic author known for her novels of romantic fiction and social commentary."},
            {"name": "Agatha Christie", "bio": "Famous for her detective novels, including those featuring Hercule Poirot."},
        ]
        for author_data in authors:
            Author.objects.get_or_create(name=author_data['name'], defaults=author_data)

    def seed_products(self):
        categories = {cat.name: cat for cat in Category.objects.all()}
        authors = {auth.name: auth for auth in Author.objects.all()}

        # Mapping of products to specific authors and categories
        products = [
            {
                "name": "Harry Potter and the Sorcerer's Stone",
                "description": "The first book in J.K. Rowling's Harry Potter series. It introduces Harry Potter, a young wizard, and his adventures at Hogwarts.",
                "category": "Fiction",
                "author": "J.K. Rowling",
                "price": 29.99,
                "featured": True
            },
            {
                "name": "A Game of Thrones",
                "description": "The first book in George R.R. Martin's 'A Song of Ice and Fire' series, set in a medieval fantasy world.",
                "category": "Fantasy",
                "author": "George R.R. Martin",
                "price": 35.99,
                "featured": True
            },
            {
                "name": "The Shining",
                "description": "Stephen King's horror novel about a haunted hotel and a man losing his sanity.",
                "category": "Fiction",
                "author": "Stephen King",
                "price": 24.99,
                "image": "The_Shining.jpg",
                "featured": False
            },
            {
                "name": "Outliers: The Story of Success",
                "description": "Malcolm Gladwell's exploration of what makes high achievers different.",
                "category": "Non-Fiction",
                "author": "Malcolm Gladwell",
                "price": 19.99,
                "featured": False
            },
            {
                "name": "Sapiens: A Brief History of Humankind",
                "description": "Yuval Noah Harari's history of humanity from ancient times to the present.",
                "category": "History",
                "author": "Yuval Noah Harari",
                "price": 29.99,
                "featured": False
            },
            {
                "name": "Pride and Prejudice",
                "description": "Jane Austen's classic novel of manners, upbringing, and marriage in early 19th century England.",
                "category": "Romance",
                "author": "Jane Austen",
                "price": 14.99,
                "featured": False
            },
            {
                "name": "Murder on the Orient Express",
                "description": "Agatha Christie's famous detective novel featuring Hercule Poirot investigating a murder on a train.",
                "category": "Fiction",
                "author": "Agatha Christie",
                "price": 21.99,
                "featured": False
            },
            # Add more products as needed
        ]
        for product_data in products:
            category = categories.get(product_data['category'])
            author = authors.get(product_data['author'])

            # Assuming product_data['image'] already contains the correct relative path
            image_path = product_data['image']

            if category and author:
                Product.objects.create(
                    name=product_data["name"],
                    short_description=f"Short description for {product_data['name']}.",
                    description=product_data["description"],
                    price=product_data["price"],
                    category=category,
                    author=author,
                    featured=product_data["featured"]
                )
            else:
                self.stdout.write(self.style.ERROR(f'Error: Missing category or author for {product_data["name"]}'))

    def seed_sliders(self):
        sliders = [
            {"title": "Welcome to Our Bookstore", "subtitle": "Discover your next great read with us.", "order": 1},
            {"title": "Best Sellers", "subtitle": "Check out our top-selling books.", "order": 2},
            # ... other sliders
        ]
        for slider in sliders:
            Slider.objects.create(**slider)
