# warosu-scraper
Basic HTML scraper for warosu.org. It will scrape the post numbers, subjects (if available), post content, and timecode of every OP on a given board beginning from the most recently archived to the beginning of the board or beginning of archival. Posts are saved locally to a 'posts' folder as .json in the following format:

{"number": <post number>,
  "subject": <OP subject ('' if no subject in post)>,
  "text": <post content>,
  "time": <UNIX timestamp of post>}
  
In the future, the scraper will support loading posts to MongoDB and SQL databases.
 
The scraper requests warosu.org once per second and scrapes 20 threads per request. If you decide to edit the scraper to request more frequently, don't come crying to me if you get your IP blacklisted.
  
Usage:
  
  scraper.py <board>
