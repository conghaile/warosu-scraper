# warosu-scraper
HTML scraper for warosu.org. It will scrape the post numbers, subjects (if available), post content, and timecode of every opening post on a given board, beginning from the most recently archived to the beginning of the board or beginning of archival.
The scraper can be used by typing the following into the command line:
```
python scraper.py
```

The scraper can currently:

-Dump posts as raw JSON files to a new ./posts directory (if it doesn't already exist) in the following format:
```
{"number": <post number>,
  "subject": <OP subject ('' if no subject in post)>,
  "text": [
    <first sentence of post>,
    <second sentence of post>,
    ...
    ],
  "time": <UNIX timestamp of post>}
```
-Save posts to a local Postgres database, presumed to be running at port 5432

-Save posts to a local MongoDB instance, presumed to be running at port 27017 unless otherwise specified

---

In order to dump raw JSON files, enter the following into the command line:
```
python scraper.py [board] flat
```
---

In order to save posts to a Postgres database, create a file called `database.ini` with the following format:
```
[postgresql]
host=localhost
database=[database name]
user=[username]
password=[password]
```

Save this file to the same directory that `scraper.py` is saved to, then type the following into the command line:
```
python scraper.py [board] postgres [OPTIONAL:table name]
```

If no table name is provided, the scraper will create a table called 'warosu' with the appropriate column names and types.
If a table name is provided, the scraper expects four string columns in the table, `number, subject, text, time`, each with type set to VARCHAR.

---
In order to save posts to a MongoDB instance, start the instance and then enter the following into the command line:
```
python scraper.py [board] mongo [OPTIONAL:port]
```
The posts will be stored in the same format as the raw JSON shown above. You may provide a port if your MongoDB instance isn't running at the default port (27017).

---
The python scripts in this repo require a sizeable number of packages. If an error occurs, simply install the relevant package and run again.
  
In the future, this repository will contain a docker image containing all necessary dependencies for ease of use.
 
The scraper requests warosu.org once per second and scrapes 20 threads per request. It's not advisable to increase the rate of requests, as you might get your IP blocked.
If speed of data ingestion is an issue, consider running multiple instances of the scraper, each from a different IP address. If you don't know how to do this, you probably shouldn't be trying to make so many requests anyways.
