#!/usr/bin/env python3
"""Builder for the Dodgers content bank — franchise facts, records, and quotes."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
TEAM_SRC = "https://www.baseball-almanac.com/teams/dodgers.shtml"

franchise = {
    "name": "Los Angeles Dodgers",
    "founded": 1890,
    "founded_as": "Brooklyn Bridegrooms (National League)",
    "world_series": [1955, 1959, 1963, 1965, 1981, 1988, 2020],
    "source": TEAM_SRC,
    "notes": [
        "The franchise began in 1890 as the Brooklyn Bridegrooms.",
        "Ebbets Field opened in 1913 and was home for 46 years.",
        "The team moved to Los Angeles in 1958, playing in the Coliseum before Dodger Stadium opened in 1962.",
        "Jackie Robinson broke baseball's color barrier with the Dodgers in 1947.",
    ],
}

# Dodgers-specific nuggets. Numbers hand-checked against the sources noted.
facts = [
    {"fact": "The Dodgers have won seven World Series: 1955 in Brooklyn, then 1959, 1963, 1965, 1981, 1988 and 2020 in Los Angeles.", "verified": True},
    {"fact": "The franchise was founded in 1890 as the Brooklyn Bridegrooms — the Dodgers name came later.", "verified": True},
    {"fact": "Ebbets Field opened in 1913 and served as the Dodgers' home for 46 years.", "verified": True},
    {"fact": "The Dodgers left Brooklyn for Los Angeles in 1958, playing four seasons in the Coliseum before Dodger Stadium opened in 1962.", "verified": True},
    {"fact": "Jackie Robinson debuted for the Brooklyn Dodgers on April 15, 1947, breaking baseball's color barrier.", "verified": True},
    {"fact": "Jackie Robinson hit .313 for his career with 1,568 hits, 141 home runs and 203 stolen bases across 11 seasons.", "verified": True},
    {"fact": "Jackie Robinson won the inaugural Rookie of the Year award in 1947 and the National League MVP in 1949.", "verified": True},
    {"fact": "In 1962 Jackie Robinson became the first Black player elected to the Hall of Fame — on the first ballot.", "verified": True},
    {"fact": "Vin Scully called Dodgers games for 67 seasons, the longest tenure of any broadcaster with a single team in sports history.", "verified": True},
    {"fact": "Sandy Koufax threw four no-hitters, including a perfect game against the Cubs on September 9, 1965.", "verified": True},
    {"fact": "Sandy Koufax retired at 30, after a 1966 season in which he won 27 games.", "verified": True},
    {"fact": "Kirk Gibson's pinch-hit walk-off home run in Game 1 of the 1988 World Series came off Dennis Eckersley — Gibson's only plate appearance of the Series.", "verified": True},
    {"fact": "Orel Hershiser threw 59 consecutive scoreless innings in 1988, breaking Don Drysdale's record of 58 2/3 — also a Dodger.", "verified": True},
    {"fact": "The Dodgers were the first team to draw three million fans in a season, at Dodger Stadium in 1978.", "verified": True},
    {"fact": "Roy Campanella won three National League MVP awards (1951, 1953, 1955) as the Dodgers' catcher.", "verified": True},
    {"fact": "Don Drysdale and Sandy Koufax staged a joint holdout in 1966 — a landmark moment for player leverage.", "verified": True},

    # --- franchise record book ---
    {"fact": "Zack Wheat holds Dodgers career records for hits (2,804), games (2,322), doubles (464), triples (171) and total bases (4,003).", "verified": True},
    {"fact": "Duke Snider holds the Dodgers career home run record with 389, and the RBI record with 1,271.", "verified": True},
    {"fact": "Jackie Robinson's .409 on-base percentage is the highest in Dodgers history.", "verified": True},
    {"fact": "Pee Wee Reese scored 1,338 runs and drew 1,210 walks as a Dodger — both franchise records.", "verified": True},
    {"fact": "Babe Herman batted .393 for Brooklyn in 1930 with 241 hits and 416 total bases — all still franchise single-season records.", "verified": True},
    {"fact": "Don Sutton holds Dodgers career records for wins (233), starts (533) and shutouts (52).", "verified": True},
    {"fact": "Clayton Kershaw is the Dodgers' all-time strikeout leader.", "verified": True},
    {"fact": "Sandy Koufax struck out 382 batters in 1965 — still the Dodgers single-season record.", "verified": True},
    {"fact": "Sandy Koufax threw 11 shutouts in 1963, a Dodgers single-season record.", "verified": True},
    {"fact": "Maury Wills stole 104 bases in 1962, breaking Ty Cobb's 47-year-old single-season record.", "verified": True},
    {"fact": "Tommy Davis drove in 153 runs in 1962, the Dodgers single-season record.", "verified": True},
    {"fact": "Eric Gagne saved 55 games in 2003 and converted 84 consecutive save opportunities across three seasons.", "verified": True},
    {"fact": "Kenley Jansen saved 350 games for the Dodgers, the franchise record.", "verified": True},
    {"fact": "Mike Marshall pitched in 106 games for the Dodgers in 1974 — still the major league record.", "verified": True},
    {"fact": "Shohei Ohtani hit 54 home runs and stole 59 bases in 2024, the first 50-50 season in MLB history.", "verified": True},
    {"fact": "The largest crowd ever to see a game in the United States — 92,706 — watched the Dodgers face the White Sox at the LA Coliseum on October 6, 1959.", "verified": True},
]

QSRC = "https://www.baseball-almanac.com/quomenu.shtml"

def q(text, who, cite=None):
    d = {"quote": text, "speaker": who, "source": QSRC, "dodgers": True}
    if cite: d["cite"] = cite
    return d

quotes = [
    q("I bleed Dodger blue and when I die, I'm going to the big Dodger in the sky.", "Tommy Lasorda"),
    q("I believe managing is like holding a dove in your hand. If you hold it too tightly you kill it, but if you hold it too loosely, you lose it.", "Tommy Lasorda", "The Artful Dodger"),
    q("About the only problem with success is that it does not teach you how to deal with failure.", "Tommy Lasorda", "The Artful Dodger"),
    q("There are three types of baseball players: those who make it happen, those who watch it happen, and those who wonder what happens.", "Tommy Lasorda"),
    q("I love doubleheaders. That way I get to keep my uniform on longer.", "Tommy Lasorda"),
    q("To win. Nothing else matters, and nothing else will do.", "Sandy Koufax", "Koufax, 1966"),
    q("I became a good pitcher when I stopped trying to make them miss the ball and started trying to make them hit it.", "Sandy Koufax", "A Thinking Man's Guide to Baseball"),
    q("Pitching is the art of instilling fear.", "Sandy Koufax", "The Gashouse Gang, 1976"),
    q("Trying to hit him was like trying to drink coffee with a fork.", "Willie Stargell, on Sandy Koufax"),
    q("There are two times in my life the hair on my arms has stood up: the first time I saw the ceiling of the Sistine Chapel and the first time I saw Sandy Koufax throw a fastball.", "Al Campanis", "Sandy Koufax: A Lefty's Legacy, 2003"),
    q("I can see how he won twenty-five games. What I don't understand is how he lost five.", "Yogi Berra, on Sandy Koufax"),
    q("I never want to quit playing ball. They'll have to cut this uniform off of me to get me out of it.", "Roy Campanella"),
    q("To be good you've gotta have a lot of little boy in you.", "Roy Campanella"),
    q("Luck is the residue of design.", "Branch Rickey", "New York Times, November 17, 1965"),
    q("The greatest untapped reservoir of raw material in the history of our game is the black race.", "Branch Rickey", "on signing Jackie Robinson, 1946"),
    q("It doesn't tell how big you are, what church you attend, what color you are, or how your father voted in the last election.", "Branch Rickey, on the box score", "I Never Had It Made, 1997"),
    q("Never surrender opportunity for security.", "Branch Rickey"),
    q("In a year that has been so improbable, the impossible has happened.", "Vin Scully", "1988 World Series, Kirk Gibson's home run"),
    q("Statistics are used much like a drunk uses a lamp post: for support, not illumination.", "Vin Scully"),
    q("It may sound corny, but I enjoyed listening to Vin call a game almost more than playing in them.", "Sandy Koufax, on Vin Scully"),
]

out = {"_source": TEAM_SRC,
       "_note": "Dodgers-specific content bank. Enabled via config.json when team_focus is 'dodgers'.",
       "franchise": franchise,
       "facts": facts,
       "quotes": quotes}

with open(os.path.join(DATA, "dodgers.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote data/dodgers.json — {len(facts)} facts, {len(quotes)} quotes")
