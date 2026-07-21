from RlStatsScraper import RlStatsScraper, Platform
from storygraph_api import User, Book
from rss_parser import RSSParser
from requests import get
from html.parser import HTMLParser

import pinboard
import json
import datetime
import sys

def ranks_to_json(filename):
    scraper = RlStatsScraper(Platform.STEAM, "wavdl")
    output = dict()
    output['lastUpdatedTime'] = str(datetime.datetime.now())
    scraped_ranks = scraper.get_ranks()
    ranks = []
    for rank in scraped_ranks:
        if 'Tournament' in rank.playlist:
            continue
        ranks.append(rank)
    output['ranks'] = ranks
    with open(filename, 'w') as f:
        json.dump(output, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def books_to_json(filename, cookie):
    output = dict()
    output['lastUpdatedTime'] = str(datetime.datetime.now())
    user = User()
    read_books_str = user.books_read('wavdl', cookie=cookie)
    read_books = json.loads(read_books_str)[:15]
    output['read'] = read_books[:15]
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)

def links_to_json(filename, api_key):
    pb = pinboard.Pinboard(api_key)
    posts = pb.posts.recent(tag=["reading-list", "python"])
    bookmarks = posts['posts'][:15]
    recents = []
    for bookmark in bookmarks:
        entry = {
        'title': bookmark.description,
        'description': bookmark.extended,
        'url': bookmark.url
        }
        recents.append(entry)
    output = {'recent': recents, 'lastUpdatedTime': str(datetime.datetime.now())}
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)

def movies_to_json(filename):

    rss_url = "https://letterboxd.com/wavdl/rss/"
    response = get(rss_url)
    rss = RSSParser.parse(response.text)

    class MovieHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.img_src = ""
            self.review = ""
            self.in_paragraph = False

        def clear_movie(self):
            self.img_src = ""
            self.review = ""

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                self.img_src = attrs[0][1]
            if tag == "p":
                self.in_paragraph = True

        def handle_endtag(self, tag):
            if tag == "p":
                self.in_paragraph = False

        def handle_data(self, data):
            if self.in_paragraph:
                self.review = data.strip()

    parser = MovieHTMLParser()

    output = dict()
    output['watched'] = []
    for item in rss.channel.items:
        parser.feed(item.description.content)
        output['watched'].append({'title': item.title.content, 'image': parser.img_src, 'review': parser.review, 'link': item.links[0].content})
        parser.clear_movie()
    output['watched'] = output['watched'][:15]

    output['lastUpdatedTime'] = str(datetime.datetime.now())
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)

# Usage: python3 _scripts/PullUpdates.py <storygraph-cookie> <pinboard-api-key>
if __name__ == '__main__':
    movies_to_json("_data/movies.json")
    # Scrape Rocket League ranks
    ranks_to_json("_data/ranks.json")
    # Scrape StoryGraph reading list.
    cookie = sys.argv[1]
    books_to_json("_data/books.json", cookie)
    # Pull Pinboard reading list.
    api_key = sys.argv[2]
    links_to_json("_data/links.json", api_key)
