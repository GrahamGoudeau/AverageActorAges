import re
import urllib
import requests
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

current_year = 2015

currently_playing_api = 'http://www.myapifilms.com/imdb/inTheaters'

# format the following api urls with the movie title or actor and
# year if necessary and send a GET request
title_search_api = 'http://www.omdbapi.com/?t={}&plot=short&r=json&y={}'
actor_search_api = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={}&rvsection=0'

birth_date_regex = r'\| birth_date\s*=\s*{{.*?\|(\d+).*}}'

def get_current_movies():
    if True:
        r = requests.get(currently_playing_api)
        with open('content.txt', 'w') as f:
            f.write(r.content)

        content = json.loads(r.content)
    '''
    else:
        with open('content.txt', 'r') as f:
            content = json.loads(f.read())
            '''

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
    return urllib.quote_plus(string.encode('utf8'))

# requires a url-safe movie title
def get_actor_list(title):
    r = requests.get(title_search_api.format(title, current_year))
    content = json.loads(r.content)

    # try searching for movies the previous year too
    if 'Error' in content:
        r = requests.get(title_search_api.format(title, current_year - 1))
        content = json.loads(r.content)

        # if still an error, then the movie cannot be found
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

    # get the actor's name from the wikipedia info box
    infobox = pages[page_number]['revisions'][0]['*']
    search_obj = re.search(birth_date_regex, infobox)
    if search_obj:
        return current_year - int(search_obj.group(1))

if __name__ == "__main__":
    print "Gathering currently playing movies..."
    currently_playing_titles = get_current_movies()
    movie_age_map = {}

    # cache actor names we have seen already
    actor_age_map = {}

    titles = []
    ages = []
    for title in currently_playing_titles:
        print "Gathering actor/actress information for '{}'".format(title)
        actor_list = get_actor_list(get_url_safe_title(title))

        for actor in actor_list:
            safe_actor = get_url_safe_actor(actor)

            # if seen this actor already, use the cached value
            if safe_actor in actor_age_map:
                ages.append(actor_age_map[safe_actor])
                titles.append(title)
            else:
                age = get_actor_age(safe_actor)

                # only consider ages we actually found
                if age is not None:
                    titles.append(title)
                    ages.append(age)
                    actor_age_map[safe_actor] = age

        if len(ages) > 0:
            movie_age_map[title] = (sum(ages) * 1.0) / len(ages)
    '''
    index = np.arange(len(currently_playing_titles))
    opacity = 0.4
    bar_width = 0.35
    plt.bar(index, ages, bar_width, alpha=opacity,
            color='b', label='Average age of cast')
    plt.xlabel('Movie')
    plt.ylabel('Average age')
    plt.title('Average ages of movie casts')
    plt.xticks(index, titles)
    plt.legend()
    plt.tight_layout()
    '''
    plt.bar(titles, ages, align='center')
    plt.title('Average ages of movie casts')
    plt.xlabel('Movies')
    plt.ylabel('Average age')
    plt.savefig()
    for key in movie_age_map.keys():
        print key, movie_age_map[key]
