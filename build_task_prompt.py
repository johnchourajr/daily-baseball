#!/usr/bin/env python3
"""Generate the SELF-CONTAINED scheduled-task prompt from the data bank.

Why this exists: scheduled tasks run in Anthropic's cloud with NO device bridge,
so a prompt that points at the repo on the Mac can never work — it fails every
morning with "path does not exist". This bakes the rotation bank into the prompt
text so the task needs nothing but a live history fetch.

Rotation without a state file: the task computes N = day of the year and indexes
each list with (N mod len). Different list lengths mean the daily combination
varies, and each pool cycles without repeating.

LIMITS keeps the prompt small enough to store in a trigger. The full bank stays
in data/ for the local generator and future expansion.

Run after changing data/, then push automation/daily_task_prompt.txt into the
scheduled task via update_trigger.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "automation", "daily_task_prompt.txt")

# How many of each pool to embed. Raise these if the trigger accepts a bigger prompt.
LIMITS = {"terms": 41, "stats": 30, "dodgers_facts": 20,
          "rules": 25, "quotes": 20, "dodgers_quotes": 12}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


terms = load("terms.json")["terms"][:LIMITS["terms"]]
stats = [s for s in load("stats.json")["stats"] if s.get("verified")][:LIMITS["stats"]]
dod = load("dodgers.json")
dfacts = [f for f in dod["facts"] if f.get("verified")][:LIMITS["dodgers_facts"]]
dquotes = dod["quotes"][:LIMITS["dodgers_quotes"]]
rules = load("rules.json")["rule_changes"][:LIMITS["rules"]]
quotes = load("quotes.json")["quotes"][:LIMITS["quotes"]]


def term_line(t):
    s = f"{t['term']} — {t['def']}"
    if t.get("first_use"):
        s += f" (first used {t['first_use']})"
    return s


def quote_line(q):
    return f'"{q["quote"]}" — {q["speaker"]}'


def numbered(items, fmt):
    return "\n".join(f"{i}. {fmt(x)}" for i, x in enumerate(items))


prompt = f"""Produce John's "Daily Baseball" fun-facts email and deliver it to him. One recipient, no mailing list.

THIS TASK IS SELF-CONTAINED. Everything needed is below. Do NOT look for a repo, local folder, device bridge, or any file on John's Mac — this runs in the cloud and none of that is reachable. Do NOT run a script. Do NOT invent any fact not listed below.

STEP 1 — Get today's date. Compute N = day of the year (Jan 1 = 1, Feb 1 = 32, etc.).

STEP 2 — HISTORY (the only live lookup). WebFetch https://www.baseball-almanac.com/history/today.php?d=MM-DD using today's MM-DD. Ask for the "This Day in Baseball History" events verbatim as "YEAR — event". Keep the 4-5 most interesting (records, milestones, famous names, firsts). If the fetch fails or is empty, SKIP the history section — do not invent events.

STEP 3 — Pick by index. Lists below are numbered from 0; use index (N mod COUNT):
  TERM OF THE DAY : TERMS ({len(terms)})
  BY THE NUMBERS  : if N is even -> DODGERS FACTS ({len(dfacts)}); if N is odd -> STATS ({len(stats)})
  RULE CHANGE     : RULES ({len(rules)})
  CLOSING QUOTE   : if N mod 3 == 0 -> DODGERS QUOTES ({len(dquotes)}); else QUOTES ({len(quotes)})

STEP 4 — Compose exactly this plain-text shape:

Daily Baseball — <Month Day>
fun facts from the archives

THIS DAY IN BASEBALL HISTORY
  · <event>
  · <event>

TERM OF THE DAY — <term name>
  <definition>

BY THE NUMBERS
  <fact>

RULE CHANGE — <year>
  <rule text>

  "<quote>"
  — <speaker>

Facts from baseball-almanac.com and the Dickson Baseball Dictionary.

STEP 5 — DELIVER: output that finished email as your FINAL message, verbatim, with no preamble, no summary, no commentary, and no explanation of your picks. That text rides along in this task's completion notification to John's inbox — it IS the email. Nothing else belongs in the final message. Do not create a Gmail draft (the connected Gmail can only draft, never send).

===== TERMS ({len(terms)}) =====
{numbered(terms, term_line)}

===== STATS ({len(stats)}) — numbers hand-verified; use exactly as written =====
{numbered(stats, lambda s: s['fact'])}

===== DODGERS FACTS ({len(dfacts)}) =====
{numbered(dfacts, lambda s: s['fact'])}

===== RULES ({len(rules)}) — render as "RULE CHANGE — <year>" =====
{numbered(rules, lambda r: f"{r['year']} :: {r['rule']}")}

===== QUOTES ({len(quotes)}) =====
{numbered(quotes, quote_line)}

===== DODGERS QUOTES ({len(dquotes)}) =====
{numbered(dquotes, quote_line)}
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(prompt)

print(f"wrote automation/daily_task_prompt.txt — {len(prompt):,} chars")
print(f"  terms {len(terms)} | stats {len(stats)} | dodgers facts {len(dfacts)}")
print(f"  rules {len(rules)} | quotes {len(quotes)} | dodgers quotes {len(dquotes)}")
