---
layout: post
author: William Van Der Laar
title: "Sharing my daily Rocket League ranking."
date: 2025-08-08 10:00:00 -0500
published: true
---

I recently added a [page](/ranks/) to this website that shows my latest Rocket League Rank. When I first had the idea, I
was
worried it might be a significant project. In the end, it was less than 100 lines of Python and a simple GitHub
workflow.
Here's how I did it.

---
---

{% include ranks.html %}

---
---

I was initially inspired
by [this post](https://parkerhiggins.net/2025/07/cascading-github-action-workflows-for-static-sites/) explaining how to
use cascading GitHub workflows to update a static GitHub Pages site. I'm not quite interesting enough to have a live
feed of all of the movies/books/shows I've consumed, but I do play a lot of Rocket League in my free time. The first
problem I had to solve was where to pull my rank data from, and then how I wanted the workflow to pull that data into my
repo. I considered following the article's lead and have the rank data live in a Google Sheet that would serve as an
intermediary data source between a cron job that would pull the rank data and the workflow that would insert it into my
website. Instead, I decided to just dump a simple JSON file into my websites _data directory which is overwritten on
each run of the cron job with the current rank data. In the future, I may extend my solution to keep a historical log of
my rank progression or other game statistics in a proper data store, but I decided that just displaying my current rank
would be good enough for a proof of concept.

The source of truth for Rocket League rank data is controlled by Psyonix (or now, Epic Games). There is a semi-public
API to pull rank data for any specific user which is how you can look yours up on sites
like [RL Tracker](https://tracker.gg) and [RLStats.net](https://rlstats.net),
but you need specific permission from Psyonix to get an API key. After reading a few dejected conclusions to Reddit
threads of other curious programmers, I knew my chances of have having direct API access were slim to none. This meant I
would have to go through the existing rank tracking websites, either through an intermediate API or by scraping my
profile off of their site. At this point I reached out to the owner of rlstats.net since it appeared to be just one guy
providing the service. He confirmed my fears that they don't give out API access any more, and part of his agreement to
continue using it was to not extend access through his own API. He was gracious enough however to give tacit endorsement
of me scraping his site by saying he wouldn't try to stop me as long as I didn't send any heavy traffic. All I wanted
was at most a couple of GET calls per day, so I was in luck!

I had never written a web scraper before, but turns out it's really easy. After a few minutes of
reading the [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) documentation I had a few lines of python that
would pull the data I needed. The hardest part was just sifting through the HTML structure to find the elements I was
interested in. I've never been much of a frontend coder and usually touching HTML or JavaScript or CSS at all is enough
to ruin my day, but again, this was easy! Then I just dumped the ranks to a JSON file, wrote my own static web page that
is populated with the contents of the JSON file, and began applying my learnings on GitHub workflows. The workflow runs
each night, triggering my scraper script which pushes the new rank data which in turn triggers the re-build of my static
Jekyll site that is then published through GitHub Pages. Easy!

Now that my mind has been opened to the possibility of sharing more than just extended versions of Bluesky rants on this
site, I hope to fill it out with more stuff that I find interesting.

