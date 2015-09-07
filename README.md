# AverageActorAges
## Description
A Python tool for finding the average ages of the casts of currently-playing movies. It uses `pyplot` from `matplotlib` to generate an easy-to-read bar graph of the results.
## API Dependencies
The tool relies on [MyAPIFilms](http://www.myapifilms.com/) for the list of currently-playing movies, the [OMDb API](http://www.omdbapi.com/) for actor lists for those movies, and [Wikipedia's API](https://www.mediawiki.org/wiki/API:Main_page) for actor biographies.
## Running
The tool can be run from the command line with a simple call:

    $ python average_actors_age.py

This will silently access the above APIs and generate a PDF with the default name `average_ages.pdf` with the resulting bar graph.
#### Command Line Arguments
There are various arguments that can be passed to the program.  If more than one is used, they must be combined (e.g., `-vn`).  If this is the case, order is irrelevant.

    $ python average_actors_age.py -v

will print to the terminal the status of the program as it is running.

    $ python average_actors_age.py -n {PDF name}

allows you to give a custom name to the bar graph PDF that is generated.
