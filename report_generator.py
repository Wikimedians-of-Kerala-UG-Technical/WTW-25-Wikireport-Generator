# start
import json
import os
from collections import Counter
import sys

def load_movies():
    """Load Malayalam movies from JSON file."""
    json_file = os.path.join(os.path.dirname(__file__), "malayalam_movies.json")
    
    if not os.path.exists(json_file):
        print("[-] malayalam_movies.json not found. Please run download_movies.py first.")
        return None
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[-] Error loading JSON: {e}")
        return None

def filter_movies_by_year(movies, start_year=None, end_year=None):
    """Filter movies by year range."""
    filtered = []
    
    for movie in movies:
        year = movie.get("release_year")
        if year and year.isdigit():
            year_int = int(year)
            if start_year and year_int < start_year:
                continue
            if end_year and year_int > end_year:
                continue
            filtered.append(movie)
    
    return sorted(filtered, key=lambda x: (int(x.get("release_year", "0")) if x.get("release_year", "").isdigit() else 0), reverse=True)

def generate_report(data, start_year=None, end_year=None):
    """Generate a comprehensive report from the movie data."""
    
    if not data or "movies" not in data:
        print("[-] No movie data available.")
        return
    
    movies = data["movies"]
    
    if start_year or end_year:
        movies = filter_movies_by_year(movies, start_year, end_year)
    
    print("\n" + "="*80)
    year_range = ""
    if start_year and end_year:
        year_range = f" ({start_year}-{end_year})"
    elif start_year:
        year_range = f" (from {start_year})"
    elif end_year:
        year_range = f" (until {end_year})"
    
    print(f"MALAYALAM MOVIES REPORT{year_range}".center(80))
    print("="*80 + "\n")
    
    all_directors = []
    all_genres = []
    movies_by_year = {}
    
    for movie in movies:
        if movie.get("directors"):
            all_directors.extend(movie["directors"])
        
        if movie.get("genres"):
            all_genres.extend(movie["genres"])
        
        year = movie.get("release_year")
        if year:
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(movie["title"])
    
    unique_directors = list(set(all_directors))
    unique_genres = list(set(all_genres))
    
    print(f"SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total Malayalam Movies:        {len(movies):>3}")
    print(f"Unique Directors:              {len(unique_directors):>3}")
    print(f"Unique Genres:                 {len(unique_genres):>3}")
    print(f"Years Covered:                 {len(movies_by_year):>3}")
    print()
    
    print(f"TOP 10 MOST PROLIFIC DIRECTORS")
    print("-" * 80)
    director_counts = Counter(all_directors)
    for i, (director, count) in enumerate(director_counts.most_common(10), 1):
        print(f"{i:2}. {director:<50} {count:>3} movie(s)")
    print()
    
    print(f"GENRE DISTRIBUTION")
    print("-" * 80)
    genre_counts = Counter(all_genres)
    for i, (genre, count) in enumerate(genre_counts.most_common(10), 1):
        print(f"{i:2}. {genre:<50} {count:>3} movie(s)")
    print()
    
    print(f"MOVIES BY YEAR")
    print("-" * 80)
    sorted_years = sorted([int(y) for y in movies_by_year.keys() if y.isdigit()], reverse=True)
    for year in sorted_years[:15]:
        count = len(movies_by_year[str(year)])
        print(f"{year}:  {count:>3} movie(s)")
    print()
    
    print(f"ALL MOVIES ({len(movies)} total)")
    print("-" * 80)
    for i, movie in enumerate(sorted(movies, key=lambda x: x.get("title", "")), 1):
        title = movie.get("title", "Unknown")
        directors = ", ".join(movie.get("directors", ["Unknown"])) if movie.get("directors") else "Unknown"
        year = movie.get("release_year", "N/A")
        genres = ", ".join(movie.get("genres", [])) if movie.get("genres") else "N/A"
        
        print(f"\n{i}. {title}")
        print(f"   Director(s): {directors}")
        print(f"   Year: {year}")
        print(f"   Genre(s): {genres}")
    
    print("\n" + "="*80)
    print()

if __name__ == "__main__":
    start_year = None
    end_year = None
    
    if len(sys.argv) > 1:
        try:
            start_year = int(sys.argv[1])
            if len(sys.argv) > 2:
                end_year = int(sys.argv[2])
            else:
                end_year = start_year
        except ValueError:
            print("Usage: python report_generator.py [start_year] [end_year]")
            print("Example: python report_generator.py 2010 2015")
            sys.exit(1)
    
    data = load_movies()
    if data:
        generate_report(data, start_year, end_year)
