from RlStatsScraper import RlStatsScraper, Platform
from storygraph_api import User, Book
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
    user = User()
    read_books_str = user.books_read('wavdl', cookie=cookie)
    read_books = json.loads(read_books_str)[:15]
    book = Book()
    for read_book in read_books:
        info_str = book.book_info(read_book['book_id'])
        info = json.loads(info_str)
        read_book['authors'] = info['authors']
    output['read'] = read_books[:15]
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)

def links_to_json(filename, api_key):
    pb = pinboard.Pinboard(api_key)
    posts = pb.posts.recent(tag=["reading-list", "python"])
    bookmarks = posts['posts'][:10]
    recents = []
    for bookmark in bookmarks:
        entry = {
        'title': bookmark.description,
        'description': bookmark.extended,
        'url': bookmark.url
        }
        recents.append(entry)
    output = {'recent': recents}
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)


if __name__ == '__main__':
    # Scrape Rocket League ranks
    ranks_to_json(sys.argv[1])
    # Scrape StoryGraph reading list.
    cookie = sys.argv[4]
    books_to_json(sys.argv[2], cookie)
    # Pull Pinboard reading list.
    api_key = sys.argv[5]
    links_to_json(sys.argv[3], api_key)
