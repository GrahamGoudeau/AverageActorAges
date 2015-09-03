import urllib
import requests
import json

r = requests.get('http://www.myapifilms.com/imdb/inTheaters?actors=S')
content = json.loads(r.content)

in_theaters = []
for entry in content:
    print entry.keys()
    for movie in entry['movies']:
        print movie.keys()
        print movie['title']
        in_theaters.append(movie['title'])

movie_actor_map = {}
actor_age_map = {}

    #print movie['movies']['originalTitle']
    #print movie
