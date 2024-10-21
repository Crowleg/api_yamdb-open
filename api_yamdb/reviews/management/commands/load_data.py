import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data import...'))

        self.load_users()
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_reviews()
        self.load_comments()

        self.stdout.write(self.style.SUCCESS('Data import completed.'))

    def load_users(self):
        """Загружаем данные пользователей из users.csv"""
        file_path = os.path.join(DATA_DIR, 'users.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    bio=row['bio'],
                )
        self.stdout.write(self.style.SUCCESS('Users loaded'))

    def load_categories(self):
        """Загружаем данные категорий из categories.csv"""
        file_path = os.path.join(DATA_DIR, 'category.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
        self.stdout.write(self.style.SUCCESS('Categories loaded'))

    def load_genres(self):
        """Загружаем данные жанров из genre.csv"""
        file_path = os.path.join(DATA_DIR, 'genre.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
        self.stdout.write(self.style.SUCCESS('Genres loaded'))

    def load_titles(self):
        """Загружаем данные произведений из titles.csv"""
        file_path = os.path.join(DATA_DIR, 'titles.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category,
                )
        self.stdout.write(self.style.SUCCESS('Titles loaded'))

    def load_reviews(self):
        """Загружаем данные отзывов из review.csv"""
        file_path = os.path.join(DATA_DIR, 'review.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    title=title,
                    author=author,
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Reviews loaded'))

    def load_comments(self):
        """Загружаем данные комментариев из comments.csv"""
        file_path = os.path.join(DATA_DIR, 'comments.csv')
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    review=review,
                    author=author,
                    text=row['text'],
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Comments loaded'))
