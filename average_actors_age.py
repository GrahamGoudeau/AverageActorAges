import urllib
import requests
import json

currently_playing_api = 'http://www.myapifilms.com/imdb/inTheaters?actors=S'
title_search_api = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'

if False:
    r = requests.get(currently_playing_api)
    with open('content.txt', 'w') as f:
        f.write(r.content)

    content = json.loads(r.content)
else:
    print "Not making api call"
    with open('content.txt', 'r') as f:
        content = json.loads(f.read())

in_theaters = []
for entry in content:
    print entry.keys()
    for movie in entry['movies']:
        print movie.keys()
        print movie['title']
        in_theaters.append(movie['title'])

movie_actor_map = {}
actor_age_map = {}

# requires a url-safe movie title
def get_actor_list(title):
    url = title_search_api.format(title)
    print url

for movie in in_theaters:
    # encode movie titles as utf8 and make them url-safe
    url_safe_movie = urllib.quote_plus(movie.encode('utf8'))
    get_actor_list(url_safe_movie)
