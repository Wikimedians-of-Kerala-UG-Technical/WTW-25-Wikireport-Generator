import json

data = json.load(open('malayalam_movies.json'))
years = [int(m['release_year']) for m in data['movies'] if m.get('release_year') and str(m.get('release_year')).isdigit()]
print(f'Year range: {min(years)} - {max(years)}')

recent = [m for m in data['movies'] if 2020 <= int(m.get('release_year', '0') or '0') <= 2025]
print(f'Movies 2020-2025: {len(recent)}')
# last