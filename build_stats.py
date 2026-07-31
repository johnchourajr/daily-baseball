#!/usr/bin/env python3
"""Builder for the expanded stats bank.

Every number here was hand-checked before being written. The site's auto-summarizer
demonstrably drifts on record totals (it reported Babe Ruth at 708 career home runs
— the real figure is 714 — and mis-ordered the single-season home run list), so
scraped figures are treated as leads, not facts. Anything that could not be
confirmed, or that postdates a verifiable source, was left out rather than guessed.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RB = "https://www.baseball-almanac.com/rb_menu.shtml"


def s(fact, category, source=RB):
    return {"fact": fact, "category": category, "verified": True, "source": source}


stats = [
    # ---------------- home runs ----------------
    s("Barry Bonds holds the career home run record with 762.", "home runs"),
    s("Hank Aaron hit 755 career home runs, the record from 1974 until 2007.", "home runs"),
    s("Babe Ruth finished his career with 714 home runs.", "home runs"),
    s("Albert Pujols retired with 703 home runs, the fourth-highest total in history.", "home runs"),
    s("Willie Mays hit 660 career home runs.", "home runs"),
    s("Barry Bonds holds the single-season home run record with 73, set in 2001.", "home runs"),
    s("Mark McGwire hit 70 home runs in 1998, breaking a record that had stood since 1961.", "home runs"),
    s("Sammy Sosa hit 60 or more home runs in three different seasons — and never once led the league.", "home runs"),
    s("Roger Maris hit 61 home runs in 1961, breaking Babe Ruth's 34-year-old record of 60.", "home runs"),
    s("Aaron Judge hit 62 home runs in 2022, the American League record.", "home runs"),
    s("Mike Schmidt hit 509 home runs as a third baseman, the most at the position.", "home runs"),

    # ---------------- hitting ----------------
    s("Pete Rose is the all-time hits leader with 4,256.", "hitting"),
    s("Ty Cobb collected 4,189 career hits, a record that stood for over 50 years.", "hitting"),
    s("Ichiro Suzuki collected 262 hits in 2004, the most in a single season.", "hitting"),
    s("Ty Cobb's career batting average of .366 is the highest in MLB history.", "hitting"),
    s("Rogers Hornsby batted .424 in 1924 — and averaged .402 across the five seasons from 1921 to 1925.", "hitting"),
    s("Hugh Duffy batted .440 in 1894, the highest single-season average ever recorded.", "hitting"),
    s("Nap Lajoie hit .426 in 1901, the American League record.", "hitting"),
    s("Ted Williams hit .406 in 1941 — no one has hit .400 since.", "hitting"),
    s("Hank Aaron drove in 2,297 runs, the most in MLB history.", "hitting"),
    s("Hack Wilson drove in 191 runs in 1930, a single-season record that still stands.", "hitting"),
    s("Jim Bottomley (1924) and Mark Whiten (1993) share the single-game record with 12 RBIs.", "hitting"),
    s("Johnny Burnett got nine hits in one game for Cleveland in 1932 — it took 18 innings.", "hitting"),

    # ---------------- streaks ----------------
    s("Joe DiMaggio's 56-game hitting streak in 1941 is the longest in MLB history.", "streaks"),
    s("Willie Keeler (1897) and Pete Rose (1978) share the second-longest hitting streak at 44 games.", "streaks"),
    s("George Sisler hit safely in 41 straight games in 1922.", "streaks"),
    s("Benito Santiago hit in 34 straight games as a rookie in 1987.", "streaks"),
    s("Cal Ripken Jr. played in 2,632 consecutive games, breaking Lou Gehrig's 'unbreakable' 2,130.", "streaks"),
    s("Carl Hubbell won 24 consecutive decisions across the 1936 and 1937 seasons.", "streaks"),

    # ---------------- baserunning ----------------
    s("Rickey Henderson stole 1,406 bases — the all-time record, nearly 500 ahead of second place.", "baserunning"),
    s("Rickey Henderson stole 130 bases in 1982, the modern single-season record.", "baserunning"),
    s("Rickey Henderson scored 2,295 runs, the most in MLB history.", "baserunning"),
    s("Lou Brock ranks second all-time with 938 career stolen bases, and stole 118 in 1974.", "baserunning"),
    s("Vince Coleman once stole 50 consecutive bases without being caught.", "baserunning"),

    # ---------------- pitching ----------------
    s("Cy Young won 511 games, the most in MLB history — and lost 315, also a record.", "pitching"),
    s("Walter Johnson won 417 games, the most of any pitcher since 1900.", "pitching"),
    s("Warren Spahn won 363 games, the most by a left-hander.", "pitching"),
    s("Old Hoss Radbourn won 59 games in 1884 — pitching, by some accounts, nearly every game down the stretch.", "pitching"),
    s("Jack Chesbro won 41 games in 1904, the modern single-season record.", "pitching"),
    s("Nolan Ryan struck out 5,714 batters, the all-time record — over 800 more than anyone else.", "pitching"),
    s("Randy Johnson struck out 4,875 batters, the most by a left-hander.", "pitching"),
    s("Nolan Ryan struck out 383 batters in 1973, the modern single-season record.", "pitching"),
    s("Twenty strikeouts is the nine-inning game record, done by Roger Clemens (twice), Kerry Wood, and Max Scherzer.", "pitching"),
    s("Tom Cheney struck out 21 batters in a 16-inning game in 1962 — the most in any game.", "pitching"),
    s("Nolan Ryan threw a record seven no-hitters.", "pitching"),
    s("Johnny Vander Meer is the only pitcher ever to throw back-to-back no-hitters, in June 1938.", "pitching"),
    s("Mariano Rivera saved 652 games, the most in MLB history.", "pitching"),
    s("Trevor Hoffman saved 601 games, second-most all time.", "pitching"),
    s("Francisco Rodriguez saved 62 games in 2008, the single-season record.", "pitching"),
    s("Mariano Rivera threw 33 1/3 consecutive scoreless postseason innings.", "pitching"),

    # ---------------- oddities ----------------
    s("Joe Nuxhall pitched in the majors at 15 years, 10 months and 11 days old — the youngest player ever.", "oddities"),
    s("Satchel Paige pitched a major league game at 59 years old, in 1965.", "oddities"),
    s("Nolan Ryan played 27 seasons, the most of any player.", "oddities"),
    s("Nolan Ryan was clocked at 100.9 mph in 1974 — a Guinness record at the time.", "oddities"),
    s("Evar Swanson circled the bases in 13.3 seconds in 1932, averaging 18.45 mph.", "oddities"),
    s("Glen Gorbous threw a baseball 445 feet 10 inches in 1957, the longest throw on record.", "oddities"),
    s("A 1956 exhibition game in Melbourne, Australia drew 114,000 spectators — the largest crowd ever for a baseball game.", "oddities"),
    s("Bob Meusel, Babe Herman, Adrian Beltre, Trea Turner and Christian Yelich each hit for the cycle three times.", "oddities"),
    s("In a two-week span in 1933, three Philadelphia Athletics — Mickey Cochrane, Jimmie Foxx and Pinky Higgins — each hit for the cycle.", "oddities"),
    s("Mike Trout hit for the cycle at 21 years, 288 days; Mel Ott did it at just 20.", "oddities"),
]

out = {
    "_source": RB,
    "_note": ("Hand-verified record nuggets. The site's auto-summarizer drifts on numbers "
              "(it reported Ruth at 708 career HR — actually 714), so every figure here was "
              "checked before inclusion and anything unconfirmable was omitted."),
    "_categories": sorted({x["category"] for x in stats}),
    "stats": stats,
}

with open(os.path.join(DATA, "stats.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

from collections import Counter
c = Counter(x["category"] for x in stats)
print(f"wrote data/stats.json — {len(stats)} verified stats")
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")
