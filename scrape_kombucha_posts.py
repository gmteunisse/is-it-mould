import praw
import urllib.request
import json
import datetime
import os.path
import time

class Submission:

    # Base attributes imported from pushshift
    def __init__(self, ps_out):

        # PushShift parameters
        self.id = ps_out["id"]
        self.url = ps_out["url"]
        self.created = ps_out["created_utc"]
        self.retrieved = ps_out["retrieved_on"]
        self.title = ps_out["title"]
        self.media_meta = ps_out["media_metadata"] if "media_metadata" in ps_out.keys() else None
        self.original_flair = ps_out["link_flair_text"] if "link_flair_text" in ps_out.keys() else None
    
        # Inferred parameters
        self.has_image = False
        self.img_urls = []
        self.dl_imgs = False

        # PRAW parameters
        self.current_flair = None

    # Method to check for images
    def check_image(self):
        if self.url.endswith(('.jpg', '.jpeg')):
            self.has_image = True
            self.img_urls.append(self.url)
        elif self.media_meta is not None:
            self.has_image = True
            for id in self.media_meta.keys():
                try:
                    url = self.media_meta[id]["s"]["u"]
                    self.img_urls.append(url)
                except KeyError:
                    # Not all images are processed and therefore lack the "s" key
                    continue
    
    # Method to check if post has a relevant flair for downloading
    def check_download(self, flairs):
        if self.current_flair in flairs:
            self.dl_imgs = True

    # Method to extract additional PRAW parameters
    def import_praw(self, praw_subm):
        self.media_meta = praw_subm.media_metadata if "media_metadata" in vars(praw_subm) else None
        self.current_flair = praw_subm.link_flair_text if "link_flair_text" in vars(praw_subm) else None
        self.img_urls = []

# Function to call the API
def fetch_ps_submission(subreddit, limit, fields, begin_ts, end_ts):

    # Create the API call
    url = "https://api.pushshift.io/reddit/search/submission/?"
    subreddit_str = ("subreddit=%s" % subreddit) if subreddit is not None else ""
    sorting = "&sort=desc&sort_type=created_utc"
    limit_str = ("&size=%s" % limit) if limit is not None else ""
    fields_str = ("&fields=%s" % ",".join(fields)) if fields is not None else "&fields=created_utc,id"
    timespan_str = ("&before=%s&after=%s") % (end_ts, begin_ts)
    q = url + subreddit_str + sorting + limit_str + fields_str + timespan_str

    # Create call and read response
    response = urllib.request.urlopen(q)
    data = response.read()
    result = json.loads(data)["data"]
    return(result)

# Function to scrape all post between two dates
# dates in "MM/DD/YYYY"
def scrape_ps_subs(subreddit = None, limit = 100, fields = None, begin_date = None, end_date = None, verbose = True):

    # Max 100 hits per query
    limit = min(limit, 100)
    n_hits = limit

    # Get the most recent timestamp
    if end_date is None:
        end = datetime.datetime.today()
        end_ts = int(datetime.datetime.timestamp(end))
    else:
        end = datetime.datetime.strptime(end_date, "%m/%d/%Y")
        end_ts = int(datetime.datetime.timestamp(end))
    ts = int(end_ts)

    # Get the date at which to stop fetching posts
    if begin_date is None:
        raise ValueError("No begin date provided - aborting")
    begin = datetime.datetime.strptime(begin_date, "%m/%d/%Y")
    begin_ts = int(datetime.datetime.timestamp(begin))

    # Structure to store submissions
    posts = []

    # Fetch posts until they run out
    while (ts >= begin_ts and n_hits == limit):

        # Fetch and store results
        result = fetch_ps_submission(subreddit, limit, fields, begin_ts, ts)
        posts = posts + result

        # Update parameters
        n_hits = len(result)
        ts = int(result[n_hits - 1]["created_utc"])

        # Verbosity
        if verbose:
            dt = datetime.datetime.fromtimestamp(ts)
            print("Number of posts fetched: %d\t(date/time: %s)" % (len(posts), dt))
        time.sleep(1)


def main():
    submissions = scrape_ps_subs(
        subreddit = "kombucha", 
        fields = [
            'id',
            'media_metadata',
            'created_utc',
            'url',
            'link_flair_text',
            'retrieved_on',
            'title'], 
        begin_date = "03/01/2022")

if __name__ == "__main__":
    main()