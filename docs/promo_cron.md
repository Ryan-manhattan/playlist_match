# Hourly Promotion Refresh

This project now generates a fresh hero/offer pitch every hour. The automation flow is:

1. `scripts/update_promo.py` gathers Supabase stats (tracks, posts, worldcup votes, visits) and the top-ranked track.
2. It builds a new `promo.json` payload with dynamic hero copy, offers, metrics, and CTA targets.
3. `index.html` renders this `promo_content` alongside the growth snapshot, so the landing hero always reflects live stats.

To keep it running automatically, install a cron entry on the host machine:

```
0 * * * * cd /Users/junkim/Projects/off_community && /usr/bin/env python3 scripts/update_promo.py >/tmp/promo-cron.log 2>&1
```

This executes every hour on the hour and writes a log for debugging. Review `/tmp/promo-cron.log` if you need to check for failures.
