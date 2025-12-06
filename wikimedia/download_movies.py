import requests
import json
import os
from datetime import datetime

def download_malayalam_movies():
    """
    Download Malayalam movies from Wikidata using SPARQL query.
    Fetches: title, director, release year, genre, cast
    """
    
    sparql_query = """
    SELECT ?movie ?movieLabel ?director ?directorLabel ?releaseYear ?genre ?genreLabel ?actor ?actorLabel
    WHERE {
      ?movie wdt:P31 wd:Q11424 ;
             wdt:P364 wd:Q36236 .
      
      OPTIONAL { ?movie wdt:P57 ?director . }
      OPTIONAL { ?movie wdt:P577 ?date . BIND(YEAR(?date) AS ?releaseYear) }
      OPTIONAL { ?movie wdt:P136 ?genre . }
      OPTIONAL { ?movie wdt:P161 ?actor . }
      
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
    }
    LIMIT 20000
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "Malayalam-Movie-Downloader/1.0",
        "Accept": "application/sparql-results+json"
    }
    
    params = {
        "query": sparql_query,
        "format": "json"
    }
    
    print("[*] Downloading Malayalam movies from Wikidata...")
    print(f"[*] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[*] Sending SPARQL query to Wikidata Query Service...\n")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        bindings = data.get("results", {}).get("bindings", [])
        
        print(f"[+] Received {len(bindings)} results from Wikidata")
        
        movies_dict = {}
        
        for binding in bindings:
            movie_id = binding.get("movie", {}).get("value", "").split("/")[-1]
            movie_label = binding.get("movieLabel", {}).get("value", "")
            director_label = binding.get("directorLabel", {}).get("value", "")
            release_year = binding.get("releaseYear", {}).get("value", "")
            genre_label = binding.get("genreLabel", {}).get("value", "")
            actor_label = binding.get("actorLabel", {}).get("value", "")
            
            if movie_id not in movies_dict:
                movies_dict[movie_id] = {
                    "id": movie_id,
                    "title": movie_label,
                    "directors": [],
                    "release_year": release_year if release_year else None,
                    "genres": [],
                    "actors": []
                }
            
            if director_label and director_label not in movies_dict[movie_id]["directors"]:
                movies_dict[movie_id]["directors"].append(director_label)
            
            if genre_label and genre_label not in movies_dict[movie_id]["genres"]:
                movies_dict[movie_id]["genres"].append(genre_label)
            
            if actor_label and actor_label not in movies_dict[movie_id]["actors"]:
                movies_dict[movie_id]["actors"].append(actor_label)
        
        movies_list = list(movies_dict.values())
        
        output_file = os.path.join(os.path.dirname(__file__), "malayalam_movies.json")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "downloaded_at": datetime.now().isoformat(),
                    "total_movies": len(movies_list),
                    "source": "Wikidata Query Service"
                },
                "movies": movies_list
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[+] Saved {len(movies_list)} unique Malayalam movies to malayalam_movies.json\n")
        
        return movies_list
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Error downloading data: {e}\n")
        return []

if __name__ == "__main__":
    download_malayalam_movies()
