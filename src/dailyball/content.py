"""Content bank loaders + no-repeat rotation.

The pool is fully pre-stored (see ../../data). Nothing here hits the network.
Rotation avoids repeating a term or stat until the whole pool has cycled,
tracking usage in a small state file under output/.
"""
from __future__ import annotations
import json, os, hashlib
from datetime import date as _date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")
STATE = os.path.join(ROOT, "output", ".rotation_state.json")
CONFIG = os.path.join(ROOT, "config.json")


def _load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def load_terms():
    return _load("terms.json")["terms"]


def load_stats(verified_only=True):
    s = _load("stats.json")["stats"]
    return [x for x in s if x.get("verified")] if verified_only else s


def load_abbreviations():
    return _load("abbreviations.json")


def load_formulas():
    """Stat definitions and formulas (offensive / pitching / defensive)."""
    return _load("formulas.json")


def load_dictionary_index():
    """The full A-Z term index: every term name plus its definition-page URL."""
    return _load("dictionary_index.json")


def lookup_term(query):
    """Search the full dictionary index. Returns matching {term, url} entries."""
    q = query.lower().strip()
    hits = []
    for letter in load_dictionary_index()["letters"].values():
        for entry in letter["terms"]:
            if q in entry["term"].lower():
                hits.append(entry)
    hits.sort(key=lambda e: (e["term"].lower() != q, len(e["term"])))
    return hits


def load_rules():
    return _load("rules.json")["rule_changes"]


def load_knickerbocker():
    return _load("rules.json")["knickerbocker_1845"]


def load_quotes():
    return _load("quotes.json")["quotes"]


# ---------------- team focus ----------------

def load_config():
    try:
        with open(CONFIG, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"team_focus": None, "team_bias": 0.0}


def load_team():
    """Return the configured team bank, or None."""
    team = load_config().get("team_focus")
    if not team:
        return None
    try:
        return _load(f"{team}.json")
    except OSError:
        return None


def team_facts():
    t = load_team()
    return [f for f in t["facts"] if f.get("verified")] if t else []


def team_quotes():
    t = load_team()
    return t["quotes"] if t else []


def _use_team(key, slot):
    """Deterministically decide whether this day's slot draws from the team bank."""
    bias = float(load_config().get("team_bias", 0.0) or 0.0)
    if bias <= 0:
        return False
    if bias >= 1:
        return True
    return (_seed(key, "teamgate:" + slot) % 1000) < int(bias * 1000)


def load_history(date_mmdd):
    """Return the pre-stored events list for MM-DD, or None if not stored yet."""
    path = os.path.join(DATA, "history", f"{date_mmdd}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("events", [])
    return None


def _read_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"terms": [], "stats": []}


def _write_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _seed(key, salt):
    return int(hashlib.sha256(f"{key}|{salt}".encode()).hexdigest(), 16)


def rotate(items, kind, key, keyfn, commit=True):
    """Pick an item, preferring ones not used recently.

    `key` is a stable per-day string (e.g. the date). Among items not in the
    recent-use log we pick deterministically from `key`; if all have been used,
    the oldest-used item is chosen and the log resets. Returns the chosen item.
    """
    state = _read_state()
    used = state.get(kind, [])
    ids = [keyfn(x) for x in items]
    fresh = [x for x in items if keyfn(x) not in used]
    if fresh:
        choice = fresh[_seed(key, kind) % len(fresh)]
    else:
        used = []  # everything cycled — start over
        choice = items[_seed(key, kind) % len(items)]
    if commit:
        used = used + [keyfn(choice)]
        # keep the log from growing past the pool size
        if len(used) >= len(ids):
            used = used[-(len(ids) - 1):] if len(ids) > 1 else []
        state[kind] = used
        _write_state(state)
    return choice


def pick_term(key, commit=True):
    return rotate(load_terms(), "terms", key, lambda x: x["term"], commit)


def pick_stat(key, commit=True):
    """By the Numbers — drawn from the team bank on team-gated days."""
    tf = team_facts()
    if tf and _use_team(key, "stat"):
        return rotate(tf, "team_stats", key, lambda x: x["fact"], commit)
    return rotate(load_stats(), "stats", key, lambda x: x["fact"], commit)


def pick_rule(key, commit=True):
    return rotate(load_rules(), "rules", key,
                  lambda x: f"{x['year']}:{x['rule'][:40]}", commit)


def pick_quote(key, commit=True):
    """Closing quote — drawn from the team bank on team-gated days."""
    tq = team_quotes()
    if tq and _use_team(key, "quote"):
        return rotate(tq, "team_quotes", key, lambda x: x["quote"][:60], commit)
    return rotate(load_quotes(), "quotes", key, lambda x: x["quote"][:60], commit)
