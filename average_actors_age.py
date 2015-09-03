import re
import urllib
import requests
import json

current_year = 2015

currently_playing_api = 'http://www.myapifilms.com/imdb/inTheaters?actors=S'

# format the api urls with the movie title or actor and send a GET request
title_search_api = 'http://www.omdbapi.com/?t={}&plot=short&r=json&y=' + str(current_year)
print title_search_api
actor_search_api = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={}&rvsection=0'

birth_date_regex = r'\| birth_date\s*=\s*{{.*?\|(\d+).*}}'

def get_current_movies():
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
        for movie in entry['movies']:
            if movie['originalTitle']:
                in_theaters.append(movie['originalTitle'])
            else:
                in_theaters.append(movie['title'])

    return in_theaters

def get_url_safe_title(string):
    return urllib.quote_plus(string.encode('utf8'))

def get_url_safe_actor(string):
    # replace spaces with underscores to conform to wikipedia api
    string = string.replace(' ', '_')
    print urllib.quote_plus(string.encode('utf8'))
    return urllib.quote_plus(string.encode('utf8'))

# requires a url-safe movie title
def get_actor_list(title):
    r = requests.get(title_search_api.format(title))
    content = json.loads(r.content)
    if 'Error' in content:
        return []
    actors_string = content['Actors']
    actors_list = actors_string.split(',')
    for index, actor in enumerate(actors_list):
        if actor[0] == ' ':
            actors_list[index] = actor[1:]

    return actors_list

# requires url-safe actor name
def get_actor_age(actor):
    r = requests.get(actor_search_api.format(actor))
    content = json.loads(r.content)
    pages = content['query']['pages']

    # expect only one page
    page_number = pages.keys()[0]
    if 'missing' in pages[page_number]:
        # actor not on wikipedia or name different
        return None
    infobox = pages[page_number]['revisions'][0]['*']
    search_obj = re.search(birth_date_regex, infobox)
    if search_obj:
        return current_year - int(search_obj.group(1))

'''
movie_actor_map = {}
actor_age_map = {}

for movie in in_theaters:
    # encode movie titles as utf8 and make them url-safe
    actor_list = get_actor_list(get_url_safe_string(movie))
    print actor_list
r = requests.get('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=Simon_Pegg&rvsection=0')
print r.content
'''

if __name__ == "__main__":
    currently_playing_titles = get_current_movies()
    movie_age_map = {}

    # cache actor names we have seen already
    actor_age_map = {}

    for title in currently_playing_titles:
        safe_title = get_url_safe_title(title)
        actor_list = get_actor_list(safe_title)
        print actor_list

        ages = []
        for actor in actor_list:
            safe_actor = get_url_safe_actor(actor)

            # if seen this actor already, use the cached value
            if safe_actor in actor_age_map:
                ages.append(actor_age_map[safe_actor])
            else:
                age = get_actor_age(safe_actor)

                # only consider ages we actually found
                if age is not None:
                    ages.append(age)
                    actor_age_map[safe_actor] = age

        if len(ages) > 0:
            print title
            print "Average age:"
            print (sum(ages) * 1.0) / len(ages)
