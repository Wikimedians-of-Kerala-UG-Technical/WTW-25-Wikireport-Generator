# Malayalam Movie Report Generator

A project that **downloads Malayalam movie data from Wikidata** and provides tools to analyze and visualize it.

## What It Does

1. **Downloads Data**: Fetches Malayalam movies from Wikidata including titles, directors, release years, and genres
2. **Generates Reports**: Creates detailed reports showing:
   - Total number of movies and unique directors
   - Top 10 most prolific directors
   - Genre distribution
   - Movies organized by year
3. **Web Dashboard**: Provides an interactive web interface to:
   - View statistics and summaries
   - Filter movies by year range
   - Browse all movies with their details

## How to Use

- **Download movies**: `python download_movies.py` - fetches data from Wikidata
- **Generate reports**: `python report_generator.py [start_year] [end_year]` - creates text reports
- **Start web app**: `python app.py` - launches the interactive dashboard on http://127.0.0.1:5000
