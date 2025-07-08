import requests
from bs4 import BeautifulSoup
from enum import StrEnum

# skills_table format
#  1v1  | 2v2  | 3v3  | tourn
#  rank | rank | rank | rank
#  div  | div  | div  | div
#  mmr  | mmr  | mmr  | mmr
#   ... | ...  | ...  | ....
def get_ranks_from_table(skills_table):
    result = []
    for i, row in enumerate(skills_table.find_all('tr')):
        headers = row.find_all('th')
        if headers and result:
            # Second set of headers means we've gotten all the info I care about
            break
        elif headers:
            result = [Rank(h.text) for h in headers]
            continue
        cells = row.find_all('td')
        for j in range(len(cells)):
            if i == 1:
                result[j].rank = cells[j].text
            if i == 2:
                result[j].division = cells[j].text
            if i == 3:
                # The MMR cells (sometimes) have div +- distances. Parsing just the MMR
                if len(cells[j].contents) > 1:
                    result[j].mmr = int(cells[j].contents[1])
    return result


class Rank:
    playlist = ""
    mmr = 0
    rank = ""
    division = ""
    def __init__(self, playlist):
        self.playlist = playlist

    def __str__(self):
        return "{}: {} - {} | {}".format(self.playlist, self.rank, self.division, self.mmr)

class Platform(StrEnum):
    STEAM = "Steam"
    EPIC = "Epic"
    PSN = "PS4"
    XBOX = "Xbox"

class RlStatsScraper:
    URL_ = 'https://rlstats.net/profile/'
    className_ = 'block-skills'
    platform_ = Platform.STEAM
    username_ = "wavdl"

    def __init__(self, platform, username):
        self.platform_ = platform
        self.username_ = username

    def get_ranks(self):
        page = requests.get(self.URL_ + self.platform_ + '/' + self.username_)
        soup = BeautifulSoup(page.content, "html.parser")
        block_skills = soup.find_all("div", class_=self.className_)
        if len(block_skills) == 0:
            print("ERROR: Couldn't find ranking class:", self.className_)
            return None
        ranks = get_ranks_from_table(block_skills[0].find("table"))
        return ranks
