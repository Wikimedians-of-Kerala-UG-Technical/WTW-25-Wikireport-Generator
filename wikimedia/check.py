import json  
data = json.load(open(r'c:\Users\Abel Anil\Downloads\wikimedia\wikimedia\malayalam_movies.json'))  
years = []  
for m in data.get('movies', []):  
 if m.get('release_year'):  
  try: years.append(int(m['release_year']))  
  except: pass  
if years:  
 print(f'Year range: {min(years)} - {max(years)}')  
 print(f'Total movies: {len(data.get(\\\"movies\\\", []))}')  
