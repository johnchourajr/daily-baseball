#!/usr/bin/env python3
"""One-off builder that emits the curated content bank as JSON.
Run once to (re)generate data/*.json. Definitions are faithful condensations
of baseball-almanac.com/Dickson Baseball Dictionary entries, each with a
source URL for provenance.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SRC = "https://www.baseball-almanac.com/dictionary-term.php?term="

def t(term, definition, first_use=None, origin=None):
    d = {"term": term, "def": definition, "source": SRC + term.replace(" ", "%20")}
    if first_use: d["first_use"] = first_use
    if origin: d["origin"] = origin
    return d

terms = [
    # --- original hand-curated six ---
    t("Can of corn", "An easily caught, high lazy fly ball that lets a fielder camp under it.",
      "1926", "May trace to grocery clerks tipping canned goods off high shelves with a pole to catch them."),
    t("Baltimore chop", "A ball chopped down near the plate that bounces so high the batter can beat it out for a hit.",
      None, "Named for the 1890s Baltimore Orioles, whose hard-baked infield made the bounce a weapon."),
    t("Texas Leaguer", "A cheap hit that loops just over the infielders but drops in front of the outfielders.",
      "1892", "H.L. Mencken called it 'a pop fly which nevertheless takes the batter to first base.'"),
    t("Southpaw", "A left-handed pitcher or thrower.",
      "1869", "By 1889 it had settled specifically onto lefty pitchers."),
    t("Rhubarb", "A noisy on-field argument or ruckus with the umpires.",
      None, "Broadcaster Red Barber popularized it in the late 1930s and '40s."),
    t("Bullpen", "The area where relief pitchers warm up during a game — and, by extension, a team's whole relief staff.",
      None, None),
    # --- scraped additions ---
    t("Ace", "A team's best pitcher, usually a starter and the rock of the rotation. (Earliest sense: a run or score in 1840s baseball.)",
      "1902", "Tradition credits pitcher Asa 'Acey' Brainard, who won 56 of 57 games for the 1869 Red Stockings."),
    t("Dinger", "A home run.",
      "1974", "Probably from 'humdinger' — something of remarkable excellence."),
    t("Tater", "A home run.",
      None, "May have started in the Negro leagues as 'potato'; George Scott popularized 'taters' with the 1966 Red Sox."),
    t("Dying quail", "A pop fly that drops suddenly, like a bird shot on the wing, often falling between fielders for a hit.",
      "1947", "Sportswriter usage for a blooper; syn. quail, dying swan."),
    t("Frozen rope", "A hard-hit line drive on a rigid, low, straight path that seems to defy gravity.",
      "1938", "'You could hang a week's wash on it,' per broadcaster Red Rush; syn. rope, clothesline."),
    t("Gopher ball", "A pitch destined to be hit for a home run — one that will 'go for' extra bases.",
      "1930", "From 'go fer' (go for two, three...); Lefty Gomez is credited by some with coining it."),
    t("Hot corner", "Third base.",
      "1889", "Coined by writer Ren Mulford after Reds 3B Hick Carpenter fielded seven sharp drives that 'almost tore him apart.'"),
    t("Moon shot", "A home run, especially one hit a very long distance.",
      "1959", "Popularized alongside the era's space program; early use described Harmon Killebrew's blasts."),
    t("Pepper", "A fast, close-range pregame drill where a batter taps quick grounders to a cluster of fielders who fire the ball right back.",
      "1914", "From 'pep' — the peppy, rapid-fire nature of the drill."),
    t("Seeing-eye single", "A softly hit single that sneaks through the infield as if the ball had eyes.",
      None, "Syn. ball with eyes on it."),
    t("Shoestring catch", "A running catch made at the fielder's shoe tops, just before the ball hits the ground.",
      "1904", None),
    t("Twin killing", "A double play.",
      "1920", None),
    t("Wheelhouse", "The part of the strike zone where a batter swings with the most power; hang a pitch there and invite a home run.",
      "1959", "From batters 'wheeling' at the ball; also the nautical pilothouse from which a ship is steered."),
    t("Cup of coffee", "A brief trial in the major leagues by a minor-league player — figuratively, just long enough to drink a cup of coffee.",
      "1908", None),
    t("Uncle Charlie", "A curveball, especially a big sweeping one.",
      "1933", "The two words may onomatopoetically suggest a curve; see also Lord Charles, Sir Charles."),
    t("Cheese", "A fastball. 'High cheese' is one up and in.",
      "1975", "From old slang where 'cheese' meant the best thing of its kind; also gives us 'the big cheese.'"),
    t("Chin music", "A brushback pitch thrown so high and inside the batter can supposedly hear it buzz past his jaw.",
      "1867", "Older slang for idle chatter, dating to the 1820s."),
    t("Circus catch", "A spectacular catch — a jump, dive, flip, or roll — suggesting a circus acrobat.",
      "1878", "Cubs OF 'Circus Solly' Hofman was named for his acrobatic grabs; syn. showboat catch."),
    t("Cellar", "Last place — the position held by the team with the worst record.",
      "1907", "Syn. basement, pit."),
    t("Closer", "The relief pitcher used to get the final outs and protect a late lead.",
      "1977", "Cubs manager Herman Franks invented the modern role using Bruce Sutter only with an 8th/9th-inning lead."),
    t("Crooked number", "Any inning total greater than one — so called for the curves in the numerals 2 through 9.",
      "1978", "A 1-0 game is one in which neither team posted a crooked number."),
    t("Ducks on the pond", "Baserunners waiting to be driven home.",
      "1921", "Brought to baseball by Senators broadcaster Arch McDonald."),
    t("Golden sombrero", "The dubious mark for striking out four times in a single game.",
      "1979", "Three K's is a hat trick; four earns a 'sombrero' (bigger than a hat); five is the 'platinum sombrero.'"),
    t("Mendoza Line", "The .200 batting-average threshold separating adequate hitters from the rest.",
      "1982", "Named for shortstop Mario Mendoza (career .215); popularized by George Brett."),
    t("Meatball", "An easy-to-hit pitch served right down the middle.",
      "1912", "A refashioning of 'meet the ball'; syn. meat."),
    t("Immaculate inning", "A half-inning in which a pitcher strikes out all three batters on exactly nine pitches.",
      "2008", "There were none from 1929–52 — but seven in 2022 alone."),
    t("Warning track", "The dirt or cinder strip inside the outfield wall that warns a fielder, by feel underfoot, that the wall is near.",
      None, "Conceived after Pete Reiser was badly hurt crashing into Ebbets Field's wall in 1947."),
    t("Worm burner", "A ball hit so hard and low it skids across the ground without bouncing.",
      None, "Syn. worm killer."),
    t("Pickle", "A rundown — a baserunner trapped between two bases with fielders closing in. (Also, as a verb, to hit a ball very hard.)",
      "1908", "Short for 'in a pickle.'"),
    t("Bandbox", "A ballpark whose small dimensions make home runs easy — John Updike's 'lyric little green bandbox' was Fenway.",
      "1894", "After the small-town bandstands common at the turn of the century; syn. crackerbox."),
    t("Submariner", "A pitcher who throws with an underhand, submarine-style delivery.",
      None, "Syn. subway slinger; Carl Mays was the most infamous."),
    t("Payoff pitch", "The pitch thrown on a full count (3-2) — barring a foul, it decides the at-bat.",
      None, "Syn. decision pitch."),
    t("Spitball", "A late-breaking pitch thrown off a ball loaded with saliva, banned in 1920 for hygiene and to boost offense.",
      "1902", "Grandfathered pitchers could keep throwing it; the last legal one was Burleigh Grimes, retired 1934."),
    t("Knuckleball", "A slow pitch thrown with almost no spin so it flutters, darts, and dips unpredictably — sometimes moving 11 inches.",
      "1907", "Perfected by Hoyt Wilhelm, Phil Niekro, and Charlie Hough."),
    t("Screwball", "A pitch that breaks the opposite way from a curveball, thrown with an inward twist of the wrist. (Also: a zany player.)",
      "1921", "Made famous by Christy Mathewson's 'fadeaway' and later Carl Hubbell."),
]

# Verified stats (numbers hand-checked; historical records that do not change).
stats = [
    {"fact": "Barry Bonds holds the career home run record with 762.", "verified": True},
    {"fact": "Hank Aaron hit 755 career home runs, the record from 1974 until 2007.", "verified": True},
    {"fact": "Babe Ruth finished his career with 714 home runs.", "verified": True},
    {"fact": "Barry Bonds holds the single-season home run record with 73, set in 2001.", "verified": True},
    {"fact": "Pete Rose is the all-time hits leader with 4,256.", "verified": True},
    {"fact": "Ty Cobb collected 4,189 career hits, a record that stood for over 50 years.", "verified": True},
    {"fact": "Rickey Henderson stole 1,406 bases — the all-time record, nearly 500 ahead of second place.", "verified": True},
    {"fact": "Rickey Henderson scored 2,295 runs, the most in MLB history.", "verified": True},
    {"fact": "Lou Brock ranks second all-time with 938 career stolen bases.", "verified": True},
    {"fact": "Joe DiMaggio's 56-game hitting streak in 1941 is the longest in MLB history.", "verified": True},
    {"fact": "Willie Keeler (1897) and Pete Rose (1978) share the second-longest hitting streak at 44 games.", "verified": True},
    {"fact": "George Sisler hit safely in 41 straight games in 1922.", "verified": True},
    {"fact": "Cy Young won 511 games, the most in MLB history — and lost 315, also a record.", "verified": True},
    {"fact": "Nolan Ryan struck out 5,714 batters, the all-time record.", "verified": True},
    {"fact": "Nolan Ryan threw a record seven no-hitters.", "verified": True},
    {"fact": "Cal Ripken Jr. played in 2,632 consecutive games, breaking Lou Gehrig's 'unbreakable' 2,130.", "verified": True},
]

# Stat abbreviations glossary (from baseball-almanac.com/stats4.shtml).
abbreviations = {
    "_source": "https://www.baseball-almanac.com/stats4.shtml",
    "offensive": {
        "AB": "At Bats", "BB": "Bases on Balls (Walks)", "AVG": "Batting Average",
        "CS": "Caught Stealing", "2B": "Doubles", "GIDP": "Ground into Double Plays",
        "GRSL": "Grand Slams", "HBP": "Hit by Pitch", "H": "Hits", "HRR": "Home Run Ratio",
        "HR": "Home Runs", "IBB": "Intentional Walks", "ISO": "Isolated Power",
        "LOB": "Left on Base", "OBP": "On-Base Percentage", "OPS": "On-Base Plus Slugging",
        "R": "Runs", "RBI": "Runs Batted In", "SF": "Sacrifice Flies",
        "SH": "Sacrifice Hits (Bunts)", "S": "Singles", "SLG": "Slugging Percentage",
        "SB%": "Stolen Base Percentage", "SBR": "Stolen Base Runs", "SB": "Stolen Bases",
        "SO": "Strikeouts", "TB": "Total Bases", "3B": "Triples"
    },
    "pitching": {
        "AO": "Fly Outs (Air)", "BB": "Walks (Bases on Balls)", "BFP": "Batters Facing Pitcher",
        "BK": "Balks", "CBO": "Combined Shutout", "CG": "Complete Games", "CGL": "Complete Game Losses",
        "ER": "Earned Runs", "ERA": "Earned Run Average", "GF": "Games Finished", "GO": "Ground Outs",
        "GOAO": "Ground Outs / Fly Outs Ratio", "GP": "Games Played", "GS": "Games Started",
        "H": "Hits", "HBP": "Hit Batters", "HR": "Home Runs", "IBB": "Intentional Walks",
        "IP": "Innings Pitched", "IRA": "Inherited Runs Allowed", "IPS": "Innings Per Start",
        "L": "Losses", "MB9": "Baserunners Per 9 Innings", "OBA": "Opponents' Batting Average",
        "PA": "Plate Appearances", "R": "Runs", "RPF": "Relief Failures", "RW": "Relief Wins",
        "S/SHO": "Shutouts", "SO": "Strikeouts", "SV": "Saves", "SVO": "Save Opportunities",
        "TB": "Total Bases", "W": "Wins", "WP": "Wild Pitches"
    },
    "defensive": {
        "A": "Assists", "CS": "Caught Stealing", "DP": "Double Plays", "E": "Errors",
        "GP": "Games Played", "OFA": "Outfield Assists", "PB": "Passed Balls", "PK": "Pickoffs",
        "PO": "Putouts", "SB": "Stolen Bases", "TC": "Total Chances", "TP": "Triple Plays"
    },
    "misc": {"ML SER": "Major League Service"}
}

def dump(name, obj):
    with open(os.path.join(DATA, name), "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"wrote data/{name} ({len(json.dumps(obj))} bytes)")

dump("terms.json", {"_source": "https://www.baseball-almanac.com/dictionary.php",
                    "_note": "Curated pool from the Dickson Baseball Dictionary via baseball-almanac.com. Faithful condensations for daily use; each entry links its source.",
                    "terms": terms})
dump("stats.json", {"_note": "Human-verified record nuggets. Numbers hand-checked, not auto-scraped (the scraper's summarizer misreported some totals). These are stable historical records.",
                    "stats": stats})
dump("abbreviations.json", abbreviations)

# History seed (July 31), kept per-date; the daily task fetches missing dates live.
hist_0731 = {
    "date": "07-31",
    "events": [
        "1954 — Joe Adcock hit four home runs and a double; his 18 total bases set a new Major League record as the Braves beat the Dodgers 15-7.",
        "1978 — Pete Rose singled to extend his hitting streak to 44 games, tying Willie Keeler's 81-year-old National League record.",
        "1961 — The All-Star Game ended in a 1-1 tie at Fenway Park, called for heavy rain — the only tie in All-Star history.",
        "1930 — Lou Gehrig drove in eight runs with a grand slam and two doubles as the Yankees edged the Red Sox 14-13.",
        "1988 — Jose Canseco homered twice to become the first player with 30+ home runs in each of his first three seasons."
    ],
    "source": "https://www.baseball-almanac.com/history/today.php?d=07-31"
}
with open(os.path.join(DATA, "history", "07-31.json"), "w") as f:
    json.dump(hist_0731, f, indent=2, ensure_ascii=False)
print("wrote data/history/07-31.json")
print(f"TOTAL terms: {len(terms)} | stats: {len(stats)}")
