# history/

One JSON file per calendar date, named `MM-DD.json`:

```json
{
  "date": "07-31",
  "events": ["1954 — Joe Adcock hit four home runs ...", "..."],
  "source": "https://www.baseball-almanac.com/history/today.php?d=07-31"
}
```

Only `07-31.json` is seeded. The daily task fetches any missing date live from
baseball-almanac and can save the result here — so the archive fills in over
time and each date only ever needs to be fetched once. Once all 366 dates are
stored, the generator runs fully offline.
