from flask import Flask, render_template, request, jsonify
import json
import os
from collections import Counter

app = Flask(__name__)

def load_movies():
    """Load Malayalam movies from JSON file."""
    json_file = os.path.join(os.path.dirname(__file__), "malayalam_movies.json")
    
    if not os.path.exists(json_file):
        return None
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def get_all_years():
    """Get all unique years from movies."""
    data = load_movies()
    if not data or "movies" not in data:
        return []
    
    years = set()
    for movie in data["movies"]:
        year = movie.get("release_year")
        if year and year.isdigit():
            years.add(int(year))
    
    return sorted(list(years), reverse=True)

def filter_movies_by_year(start_year=None, end_year=None):
    """Filter movies by year range."""
    data = load_movies()
    if not data or "movies" not in data:
        return []
    
    movies = data["movies"]
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

def filter_movies_by_director(director_name=None):
    """Filter movies by director name."""
    data = load_movies()
    if not data or "movies" not in data:
        return []
    
    if not director_name:
        return data["movies"]
    
    movies = data["movies"]
    filtered = []
    director_name_lower = director_name.lower()
    
    for movie in movies:
        if movie.get("directors"):
            for director in movie["directors"]:
                if director_name_lower in director.lower():
                    filtered.append(movie)
                    break
    
    return sorted(filtered, key=lambda x: x.get("title", ""))

def filter_movies_by_title(movie_title=None):
    """Filter movies by title."""
    data = load_movies()
    if not data or "movies" not in data:
        return []
    
    if not movie_title:
        return data["movies"]
    
    movies = data["movies"]
    filtered = []
    title_lower = movie_title.lower()
    
    for movie in movies:
        if title_lower in movie.get("title", "").lower():
            filtered.append(movie)
    
    return sorted(filtered, key=lambda x: x.get("title", ""))

def filter_movies_by_actor(actor_name=None):
    """Filter movies by actor name."""
    data = load_movies()
    if not data or "movies" not in data:
        return []
    
    if not actor_name:
        return data["movies"]
    
    movies = data["movies"]
    filtered = []
    actor_name_lower = actor_name.lower()
    
    for movie in movies:
        if movie.get("actors"):
            for actor in movie["actors"]:
                if actor_name_lower in actor.lower():
                    filtered.append(movie)
                    break
    
    return sorted(filtered, key=lambda x: x.get("title", ""))

def compute_statistics(movies=None):
    """Compute statistics from movie data."""
    data = load_movies()
    
    if not data or "movies" not in data:
        return {
            "total_movies": 0,
            "unique_directors": 0,
            "unique_genres": 0,
            "top_directors": [],
            "genres": [],
            "movies": [],
            "downloaded_at": "N/A",
            "years": []
        }
    
    if movies is None:
        movies = data["movies"]
    
    metadata = data.get("metadata", {})
    
    all_directors = []
    all_genres = []
    
    for movie in movies:
        if movie.get("directors"):
            all_directors.extend(movie["directors"])
        if movie.get("genres"):
            all_genres.extend(movie["genres"])
    
    unique_directors = list(set(all_directors))
    unique_genres = list(set(all_genres))
    director_counts = Counter(all_directors)
    genre_counts = Counter(all_genres)
    
    return {
        "total_movies": len(movies),
        "unique_directors": len(unique_directors),
        "unique_genres": len(unique_genres),
        "top_directors": [{"name": name, "count": count} for name, count in director_counts.most_common(10)],
        "genres": [{"name": name, "count": count} for name, count in genre_counts.most_common(15)],
        "movies": sorted(movies, key=lambda x: x.get("title", "")),
        "downloaded_at": metadata.get("downloaded_at", "N/A"),
        "years": get_all_years()
    }

@app.route("/")
def index():
    """Render the main dashboard."""
    stats = compute_statistics()
    return render_template("index.html", stats=stats)

@app.route("/api/years")
def api_years():
    """API endpoint to get all available years."""
    years = get_all_years()
    return jsonify({"years": years})

@app.route("/api/report/by-year")
def api_report_by_year():
    """API endpoint to generate report filtered by year range."""
    start_year = request.args.get("start_year", type=int)
    end_year = request.args.get("end_year", type=int)
    
    filtered_movies = filter_movies_by_year(start_year, end_year)
    stats = compute_statistics(filtered_movies)
    
    movies_by_year = {}
    for movie in filtered_movies:
        year = movie.get("release_year")
        if year:
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(movie.get("title", "Unknown"))
    
    return jsonify({
        "filter": {
            "start_year": start_year,
            "end_year": end_year
        },
        "statistics": stats,
        "movies_by_year": movies_by_year,
        "total_in_range": len(filtered_movies)
    })

@app.route("/api/movies/by-year")
def api_movies_by_year():
    """API endpoint to get movies filtered by year range."""
    start_year = request.args.get("start_year", type=int)
    end_year = request.args.get("end_year", type=int)
    
    filtered_movies = filter_movies_by_year(start_year, end_year)
    
    return jsonify({
        "total": len(filtered_movies),
        "movies": filtered_movies
    })

@app.route("/api/directors")
def api_get_all_directors():
    """API endpoint to get all unique directors."""
    data = load_movies()
    if not data or "movies" not in data:
        return jsonify({"directors": []})
    
    all_directors = []
    for movie in data["movies"]:
        if movie.get("directors"):
            all_directors.extend(movie["directors"])
    
    unique_directors = sorted(list(set(all_directors)))
    return jsonify({"directors": unique_directors})

@app.route("/api/report/by-director")
def api_report_by_director():
    """API endpoint to generate report filtered by director."""
    director_name = request.args.get("director", "")
    
    filtered_movies = filter_movies_by_director(director_name) if director_name else []
    stats = compute_statistics(filtered_movies)
    
    movies_by_year = {}
    for movie in filtered_movies:
        year = movie.get("release_year")
        if year:
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(movie.get("title", "Unknown"))
    
    return jsonify({
        "filter": {
            "director": director_name
        },
        "statistics": stats,
        "movies_by_year": movies_by_year,
        "total_in_range": len(filtered_movies)
    })

@app.route("/api/report/by-movie-title")
def api_report_by_movie_title():
    """API endpoint to generate report filtered by movie title."""
    title = request.args.get("title", "")
    
    filtered_movies = filter_movies_by_title(title) if title else []
    stats = compute_statistics(filtered_movies)
    
    movies_by_year = {}
    for movie in filtered_movies:
        year = movie.get("release_year")
        if year:
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(movie.get("title", "Unknown"))
    
    return jsonify({
        "filter": {
            "title": title
        },
        "statistics": stats,
        "movies_by_year": movies_by_year,
        "total_in_range": len(filtered_movies)
    })

@app.route("/api/report/by-actor")
def api_report_by_actor():
    """API endpoint to generate report filtered by actor."""
    actor = request.args.get("actor", "")
    
    filtered_movies = filter_movies_by_actor(actor) if actor else []
    stats = compute_statistics(filtered_movies)
    
    movies_by_year = {}
    for movie in filtered_movies:
        year = movie.get("release_year")
        if year:
            if year not in movies_by_year:
                movies_by_year[year] = []
            movies_by_year[year].append(movie.get("title", "Unknown"))
    
    return jsonify({
        "filter": {
            "actor": actor
        },
        "statistics": stats,
        "movies_by_year": movies_by_year,
        "total_in_range": len(filtered_movies)
    })

if __name__ == "__main__":
    print("[*] Starting Flask application...")
    print("[*] Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host="127.0.0.1", port=5000)
