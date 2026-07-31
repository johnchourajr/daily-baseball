#!/usr/bin/env python3
"""Build the Daily Baseball email (HTML + plain text) from the pre-stored bank.

Terms, stats, rules and quotes come entirely from data/ — no network needed.
Daily history is read from data/history/<MM-DD>.json when present; if a date
isn't stored yet, pass events in with --history <file> (the scheduled task
fetches them live and can save them back to grow the archive).

Usage:
    python -m dailyball.generate --date 07-31
    python -m dailyball.generate --date 07-31 --history events.txt
Outputs land in output/ as email_<YYYY-MM-DD>.{html,txt}.
"""
from __future__ import annotations
import argparse, datetime, html, os
from . import content

ROOT = content.ROOT
TEMPLATE = os.path.join(ROOT, "templates", "email.html")
OUT = os.path.join(ROOT, "output")

# section swatch colors, matched to the template
CLAY = "#b09a7d"


def _pretty(date_mmdd):
    try:
        return datetime.datetime.strptime(date_mmdd, "%m-%d").strftime("%B %-d")
    except ValueError:
        return date_mmdd


def _section_head(color, label):
    return (
        '<tr><td style="padding:36px 0 0 0;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
        f'<td width="14" style="width:14px;"><div style="width:14px;height:14px;background:{color};"></div></td>'
        f'<td style="padding-left:12px;font-size:16px;font-weight:600;color:#1c1c1a;">{label}</td>'
        '</tr></table></td></tr>')


def build(date_mmdd, history=None, commit_rotation=True):
    events = history if history is not None else (content.load_history(date_mmdd) or [])
    events = events[:5]
    term = content.pick_term(date_mmdd, commit=commit_rotation)
    stat = content.pick_stat(date_mmdd, commit=commit_rotation)
    rule = content.pick_rule(date_mmdd, commit=commit_rotation)
    quote = content.pick_quote(date_mmdd, commit=commit_rotation)
    pretty = _pretty(date_mmdd)

    # ---------------- plain text ----------------
    lines = [f"Daily Baseball — {pretty}", "fun facts from the archives", ""]
    if events:
        lines.append("THIS DAY IN BASEBALL HISTORY")
        lines += [f"  · {e}" for e in events]
        lines.append("")
    lines += [f"TERM OF THE DAY — {term['term']}", f"  {term['def']}"]
    meta = []
    if term.get("first_use"):
        meta.append(f"First used {term['first_use']}.")
    if term.get("origin"):
        meta.append(term["origin"])
    if meta:
        lines.append(f"  {' '.join(meta)}")
    lines += ["", "BY THE NUMBERS", f"  {stat['fact']}"]
    lines += ["", f"RULE CHANGE — {rule['year']}", f"  {rule['rule']}"]
    cite = f", {quote['cite']}" if quote.get("cite") else ""
    lines += ["", f'  "{quote["quote"]}"', f"  — {quote['speaker']}{cite}"]
    lines += ["", "Facts from baseball-almanac.com and the Dickson Baseball Dictionary."]
    text = "\n".join(lines)

    # ---------------- html ----------------
    if events:
        items = "".join(
            '<tr><td style="padding:0 0 14px 0;font-size:16px;line-height:1.6;color:#43423d;">'
            f'{html.escape(e)}</td></tr>' for e in events)
        history_block = (
            _section_head(CLAY, "This Day in Baseball History") +
            '<tr><td style="padding:14px 0 0 0;">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            f'{items}</table></td></tr>')
    else:
        history_block = ""

    tmeta = []
    if term.get("first_use"):
        tmeta.append(f"First used {html.escape(str(term['first_use']))}.")
    if term.get("origin"):
        tmeta.append(html.escape(term["origin"]))
    term_meta = (
        f'<div style="font-size:14px;line-height:1.6;color:#8a8a80;margin-top:10px;">{" ".join(tmeta)}</div>'
        if tmeta else "")

    rule_block = (
        _section_head("#c08a4a", "Rule Change") +
        '<tr><td style="padding:14px 0 0 0;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
        '<td width="52" valign="top" style="width:52px;font-size:16px;font-weight:600;color:#c08a4a;">'
        f'{rule["year"]}</td>'
        '<td style="font-size:16px;line-height:1.6;color:#43423d;">'
        f'{html.escape(rule["rule"])}</td></tr></table></td></tr>')

    qcite = f', {html.escape(quote["cite"])}' if quote.get("cite") else ""
    quote_block = (
        '<tr><td style="padding:40px 0 0 0;">'
        '<div style="background:#eeeef2;padding:26px 24px;">'
        '<div style="font-size:18px;line-height:1.55;color:#1c1c1a;letter-spacing:-0.01em;">'
        f'&ldquo;{html.escape(quote["quote"])}&rdquo;</div>'
        '<div style="font-size:14px;color:#7a7a86;margin-top:12px;">'
        f'{html.escape(quote["speaker"])}{qcite}</div>'
        '</div></td></tr>')

    preheader = f"{term['term']} · {rule['year']} rule change · and more"

    with open(TEMPLATE, encoding="utf-8") as f:
        tmpl = f.read()
    doc = tmpl.format(
        preheader=html.escape(preheader),
        pretty=pretty,
        history_block=history_block,
        term_name=html.escape(term["term"]),
        term_def=html.escape(term["def"]),
        term_meta=term_meta,
        stat_fact=html.escape(stat["fact"]),
        rule_block=rule_block,
        quote_block=quote_block)
    return text, doc, pretty


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="MM-DD")
    ap.add_argument("--history", help="optional file: one 'YEAR — event' per line")
    ap.add_argument("--year", type=int, default=datetime.date.today().year)
    args = ap.parse_args()
    hist = None
    if args.history:
        with open(args.history, encoding="utf-8") as f:
            hist = [l.strip() for l in f if l.strip()]
    text, doc, _ = build(args.date, history=hist)
    os.makedirs(OUT, exist_ok=True)
    stamp = f"{args.year}-{args.date}"
    open(os.path.join(OUT, f"email_{stamp}.txt"), "w", encoding="utf-8").write(text)
    open(os.path.join(OUT, f"email_{stamp}.html"), "w", encoding="utf-8").write(doc)
    print(f"Wrote output/email_{stamp}.html and .txt")


if __name__ == "__main__":
    main()
