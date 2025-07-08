from RlStatsScraper import RlStatsScraper, Platform
import json
import datetime
import sys

def ranks_to_json(rank_objects, filename):
    output = dict()
    output['lastUpdatedTime'] = str(datetime.datetime.now())
    output['ranks'] = rank_objects
    with open(filename, 'w') as f:
        json.dump(output, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

if __name__ == '__main__':
    scraper = RlStatsScraper(Platform.STEAM, "wavdl")
    ranks = scraper.get_ranks()
    ranks_to_json(ranks, sys.argv[1])
