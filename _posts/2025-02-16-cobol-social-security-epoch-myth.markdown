---
layout: post
author: William Van Der Laar
title:  "COBOL, Social Security, and the epoch myth."
date:   2025-02-16 10:00:00 -0500
published: true
---
Elon Musk is a [liar](https://www.msn.com/en-us/entertainment/entertainment-celebrity/elon-musk-baselessly-claims-150-year-olds-are-collecting-social-security-in-bizarre-rant/ar-AA1yVvi7), but that doesn't mean you need to lie too.

> First, a disclaimer. I am not a COBOL expert, nor do I have any experience with old IBM mainframe systems. In my 8 years as a Software Engineer, the oldest thing I worked on was a codebase from the 90s written in Ada. That is pretty old in software age, but the COBOL ecosystem is still comparatively ancient. If any actual COBOL experts read this, I would happily take your feedback.


## Background
While scrolling bluesky I saw a post with this screenshot making fun of Elon Musk and his people for not knowing how to code.

![wrong](/assets/wrong-explanation.jpg)

At first glance this explanation seems plausible. I have used timestamps based on the Unix Epoch on almost a daily basis in my previous work, and it would make sense for a language created before the Unix Epoch to simply use an earlier epoch date. But then I stopped and thought about it for 5 seconds.

In the end, as sure as I am that Elon is not a good coder, I am also sure that the people spreading this explanation do not know what they're talking about either. After seeing this [same misinformation](https://bsky.app/profile/pbump.com/post/3li5daxur322v) pop up [repeatedly](https://bsky.app/profile/karlykingsley.bsky.social/post/3li6zohbkkn26) on [several](https://www.instagram.com/reel/DGECzHdS5wI/?igsh=dHBlcjE1b3BpNm1h) social media platforms receiving tens of thousands of likes and reposts, I was fed up, people were *wrong* on the *internet* so I had to step in.

## ISO 8601
First of all, the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard does not use an epoch! ISO 8601 is a format for representing a date and/or time as a string of characters. In other words, it does NOT represent itself as a count of units of time after some chosen starting point (aka. [an epoch](https://en.wikipedia.org/wiki/Epoch_(computing))). Its dates are just a textual representation of a day in the Gregorian calendar (e.g. today is '2025-02-16').

In 2004 the ISO 8601 standard was updated to include a "reference date" of the day of the Metre Convention, May 20th 1875. This is certainly the source of the confusion here, but it also does not change the format of an ISO 8601 date whatsoever. If you read the [actual standard](https://web.archive.org/web/20171020084445/https://www.loc.gov/standards/datetime/ISO_DIS%208601-1.pdf) (before it was updated again in 2019 to remove this date) it's just a single sentence: 
> The Gregorian calendar has a reference point that assigns 20th May 1875 to the calendar day that the “Convention du Mètre” was signed in Paris. 

Why was that sentence added and then removed? Maybe the authors felt this was necessary to shut down some remaining Julian calendar fans who were referring to that same day as 7th May 1875. I don't know. It doesn't matter. There's still no epoch.

## COBOL
But what about the representation in COBOL? Maybe it uses the day of the Metre Convention as a default? Except it doesn't. Yes, I subjected myself to learning the basics of a programming language that was designed three and a half decades before I was born. But you see, someone was wrong on the internet.

The one thing OP gets correct is that COBOL does not have a built-in date or time type. It does however have some built-in functions that will help you use ISO 8601 dates, and will even convert them for you to an integer that counts from an epoch. But once again, that epoch is not in 1875. The epoch is configurable using the COBOL's [INTDATE](https://www.ibm.com/docs/en/cobol-zos/6.3?topic=options-intdate) option, but the only two choices are January 1st, 1601, or October 15th, 1582. This means that in theory a 0 value should default in COBOL to 1601, 424 years ago, not 150. Except even that is not right. COBOL indexes from 1 and not from 0. So really a 0 value is invalid, and just returns a 0000-00-00 representation. But don't take my word for it, here is some COBOL I wrote, and its output:

```
PROCEDURE DIVISION.
INITIALIZE WS-DATE-DATA. 
DISPLAY 'Default initialized ISO 8601 basic format:'
DISPLAY WS-DATE-DATA.
DISPLAY 'System defined current date:'
DISPLAY FUNCTION CURRENT-DATE.
INITIALIZE WS-INTEGER-DATE. 
DISPLAY 'Default initialized number:'
DISPLAY WS-INTEGER-DATE.
DISPLAY 'ISO date of the default initialized number:'
DISPLAY FUNCTION DATE-OF-INTEGER (WS-INTEGER-DATE).
DISPLAY 'ISO date on day one (1) of the epoch: '
DISPLAY FUNCTION DATE-OF-INTEGER (01).
DISPLAY 'Integer of current date (days since 1601 epoch):'
MOVE FUNCTION CURRENT-DATE (1:8) TO WS-TODAY.
COMPUTE WS-INTEGER-DATE = FUNCTION INTEGER-OF-DATE (WS-TODAY). 
DISPLAY WS-INTEGER-DATE.
STOP RUN. 
```

```
Output:

Default initialized ISO 8601 basic format:
0000000000000000
System defined current date:
2025021604532153+0000
Default initialized number:
00000000
ISO date of the default initialized number:
00000000
ISO date on day one (1) of the epoch: 
16010101
Integer of current date (days since 1601 epoch):
00154910
```

The point is, there is no way to get COBOL to give you a date in 1875 without first being supplied a representation of a date in 1875. It is not the default. It is not the epoch.


## Conclusion
Okay fine, but what if the engineers at Social Security made 1875 the default in their system or database? I mean yeah, sure, they could choose to do that. Maybe the guy that created the original database schema was just a really big fan of the Treaty of Metre.

```
CREATE TABLE SSA_RECIPIENTS
    ( SSN_NUMBER INTEGER NOT NULL PRIMARY KEY,
      FIRST_NAME VARCHAR(40),
      LAST_NAME  VARCHAR(40), 
      # WOOOOO I LOVE INTERNATIONAL STANDARDS OF WEIGHT AND MEASUREMENT!!
      BIRTHDAY   DATE WITH DEFAULT '1875-05-20') 
```
> If you're using a [DB2 database](https://www.ibmmainframer.com/db2-tutorial/db2-sql-create-table-statement/) and you omit the value after "WITH DEFAULT", the default would automatically be CURRENT-DATE. Not zero, not the epoch, not 1875.

But now we're purely speculating. In the end there's just no evidence backing any of the claims made in that original tweet. We don't even know if Elon really saw records with birthdays in 1875, and yet we're all making up a false reality where his words would make some sense. I can't speak to what's in the Social Security database, maybe there really are some people who are listed as 150 years old, but I doubt it. We don't need to be spending our time making sense of fascist misinformation that's designed to destroy our country's foundational institutions. We should be outraged that an unelected oligarch has access to peoples personal data in the first place. 

Even if it is fun to poke fun at Elon online, he is known to fall for all sorts of [obviously false](https://www.nbcnews.com/politics/doge/elon-musk-boosted-false-usaid-conspiracy-theories-global-aid-rcna190646) facts about [fraud](https://newrepublic.com/post/187311/elon-musk-pushes-deranged-conspiracy-theory-yet) or otherwise. His [minions](https://www.wired.com/story/elon-musk-government-young-engineers/) that feed him information about the vast and complex federal government that he's taken control of are mostly young, unexperienced, and untrustworthy. You shouldn't take anything he says at face value, nor random people on social media. I hope you learned something new today, I know I did.

## Notes:
If I were to poke holes in this, here's where I'd start:

 - I did not personally test out the DB2 default values for DATE types, but the documentation I referenced seems clear enough to me.
 - I did not try out every previous version of COBOL compiler to make sure the demonstrated behavior was unchanged.

For reference, here is the Working Storage Section for the program I wrote above.

```
WORKING-STORAGE SECTION.
01 WS-INTEGER-DATE   PIC 9(8).
01 WS-TODAY          PIC 9(8).
01 WS-DATE-DATA.
   05  WS-DATE.
       10  WS-YEAR         PIC 9(04).
       10  WS-MONTH        PIC 9(02).
       10  WS-DAY          PIC 9(02).
   05  WS-TIME.
       10  WS-HOURS        PIC 9(02).
       10  WS-MINUTE       PIC 9(02).
       10  WS-SECOND       PIC 9(02).
       10  WS-MILLISECONDS PIC 9(02).
```
