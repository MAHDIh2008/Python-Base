import csv
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    director: str
    year: int
    watched: bool = False

    def mark_watched(self):
        self.watched = True

    def __str__(self):
        status = "✓" if self.watched else "✗"
        return f"[{status}] {self.title} ({self.year}) - Director: {self.director}"

class MovieManager:
    FILE = 'movies.csv'
    movies: List[Movie] = []

    @classmethod
    def load_movies(cls):
        if os.path.exists(cls.FILE):
            try:
                with open(cls.FILE, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    cls.movies = [
                        Movie(
                            row['title'],
                            row['director'],
                            int(row['year']),
                            row['watched'].upper() == 'TRUE'
                        )
                        for row in reader
                        if row['title'] and row['director'] and row['year']
                    ]
            except Exception as e:
                print(f"❌ Error loading movies: {e}")

    @classmethod
    def save_movies(cls):
        try:
            with open(cls.FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'director', 'year', 'watched'])
                writer.writeheader()
                for movie in cls.movies:
                    writer.writerow({
                        'title': movie.title,
                        'director': movie.director,
                        'year': movie.year,
                        'watched': str(movie.watched)
                    })
        except Exception as e:
            print(f"❌ Error saving movies: {e}")

    @classmethod
    def add_movie(cls):
        try:
            title = input("Title: ").strip()
            if not title:
                raise ValueError("Title cannot be empty")
                
            director = input("Director: ").strip()
            if not director:
                raise ValueError("Director cannot be empty")
                
            year = int(input("Year: ").strip())
            if year <= 1800 or year > 2100:
                raise ValueError("Invalid year")
                
            cls.movies.append(Movie(title, director, year))
            cls.save_movies()
            print("✅ Movie added successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    @classmethod
    def show_movies(cls, movies: List[Movie] = None):
        movies_to_show = movies or cls.movies
        if not movies_to_show:
            print("🎬 No movies in collection")
            return
            
        print("\n🎬 Movie Collection:")
        print("=" * 60)
        for idx, movie in enumerate(movies_to_show, 1):
            print(f"{idx}. {movie}")

    @classmethod
    def search_movies(cls):
        query = input("Search (title/director/year): ").lower().strip()
        if not query:
            print("❌ Please enter a search term")
            return
            
        results = [
            movie for movie in cls.movies
            if (query in movie.title.lower() or
                query in movie.director.lower() or
                query in str(movie.year))
        ]
        
        cls.show_movies(results)

    @classmethod
    def mark_watched(cls):
        cls.show_movies()
        if not cls.movies:
            return
            
        try:
            choice = int(input("Select movie number to mark as watched: ")) - 1
            if 0 <= choice < len(cls.movies):
                cls.movies[choice].mark_watched()
                cls.save_movies()
                print("✅ Movie marked as watched!")
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")

    @classmethod
    def delete_movie(cls):
        cls.show_movies()
        if not cls.movies:
            return
            
        try:
            choice = int(input("Select movie number to delete: ")) - 1
            if 0 <= choice < len(cls.movies):
                deleted = cls.movies.pop(choice)
                cls.save_movies()
                print(f"✅ Deleted: {deleted.title}")
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")

def main():
    MovieManager.load_movies()
    
    menu = {
        '1': ('Add Movie', MovieManager.add_movie),
        '2': ('View All Movies', MovieManager.show_movies),
        '3': ('Search Movies', MovieManager.search_movies),
        '4': ('Mark as Watched', MovieManager.mark_watched),
        '5': ('Delete Movie', MovieManager.delete_movie),
        '6': ('Exit', None)
    }

    while True:
        print("\n🎥 Movie Manager")
        print("=" * 30)
        for k, (v, _) in menu.items():
            print(f"{k}. {v}")
            
        choice = input("\nEnter choice (1-6): ")
        if choice == '6':
            MovieManager.save_movies()
            print("👋 Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    main()