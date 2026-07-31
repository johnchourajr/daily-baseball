# ⚾ Daily Baseball

A daily fun-facts email from the baseball archives: *This Day in Baseball History*,
a *Term of the Day* from the game's slang dictionary, a verified *By the Numbers*
record, a *Rule Change* from the game's 180-year rulebook, and a closing quote.
Sourced from [baseball-almanac.com](https://www.baseball-almanac.com) and the
Dickson Baseball Dictionary.

The content is **pre-stored**, so producing a day's email is a fast local lookup
with no scraping in the hot path — the piece that makes it dependable enough to ship.

## Layout

```
daily-baseball/
├── config.json               # team focus + how often team content appears
├── data/                     # the content bank (pre-stored, versioned)
│   ├── terms.json            #   41 slang terms with etymology + first-use year
│   ├── dictionary_index.json #   the FULL A-Z term index (~12k terms) + definition URLs
│   ├── stats.json            #   60 hand-verified records, categorized
│   ├── rules.json            #   45 rule changes (1857–2023) + the 1845 Knickerbocker Rules
│   ├── quotes.json           #   35 curated quotes
│   ├── dodgers.json          #   team bank: 32 franchise records, 20 quotes
│   ├── formulas.json         #   stat definitions + formulas (OPS, ERA, WHIP, ZR, ...)
│   ├── abbreviations.json    #   stat-abbreviation glossary (AB, OPS, ERA, ...)
│   ├── _index_raw/           #   raw scraped letter lists the index is built from
│   └── history/              #   one file per date (MM-DD.json); fills in over time
├── src/dailyball/
│   ├── content.py            #   loaders, no-repeat rotation, team mixing
│   └── generate.py           #   builds the HTML + plain-text email
├── templates/email.html      # the email layout
├── automation/               # the scheduled-task prompt
├── output/                   # generated emails + rotation state (git-ignored)
├── build_*.py                # one-off builders that regenerate data/*.json
└── pyproject.toml            # installable as `dailyball`
```

## Run it

```bash
PYTHONPATH=src python3 -m dailyball.generate --date 07-31
# or, installed:  pip install -e .  &&  dailyball --date 07-31
```

Outputs `output/email_<date>.html` and `.txt`.

## The dictionary index

`data/dictionary_index.json` holds the complete A-Z vocabulary — every term name in
Baseball Almanac's dictionary, each with the URL of its definition page. Look one up:

```python
from dailyball import content
content.lookup_term("curve")     # -> [{'term': 'curve', 'url': ...}, ...]
```

The daily email draws its *defined* terms from the curated `terms.json` pool; the index
is the full surface area to pull from when extending it.

Coverage caveat: the B and S letter pages truncated during scraping, so those two are
flagged `partial` in the file (complete through "breezer" and "stonewall"). Re-fetching
their tails returned hallucinated generic English words rather than page content, so
that output was discarded rather than stored — better a flagged gap than fake data.

## Team focus

`config.json` mixes a team bank into the league-wide rotation:

```json
{ "team_focus": "dodgers", "team_bias": 0.5 }
```

`team_bias` is the share of days the *By the Numbers* and quote slots pull from
`data/dodgers.json` — `0.5` means roughly every other day is Dodgers content, `1.0`
is Dodgers-only, `0` turns it off. Adding another team is just another
`data/<team>.json` in the same shape.

## Rotation

`output/.rotation_state.json` tracks what's been used, so a term, stat, rule, or
quote won't repeat until its pool has fully cycled. Each pool rotates
independently, and the team pools rotate separately from the league-wide ones.

## How delivery works — and why the task is self-contained

Scheduled Cowork tasks run in Anthropic's cloud with **no bridge to your Mac**. A
task prompt that points at this repo can never work: `data/` and the generator only
exist locally, so every run fails with "path does not exist". That is by design, not
an outage, and a local cron isn't the fix either — it only fires when the Mac is
awake, online and logged in.

So the scheduled task carries its own copy of the bank. `build_task_prompt.py` reads
`data/` and emits `automation/daily_task_prompt.txt` — a fully self-contained prompt
with the rotation pools inlined. The only live call it makes is the daily history
fetch. Regenerate it after changing `data/`, then paste it into the scheduled task.

Rotation there needs no state file: the task computes N = day of the year and indexes
each pool with `N mod len`. Pools of different lengths keep the daily mix varied, and
each one cycles without repeating.

Delivery is the task's **completion notification** — the finished email is the run's
final message, so it lands in your inbox as-is. No Gmail draft: the connected Gmail
can only draft, never send, so drafts would just pile up unread.

## Local generation

A scheduled Cowork task (see `automation/daily_task_prompt.txt`) runs each morning:
it resolves the day's history (from `data/history/` or a one-time live fetch that it
then archives), runs the generator, drafts the email to Gmail, and emits the plain
text so it rides along in the task notification.

## Accuracy

Record **numbers** are the easy thing to get wrong. Scraping the record book a second
time reproduced the bug exactly: the summarizer again reported Babe Ruth at 708 career
home runs (it's 714) and returned a mis-ordered single-season home run list. So scraped
figures are treated as *leads, not facts* — every number in `stats.json` and
`dodgers.json` was hand-checked before inclusion, and anything unconfirmable was left
out rather than guessed. Term definitions are faithful condensations of their source
pages, each carrying a `source` URL.

Stats are categorized (`home runs`, `hitting`, `streaks`, `baserunning`, `pitching`,
`oddities`) so the pool can be filtered or weighted later without re-scraping.

## Extend the bank

Add entries to the relevant `build_*.py` and re-run it, or append directly to the
JSON. For history, drop `MM-DD.json` files into `data/history/` — or just let the
daily task archive each date the first time it runs. Once all 366 dates are stored,
the generator runs fully offline.

## License

MIT (code + data compilation). Underlying facts belong to their sources — see `LICENSE`.
