ROTATION:
Mon: music
Tue: talks & lectures
Wed: comedy
Thu: movies
Fri: pop-ups & events
Sat: museums & exhibitions
Sun: sports

GLOBAL PREFERENCES:
Home base: Williamsburg. Brooklyn and Manhattan are in range. Flag anything in Queens, the Bronx, Staten Island, or NJ.
Max 8–10 picks per message, best first. Each pick: date — time — venue — who/what — price — link.
★ = watchlist hit. Flag conflicts with events.md.
Never invent lineups, dates, or prices.

SOURCE RULES:
Aggregators are listed first per category; use them before venue sites.
If a listed domain is blocked or a page needs a domain not listed, do not work around it. Add a "Needs permission: <domain> (for <what>)" line at the bottom of the message.

[MUSIC]
Window: next 8 weeks. Lead with newly announced shows and presales/on-sales this week, then big shows already on sale.
Focus: Notable performers and artists I listen to.
Sources: livenation.com (NYC-area venues incl. Brooklyn Paramount, Irving Plaza, Hammerstein, stadium tours), msg.com (Madison Square Garden, Radio City, Beacon Theatre, Hulu Theater), barclayscenter.com, bowerypresents.com (Terminal 5, Brooklyn Steel, Webster Hall), kingstheatre.com, ubsarena.com, foresthillsstadium.com, ohmyrockness.com (NYC show aggregator), dice.fm (Elsewhere, Knockdown Center, smaller rooms), brooklynbowl.com
Watchlist (artists/genres):
Notes: Stadium/arena shows in Queens or NJ (UBS Arena, Forest Hills, MetLife) are worth including despite the borough rule; just flag the location.

[TALKS & LECTURES]
Window: next 6 weeks. Big names sell out early — flag anything with limited tickets.
Sources: 92ny.org, nypl.org, strandbooks.com, bklynlibrary.org, mcnallyjackson.com
Watchlist (speakers/authors/topics):
Notes:

[COMEDY]
Window: today through Sunday (Cellar lineups post late Tuesday).
Sources: standup.nyc (aggregator), comedycellar.com (MacDougal St, Village Underground, Fat Black Pussycat), thestandnyc.com, newyorkcomedyclub.com, thebellhouseny.com
Watchlist (comics):
Notes: Favor stacked lineups, big names, drop-in-prone slots, and one-off specials over routine showcases.

[MOVIES]
Window: wide releases opening this weekend + repertory/special screenings in the next 2 weeks.
Sources: rottentomatoes.com (wide releases opening this week, with scores), metrograph.com, filmforum.org, ifccenter.com, filmlinc.org, nitehawkcinema.com
Watchlist (directors/actors/films):
Notes: Lead with the notable wide releases (include Rotten Tomatoes score if available), then Q&As, premieres, and 35mm/70mm screenings.

[POP-UPS & EVENTS]
Window: this weekend + next 2 weeks. Prioritize anything needing a reservation or ticket.
Sources: Time Out's "The best things to do in NYC this weekend" (https://www.timeout.com/newyork/things-to-do/things-to-do-in-nyc-this-weekend; if that URL moves, find the current version from timeout.com/newyork/things-to-do), donyc.com, nycforfree.co, secretnyc.co, ny.eater.com, theinfatuation.com, smorgasburg.com
Watchlist:
Notes: Restaurant openings, chef collabs, food/drink pop-ups, markets, festivals, free events, one-off happenings. Always check the Time Out weekend article first.

[MUSEUMS & EXHIBITIONS] 
Window: openings in the next 2 weeks, closings in the next 3 weeks, free/late nights this week. 
Sources (aggregators first — these cover the Met, MoMA, Brooklyn Museum, and the Morgan, whose sites block automated access): timeout.com (museum/art exhibition roundups under timeout.com/newyork), hyperallergic.com (monthly New York art guide), donyc.com (museum/art listings), nycforfree.co (free museum days), secretnyc.co Direct sites: whitney.org, frick.org, guggenheim.org and newmuseum.org (JS-rendered — use the data endpoint in SOURCE NOTES; if none works, rely on the aggregators) Watchlist: 
Notes: Lead with "last chance" closings. Do not fetch metmuseum.org, moma.org, brooklynmuseum.org, or themorgan.org directly. They block bots, so don't retry or work around them.

SOURCE NOTES:
(working endpoints for JS-rendered sites go here, one line per source)
whitney.org: https://whitney.org/exhibitions works directly (server-rendered).
frick.org: https://www.frick.org/exhibitions works with plain GET (server-rendered; WebFetch gets 418, curl with browser UA gets 200).
newmuseum.org: headless WordPress (Next.js/Faust); /exhibitions/ __NEXT_DATA__ has no exhibition list and /graphql/ is not publicly queryable — no working endpoint yet (2026-09-26).
guggenheim.org: /exhibition is JS-rendered WordPress shell; no data endpoint found yet (2026-09-26).
metmuseum.org, brooklynmuseum.org: return 429 to automated requests (2026-09-26).
moma.org, themorgan.org: return 403 to automated requests (2026-09-26).


