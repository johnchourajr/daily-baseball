#!/usr/bin/env python3
"""Builder for the rules + quotes portions of the content bank."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

RULES_SRC = "https://www.baseball-almanac.com/rulechng.shtml"

# Rule changes worth a "Rule of the Day" — chosen for surprise value.
rule_changes = [
    (1857, "A game used to end after the inning in which a team reached 21 runs. This year it became a nine-inning contest won by the higher score."),
    (1858, "Called strikes are introduced — before this, a batter could simply wait for a pitch he liked."),
    (1858, "A batter is out on a batted ball, fair or foul, if it is caught on the fly OR after one bounce."),
    (1863, "Called balls and bases on balls are introduced."),
    (1864, "The one-bounce out on fair balls is abolished; a fair ball must now be caught on the fly."),
    (1868, "Bat length is limited to 42 inches — still the limit today."),
    (1870, "The batter-runner is allowed to overrun first base."),
    (1871, "The batter is officially allowed to call for a high or low pitch (a practice since 1864)."),
    (1873, "The batter's box is introduced."),
    (1877, "Canvas bases 15 inches square are introduced, and home plate is placed in the angle formed by the first- and third-base lines."),
    (1878, "It took NINE called balls to draw a walk."),
    (1880, "A walk drops to seven called balls, and the batter no longer gets a fourth strike."),
    (1883, "Six called balls become a base on balls."),
    (1885, "One side of the bat is allowed to be flat — a rule rescinded in 1893."),
    (1887, "Four called strikes are adopted — for this season only. Walks are also recorded as hits, also for this season only."),
    (1887, "The batter is awarded first base when hit by a pitch."),
    (1887, "The strike zone is established between the shoulders and the knees."),
    (1889, "Four balls finally become a base on balls — the modern standard."),
    (1891, "Large padded mitts are allowed for catchers."),
    (1893, "The pitching box is eliminated for a rubber slab, moved from 50 feet to 60 feet 6 inches — the distance still used today."),
    (1894, "Foul bunts are classified as strikes."),
    (1895, "The infield-fly rule is adopted."),
    (1900, "Home plate changes from a square to the five-sided figure used today."),
    (1901, "Foul balls start counting as strikes until the batter has two strikes."),
    (1903, "The height of the mound is limited to 15 inches above the baselines."),
    (1908, "Pitchers are prohibited from soiling a new ball."),
    (1920, "All freak deliveries, including the spitball, are outlawed — and RBIs are added to the official score."),
    (1920, "A batter is finally credited with a home run if he wins the game in the ninth with a ball hit out of the park."),
    (1925, "The minimum home-run distance is set at 250 feet."),
    (1926, "The pitcher is allowed to use a rosin bag."),
    (1931, "A ball that bounces over the fence now entitles the batter to two bases, not a home run."),
    (1950, "The home team must bat second, and the strike zone is redefined as armpits to the top of the knees."),
    (1959, "Minimum outfield dimensions are set for all new parks: 325-400-325 feet."),
    (1968, "The anti-spitball rule is rewritten and tightened after a wave of moistened pitches the prior season."),
    (1969, "The pitcher's mound is dropped five inches and the strike zone shrunk — a direct answer to 1968's Year of the Pitcher. The save also becomes an official rule."),
    (1971, "All major-league players are ordered to wear protective helmets."),
    (1973, "The American League begins using the designated hitter — on an experimental basis."),
    (1975, "The ball is permitted to be covered with cowhide because of a shortage of horses."),
    (1988, "Catchers must wear protective helmets while on defense."),
    (2008, "Limited instant replay (home run calls, fair or foul) arrives on August 29."),
    (2014, "A runner may no longer deviate from his path to initiate contact with the catcher, and the catcher may not block the plate without the ball."),
    (2017, "Pitchers no longer throw four intentional balls to issue a walk — the manager just signals the umpire."),
    (2020, "A pitcher must face a minimum of three batters, and extra innings begin with a runner on second."),
    (2022, "The National League officially adopts the designated hitter."),
    (2023, "Bases grow from 15 to 18 inches, defensive shifts are banned, and the pitch clock arrives."),
]

rules = [{"year": y, "rule": r, "source": RULES_SRC} for y, r in rule_changes]

# The 1845 Knickerbocker Rules — the origin document.
knickerbocker = {
    "title": "The Knickerbocker Rules (1845)",
    "note": "Alexander J. Cartwright's twenty rules, adopted September 23, 1845 — the foundation of modern baseball.",
    "source": "https://www.baseball-almanac.com/rule11.shtml",
    "highlights": [
        "8TH. The game to consist of twenty-one counts, or aces; but at the conclusion an equal number of hands must be played.",
        "9TH. The ball must be pitched, not thrown, for the bat.",
        "10TH. A ball knocked out of the field, or outside the range of the first and third base, is foul.",
        "12TH. If a ball be struck, or tipped, and caught, either flying or on the first bound, it is a hand out.",
        "13TH. A player running the bases shall be out, if the ball is in the hands of an adversary on the base, or the runner is touched with it before he makes his base; it being understood, however, that in no instance is a ball to be thrown at him.",
        "15TH. Three hands out, all out.",
        "17TH. All disputes and differences relative to the game, to be decided by the Umpire, from which there is no appeal.",
    ],
}

QSRC = "https://www.baseball-almanac.com/quomenu.shtml"

def q(text, who, src=None):
    d = {"quote": text, "speaker": who, "source": QSRC}
    if src: d["cite"] = src
    return d

quotes = [
    q("Age is a case of mind over matter. If you don't mind, it don't matter.", "Satchel Paige"),
    q("How old would you be if you didn't know how old you were?", "Satchel Paige"),
    q("I never threw an illegal pitch. The trouble is, once in a while I toss one that ain't never been seen by this generation.", "Satchel Paige"),
    q("Just take the ball and throw it where you want to. Throw strikes. Home plate don't move.", "Satchel Paige"),
    q("Ain't no man can avoid being born average, but there ain't no man got to be common.", "Satchel Paige"),
    q("Managing is getting paid for home runs someone else hits.", "Casey Stengel", "The Sports Hall of Fame Encyclopedia"),
    q("Can't anybody here play this game?", "Casey Stengel"),
    q("The secret of managing is to keep the guys who hate you away from the guys who are undecided.", "Casey Stengel"),
    q("You got to get twenty-seven outs to win.", "Casey Stengel", "You Could Look It Up"),
    q("Been in this game one-hundred years, but I see new ways to lose 'em I never knew existed before.", "Casey Stengel"),
    q("He'd fall in a sewer and come up with a gold watch.", "Casey Stengel on Yogi Berra", "Baseball Digest, August 1972"),
    q("Nice guys finish last.", "Leo Durocher"),
    q("I don't care if the guy is yellow or black, or if he has stripes like a god-damn zebra. I'm the manager of this team and I say he plays.", "Leo Durocher, on Jackie Robinson"),
    q("Show me a good loser in professional sports, and I'll show you an idiot.", "Leo Durocher"),
    q("If you don't win, you're going to be fired. If you do win, you've only put off the day you're going to be fired.", "Leo Durocher"),
    q("In a year that has been so improbable, the impossible has happened.", "Vin Scully", "1988 World Series, Kirk Gibson's home run"),
    q("Statistics are used much like a drunk uses a lamp post: for support, not illumination.", "Vin Scully"),
    q("Good is not good when better is expected.", "Vin Scully"),
    q("Baseball is almost the only orderly thing in a very unorderly world. If you get three strikes, even the best lawyer in the world can't get you off.", "Bill Veeck", "Sports Illustrated, March 14, 1976"),
    q("I try not to break the rules, but merely to test their elasticity.", "Bill Veeck"),
    q("This is a game to be savored, not gulped. There's time to discuss everything between pitches or between innings.", "Bill Veeck", "Sports Illustrated, March 14, 1976"),
    q("I have discovered in twenty years of moving around a ballpark, that the knowledge of the game is usually in inverse proportion to the price of the seats.", "Bill Veeck"),
    q("It breaks your heart. It is designed to break your heart.", "A. Bartlett Giamatti", "The Green Fields of the Mind, November 1977"),
    q("On matters of race, on matters of decency, baseball should lead the way.", "A. Bartlett Giamatti", "Hartford Courant, April 15, 1984"),
    q("People will say I'm an idealist. I hope so.", "A. Bartlett Giamatti", "Pete Rose banishment speech"),
    # --- on statistics (baseball-almanac.com/quotes/stats5.shtml) ---
    q("Statistics are the lifeblood of baseball.", "Leonard Koppett", "A Thinking Man's Guide to Baseball, 1967"),
    q("A baseball fan has the digestive apparatus of a billy goat. He can, and does, devour any set of statistics with insatiable appetite and then nuzzles hungrily for more.", "Arthur Daley"),
    q("Baseball fans are junkies, and their heroin is the statistic.", "Robert S. Weider", "In Praise of the Second Season, 1981"),
    q("Baseball isn't statistics — baseball is Joe DiMaggio rounding second.", "Jimmy Breslin"),
    q("A passion for statistics is the earmark of a literate people.", "Paul Fisher"),
    q("I really don't care much about baseball, or looking at ball games. All my interest in baseball is in its statistics.", "Ernest J. Lanigan", "The Baseball Cyclopedia, 1922"),
    q("If you dwell on statistics, you get shortsighted. If you aim for consistency, the numbers will be there at the end.", "Tom Seaver"),
    q("They both show a lot, but not everything.", "Toby Harrah, on statistics and bikinis"),
    q("Baseball is probably the world's best documented sport.", "Ford C. Frick", "Games, Asterisks and People, 1973"),
    q("Anybody with a pencil could be a statistician back then.", "Seymour Siwoff, Elias Sports Bureau, on the 19th century"),
]

def dump(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"wrote data/{name}")

dump("rules.json", {"_source": RULES_SRC,
                    "_note": "Rule-change timeline entries chosen for trivia value, plus the 1845 Knickerbocker Rules.",
                    "rule_changes": rules,
                    "knickerbocker_1845": knickerbocker})
dump("quotes.json", {"_source": QSRC,
                     "_note": "Curated quotes from baseball-almanac quote pages.",
                     "quotes": quotes})
print(f"TOTAL rule changes: {len(rules)} | quotes: {len(quotes)}")
