ROTATION: 
Mon: music 
Tue: talks & lectures 
Wed: comedy 
Thu: movies 
Fri: pop-ups & events 
Sat: museums & exhibitions 
Sun: sports

GLOBAL PREFERENCES: Home base: Williamsburg. Brooklyn and Manhattan are in range. Flag anything in Queens, the Bronx, Staten Island, or NJ. 
Max 5 picks per message, best first. Number each pick and list: who/what (all caps) - date — time — venue. Include whitespace between each pick. 
★ = watchlist hit. Flag conflicts with events.md (only if it's on that specific day. If an event runs multiple days, ignore conflict.) 
Never invent lineups, dates, or prices.

SOURCE RULES: Aggregators are listed first per category; use them before venue sites. Fetch ladder for every source not marked Search:
1.	Use the method in SOURCE NOTES if one exists.
2.	Otherwise plain fetch. If the listings are in the HTML, or the HTML points to a data file/API, use that.
3.	Otherwise render the page with headless Chromium (Playwright), wait for listings to load, and read the rendered page or the data requests it makes. Once a method works, record it in SOURCE NOTES so the next run goes straight to it. Replace outdated lines instead of adding duplicates. The browser is only for pages that need JavaScript. Never use it to get past logins, tokens, captchas, or bot checks; those sources stay on web search. If a listed domain is blocked or a page (including a rendered page's data requests) needs a domain not listed, do not work around it. Add a "Needs permission: <domain> (for <what>)" line at the bottom of the message.

[MUSIC] 
Window: next 8 weeks. Lead with newly announced shows and presales/on-sales this week, then big shows already on sale. 
Focus: Notable performers and artists I listen to. 
Fetch: bowerypresents.com + aegwebprod.blob.core.windows.net (the listings data for Terminal 5, Brooklyn Steel, Webster Hall, Bowery Ballroom, Forest Hills Stadium), msg.com (Madison Square Garden, Radio City, Beacon Theatre, Hulu Theater), livenation.com (Brooklyn Paramount, Irving Plaza, Hammerstein Ballroom), barclayscenter.com, brooklynbowl.com, dice.fm (Elsewhere, Knockdown Center, smaller rooms) 
Search (bot-blocked or unreachable, so find shows via web search, not fetching): Kings Theatre, UBS Arena, MetLife Stadium, Citi Field concerts 
Watchlist (artists/genres): 
Notes: Stadium/arena shows in Queens or NJ are worth including despite the borough rule; just flag the location.

[TALKS & LECTURES] 
Window: next 6 weeks. Big names sell out early — flag anything with limited tickets. 
Sources: 92ny.org, nypl.org, strandbooks.com, bklynlibrary.org, mcnallyjackson.com 
Watchlist (speakers/authors/topics): 
Notes:

[COMEDY] Window: today through Sunday (Cellar lineups post late Tuesday). 
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
Fetch (fetch ladder): guggenheim.org, newmuseum.org, whitney.org Search only (bot-blocked — do not fetch): The Met, MoMA, MoMA PS1, Brooklyn Museum, The Frick, The Morgan Queries (per search-only museum, current month + next month): "<museum> exhibitions closing <Month> <Year>", "<museum> exhibition opening <Month> <Year>", "<museum> press release exhibition <Year>" 
Rules: Only report a show if a source states its dates. Prefer the museum's own pages and press releases, then major outlets. Note "(dates unconfirmed)" rather than guessing. Search results older than 6 months only count for shows whose stated run covers the current date. Look for NYC and Brooklyn exhibitions more broadly as well; don't limit to just the museums listed. Also check: nycforfree.co and secretnyc.co for free days, late nights, and one-off museum events. 
Watchlist: 
Notes: Focus on noteworthy exhibitions only. List 5 max. List free museum days after as well. If the exhibition is ongoing, don't worry about checking against events.md.

[SPORTS] 
Window: next month. 
Sources: espn.com 
Teams/events: 
Sports: NFL, MLB, NBA, NHL, UFC. 
Notes: Favor quality matchups in the area and make a note whenever Philadelphia or Boston teams come to town. Also callout and highlight any unique sporting events going on.

SOURCE NOTES:
(best working method per source, one line each, dated. A single failure is not a write-off: note it and retry next run. Only mark a source search-only for a deliberate block such as 403/429/bot challenge.)
Search only, do not fetch (deliberate bot blocks): metmuseum.org, brooklynmuseum.org (429); moma.org, themorgan.org (403); frick.org (418 bot check); ubsarena.com (bot challenge) (2026-09-26).
barclayscenter.com: https://www.barclayscenter.com/events/category/concerts is server-rendered (curl --compressed) (2026-09-26).
brooklynbowl.com: https://www.brooklynbowl.com/brooklyn/shows/all is server-rendered with full list (curl --compressed) (2026-09-26).
bowerypresents.com: listings JSON at https://aegwebprod.blob.core.windows.net/json/resources/8/events/208lbnmkq5/events.json and .../7301mbln09/events.json (paths found in bowerypresents.com homepage HTML); fields: eventDateTime, title.headlinersText, venue.title, announceDateTime, onsaleDateTime, presaleDateTime. Covers NYC + other markets, filter by venue (2026-09-26).
espn.com: team schedules via JSON API https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/teams/{abbr}/schedule?seasontype={1 pre|2 reg|3 post} (abbrs: nyg nyj ny bkn nyr nyi nj nyy nym) (2026-09-26).
whitney.org: https://whitney.org/exhibitions works with plain fetch (server-rendered) (2026-09-26).
nycforfree.co: /resources/free-museums lists recurring free days/nights; follow redirects (curl -L) (2026-09-26).
guggenheim.org: https://www.guggenheim.org/exhibitions shell is JS, but exhibition data is embedded as JSON in the HTML (curl --compressed; parse "title" + "dates":{"start":{day,month,year},"end":{...}}) (2026-09-26).
newmuseum.org: https://www.newmuseum.org/exhibitions — parse __NEXT_DATA__ JSON (title, startDate, endDate, dateTextOverride) (2026-09-26).
secretnyc.co: homepage plain fetch works (curl -L --compressed) (2026-09-26).
