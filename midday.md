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
Max 5 picks per message, best first. Number each pick and list: who/what (all caps) - date — time — venue. Include whitespace between each pick.
★ = watchlist hit. Flag conflicts with events.md (only if it's on that specific day. If an event runs multiple days, ignore conflict.)
Never invent lineups, dates, or prices.

SOURCE RULES:
Aggregators are listed first per category; use them before venue sites.
If a listed domain is blocked or a page needs a domain not listed, do not work around it. Add a "Needs permission: <domain> (for <what>)" line at the bottom of the message.

[MUSIC] 
Window: next 8 weeks. Lead with newly announced shows and presales/on-sales this week, then big shows already on sale. 
Focus: Notable performers and artists I listen to.
Fetch: bowerypresents.com + aegwebprod.blob.core.windows.net (the listings data for Terminal 5, Brooklyn Steel, Webster Hall, Bowery Ballroom, Forest Hills Stadium), barclayscenter.com, brooklynbowl.com, dice.fm (Elsewhere, Knockdown Center, smaller rooms — screen for big names only) 
Search (JS-rendered or bot-blocked, so find shows via web search, not fetching): Madison Square Garden, Radio City, Beacon Theatre, Brooklyn Paramount, Irving Plaza, Kings Theatre, UBS Arena, MetLife Stadium, Citi Field concerts 
Watchlist (artists/genres): 
Notes: Stadium/arena shows in Queens or NJ are worth including despite the borough rule; just flag the location.

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

[MUSEUMS & EXHIBITIONS] Window: openings in the next 2 weeks, closings in the next 3 weeks, free/late nights this week. 
Method: WEB SEARCH, not page fetching. Search engines have already indexed the museum sites, including the bot-blocked and JavaScript ones, so titles and dates show up in results. Do not fetch any museum site directly. 
Museums: The Met, MoMA, MoMA PS1, Guggenheim, Whitney, Brooklyn Museum, New Museum, The Frick, The Morgan Queries (per museum, current month + next month): "<museum> exhibitions closing <Month> <Year>", "<museum> exhibition opening <Month> <Year>", "<museum> press release exhibition <Year>" 
Rules: Only report a show if a result states its dates. Prefer the museum's own pages and press releases, then major outlets. Note "(dates unconfirmed)" rather than guessing. Search results older than 6 months only count for shows whose stated run covers the current date. Look for NYC and Brooklyn exhibitions more broadly as well don't limit to just the museums listed. Also check: nycforfree.co and secretnyc.co for free days, late nights, and one-off museum events. 
Watchlist: 
Notes: Focus on noteworthy exhibitions only. List 5 max.  List free museum days after as well. 

[SPORTS]
Window: next month.
Sources: espn.com
Teams/events:
Sports: NFL, MLB, NBA, NHL, UFC. 
Notes: Favor quality matchups in the area and make a note whenever Philadelphia or Boston teams come to town. Also callout and highlight any unique sporting events going on.

SOURCE NOTES:
(working endpoints for JS-rendered sites go here, one line per source)
whitney.org: https://whitney.org/exhibitions works directly (server-rendered).
frick.org: https://www.frick.org/exhibitions works with plain GET (server-rendered; WebFetch gets 418, curl with browser UA gets 200).
newmuseum.org: headless WordPress (Next.js/Faust); /exhibitions/ __NEXT_DATA__ has no exhibition list and /graphql/ is not publicly queryable — no working endpoint yet (2026-09-26).
guggenheim.org: /exhibition is JS-rendered WordPress shell; no data endpoint found yet (2026-09-26).
metmuseum.org, brooklynmuseum.org: return 429 to automated requests (2026-09-26).
moma.org, themorgan.org: return 403 to automated requests (2026-09-26).
timeout.com: /newyork/attractions/best-museum-exhibitions-in-nyc is stale (last updated Apr 6 2026) (2026-09-26).
donyc.com: /events/art returns 404; needs a different listing path (2026-09-26).
nycforfree.co: /resources/free-museums lists recurring free days/nights (2026-09-26).
barclayscenter.com: https://www.barclayscenter.com/events/category/concerts is server-rendered (curl --compressed); /events/all returns no list (2026-09-26).
brooklynbowl.com: https://www.brooklynbowl.com/brooklyn/shows/all is server-rendered with full list (curl --compressed) (2026-09-26).
ohmyrockness.com: /shows is JS-rendered from /api/shows.json?index=true&page=1&per=50&regioned=1, which returns "HTTP Token: Access denied" — no working endpoint (2026-09-26).
bowerypresents.com, foresthillsstadium.com: listings load from aegwebprod.blob.core.windows.net/json/... (unlisted domain — needs permission) (2026-09-26).
msg.com: /calendar is JS-rendered (0 events in HTML); no endpoint found yet (2026-09-26).
livenation.com: homepage has no __NEXT_DATA__ event list; venue pages e.g. /venue/KovZpZA7AAEA/madison-square-garden-events not yet tried (2026-09-26).
kingstheatre.com: connection failed (2026-09-26). ubsarena.com: 202 bot challenge (2026-09-26).


