# AverageActorAges
## Description
A Python tool for finding the average ages of the casts of currently-playing movies. It uses `pyplot` from `matplotlib` to generate an easy-to-read bar graph of the results. The bar graph is output as a PDF at the end of the process.
## API Dependencies
The tool relies on [MyAPIFilms](http://www.myapifilms.com/) for the list of currently-playing movies, the [OMDb API](http://www.omdbapi.com/) for actor lists for those movies, and [Wikipedia's API](https://www.mediawiki.org/wiki/API:Main_page) for actor biographies.
## Running
The tool can be run from the command line with a simple call using Python 2.7:

    $ python average_actors_age.py

This will silently access the above APIs and generate a PDF with the default name `average_ages.pdf` with the resulting bar graph. If a currently-playing movie does not appear in the final bar graph, it is because searching for the actors or their ages failed in some way.
#### Command Line Arguments
There are various arguments that can be passed to the program.  If more than one is used, they must be combined (e.g., `-vn`).  If this is the case, order is irrelevant.

    $ python average_actors_age.py -v

will print to the terminal the status of the program as it is running.

    $ python average_actors_age.py -n {PDF name}

allows you to give a custom name to the bar graph PDF that is generated.  Only provide the filename up to the `.pdf` extension.
## Design Difficulties
Certain difficulties inherent in the problem presented themselves while coding this tool.  Among them:
* _Spelling consistency_ - Often, an actor's name will be returned from the OMDb API in a form that does not exactly match that expected by the Wikipedia API.  When this happens, the Wikipedia API returns a `missing` result, and that actor is skipped.  A common reason for this happening is when the actor's middle name is not included in the result list from OMDb, while their Wikipedia article title does contain their middle name (or vice versa).  Another cause for this problem is when the name contains punctuation, like the '.' in 'Jr.' or the ',' before 'Jr.', like 'John Example, Jr.'. This can cause the population size for the movie to be reduced, affecting the accuracy of the average age.
* _API service reliability_ - The OMDb API's blog reports slowness of their service as of 9/6/15.  This can rarely cause the requests to the service to time out, or at least make our performance suffer.  The same blog reports that API keys will soon be introduced, which will break this tool as API keys were not in use at the time of its creation.
* _API affiliation_ - Neither the OMDb nor the MyAPIFilms APIs are officially affiliated with IMDb.  This means that it is possible that their data could be outdated, or service could unexpectedly drop since they are not maintained by IMDb.
