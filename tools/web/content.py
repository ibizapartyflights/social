import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import *

pages = []

# 1. Where to stay
body = f'''
<p>Ibiza is small: you can drive across it in under an hour. But where you sleep still changes the whole trip, from how much you spend on taxis to whether you can sleep at all. Most party trips end up in one of four areas.</p>

<div class="tw"><table>
<tr><th>Area</th><th>Best for</th><th>Clubs nearby</th><th>Watch out for</th></tr>
<tr><td><b>Playa d'en Bossa</b></td><td>Groups who want the big clubs on the doorstep</td><td>Ushuaïa, Hï Ibiza, DC-10 a short taxi away</td><td>Loud, busy, prices jump on party nights</td></tr>
<tr><td><b>Ibiza Town</b></td><td>Couples and mixed groups who want restaurants and the old town</td><td>Pacha, short taxis to the rest</td><td>Fewer pools, parking is hard</td></tr>
<tr><td><b>Sant Rafel</b></td><td>Club-focused trips on a budget</td><td>Amnesia, [UNVRS]</td><td>Inland, no beach on foot</td></tr>
<tr><td><b>San Antonio</b></td><td>First trips, sunsets and the best value beds</td><td>Pool parties, sunset bars</td><td>West End streets can be rowdy</td></tr>
</table></div>

<h2>Playa d'en Bossa</h2>
<p>A long beach a few minutes from the airport, with the day-to-night clubs on the same strip. If your plan is pool parties in the afternoon and a club at night, this is the most convenient base, and you can often walk home. The trade-off is noise and price: on the big nights hotels here are the first to fill up.</p>
<p><a href="{bk("Playa d'en Bossa")}" target="_blank" rel="noopener sponsored">See hotels in Playa d'en Bossa →</a></p>

<h2>Ibiza Town</h2>
<p>The marina, the old walled town of Dalt Vila (a UNESCO World Heritage Site) and most of the island's good restaurants. Pacha is in town and Playa d'en Bossa is a short taxi ride away. A good choice if your group wants nights out and proper dinners, not just clubs.</p>
<p><a href="{bk("Ibiza Town")}" target="_blank" rel="noopener sponsored">See hotels in Ibiza Town →</a></p>

<h2>Sant Rafel</h2>
<p>A small village on the main road between Ibiza Town and San Antonio, closest to the two big inland clubs. Accommodation is often cheaper, but you will need taxis or the night bus for almost everything else.</p>
<p><a href="{bk("Sant Rafel de Sa Creu")}" target="_blank" rel="noopener sponsored">See hotels in Sant Rafel →</a></p>

<h2>San Antonio</h2>
<p>On the west coast, famous for its sunset strip, bars and pool parties. It usually has the widest choice of budget hotels and apartments, which is why so many first trips start here. The big clubs are a taxi or night-bus ride away.</p>
<p><a href="{bk("San Antonio, Ibiza")}" target="_blank" rel="noopener sponsored">See hotels in San Antonio →</a></p>

<h2>How to choose</h2>
<ul>
<li><b>Pick your main party first.</b> Staying near the club you go to most saves the most money on taxis.</li>
<li><b>Book early for opening and closing weeks.</b> These are the nights hotels near the clubs sell out first.</li>
<li><b>Check the cancellation policy.</b> Party dates are only confirmed in early spring, so free cancellation is worth a little extra.</li>
<li><b>Splitting rooms?</b> Apartments are often cheaper per person for groups of four or more.</li>
</ul>
'''
pages.append(("where-to-stay-in-ibiza", "Where to stay in Ibiza for a party trip (2027 guide)",
  "Playa d'en Bossa, Ibiza Town, Sant Rafel or San Antonio? The four Ibiza party areas compared for UK groups: clubs nearby, noise, prices and who each one suits.",
  "Where to stay in Ibiza for a party trip",
  "The four areas most party trips choose, compared side by side, so your group can pick in five minutes.",
  "img/hotel_playa.jpg", body,
  [("What is the best area to stay in Ibiza for clubbing?", "Playa d'en Bossa is the most convenient for the big day-to-night clubs, and Sant Rafel is closest to the inland clubs. Ibiza Town suits groups who also want restaurants and the old town."),
   ("Where is cheapest to stay in Ibiza?", "San Antonio and Sant Rafel usually have the most budget hotels and apartments. Prices everywhere rise on opening and closing weekends."),
   ("How far is the airport from Playa d'en Bossa?", "Very close: it is the nearest party area to Ibiza airport, usually a short taxi or transfer ride.")]))

# 2. Airport to hotel
body = f'''
<p>Ibiza airport (IBZ) is in the south of the island, close to Playa d'en Bossa and a short drive from Ibiza Town. Flights from the UK take around two and a half hours, so most people land with one question: what is the easiest way to the hotel?</p>

<h2>Option 1: the bus</h2>
<p>Public buses run from the stop outside arrivals to the main resorts, including Ibiza Town, Playa d'en Bossa and San Antonio, with more routes and more frequent services in summer. It is the cheapest option, but you may have to wait, and the last bus can be early compared with late arrivals. Check the current timetable on the island bus operator's website before you fly, as routes change between seasons.</p>

<h2>Option 2: a taxi from the rank</h2>
<p>The taxi rank is right outside arrivals and taxis are metered. Outside the busiest weeks it is quick and easy. On peak summer evenings, when several flights land at once, the queue can be long. Fares are higher at night and on public holidays.</p>

<h2>Option 3: a pre-booked transfer</h2>
<p>You book and pay before you fly, the price is fixed, and the driver waits at arrivals with your name, even if the flight is late. For groups it often works out similar per person to a taxi, and there is a vehicle for everyone and the luggage.</p>
{cta(TAXI, "Compare airport transfers on Kiwitaxi")}
{cta(WPICK, "Or book with Welcome Pickups", "line")}

<div class="box"><h3>Our take</h3>
<p>Travelling light and landing in daylight? The bus is fine. Landing late, in a group, or on a peak weekend? A pre-booked transfer saves you the queue and the guesswork.</p></div>

<h2>Getting around after that</h2>
<ul>
<li><b>Night buses</b> link the main resorts and clubs in summer, a cheap way home after a night out.</li>
<li><b>Taxis</b> can be hard to find at closing time on big nights. Agree a plan with your group before you go in.</li>
<li><b>Car hire</b> is great for beach days in the north, but leave the car at the hotel on party nights. Never drive after drinking.</li>
</ul>
{cta(CAR, "Compare car hire on Localrent", "line")}

<h2>Flight delayed on the way?</h2>
<p>If your flight arrived more than three hours late or was cancelled, you may be owed compensation under UK and EU rules. You can claim directly from the airline for free, or use a claims company that takes a fee only if you are paid.</p>
{cta(DELAY, "Check your flight with AirHelp", "line")}
'''
pages.append(("ibiza-airport-to-hotel", "Ibiza airport to your hotel: bus, taxi or transfer?",
  "How to get from Ibiza airport (IBZ) to Playa d'en Bossa, Ibiza Town or San Antonio. Bus, taxi rank and pre-booked transfers compared for UK travellers.",
  "Ibiza airport to your hotel: bus, taxi or transfer?",
  "Three ways out of arrivals, how each one works, and which to pick for your group.",
  "img/playa_gente.jpg", body,
  [("Is there a bus from Ibiza airport?", "Yes. Public buses run from outside arrivals to the main resorts, with more services in summer. Check the current timetable before you fly."),
   ("Are taxis at Ibiza airport metered?", "Yes, taxis from the rank are metered, with higher fares at night. Queues can be long on peak summer evenings."),
   ("Should I pre-book an airport transfer in Ibiza?", "It is worth it if you land late, travel as a group or arrive on a peak weekend: the price is fixed and the driver waits for you.")]))

# 3. Budget
body = f'''
<p>Ibiza has a reputation for being expensive, and on a big club night it can be. But most of the cost of a trip is decided before you land, by when you go and how you book. Here is where the money actually goes, and where you can save.</p>

<h2>1. Go outside the peak weeks</h2>
<p>July and August are the busiest and most expensive months for flights and beds. Late May, June and September still have the parties and the warm sea, usually for noticeably less. Opening and closing weekends are the exception: they are popular, so book those early.</p>

<h2>2. Book flights early and be flexible</h2>
<p>Many UK airports fly direct to Ibiza in summer, not just London. Checking a few nearby airports and moving your dates by a day can make a real difference.</p>
{cta(FLY, "Compare flights to Ibiza")}

<h2>3. Pick the area for the trip you want</h2>
<p>San Antonio and Sant Rafel usually have the cheapest beds. Staying near your main club also cuts the taxi bill, which adds up fast on a four-night trip. Our <a href="/guides/where-to-stay-in-ibiza.html">where to stay guide</a> compares the four areas.</p>

<h2>4. Buy club tickets in advance</h2>
<p>For the big clubs, tickets bought online ahead of the night are usually cheaper than paying on the door, and popular nights sell out. Always buy from the club's official ticket seller.</p>

<h2>5. Sort the airport run before you fly</h2>
<p>A fixed-price transfer split between the group often costs about the same per person as a taxi, without the queue. See <a href="/guides/ibiza-airport-to-hotel.html">airport to hotel</a>.</p>

<h2>6. Eat and drink like a local by day</h2>
<p>Supermarkets, bakeries and set-menu lunches away from the beachfront are far cheaper than beach clubs. Save the beach club for one special day.</p>

<h2>7. Use the night bus</h2>
<p>In summer, night buses link the main resorts and clubs for a fraction of a taxi fare.</p>

<div class="box"><h3>Before you go</h3>
<ul>
<li>Get your free UK Global Health Insurance Card (GHIC) and take travel insurance.</li>
<li>Pack an EU plug adaptor, SPF 50 and a power bank.</li>
<li>Check your bank's fees for paying in euros abroad.</li>
<li>Check your phone plan's roaming charges in Spain. If they are high, a travel eSIM with a data bundle can work out cheaper. <a href="{ESIM}" target="_blank" rel="noopener sponsored">See Spain eSIMs on Airalo</a>.</li>
</ul></div>
'''
pages.append(("ibiza-on-a-budget", "Ibiza on a budget: how UK groups spend less",
  "Practical ways to do Ibiza for less from the UK: when to go, booking flights and hotels, club tickets, airport transfers and the night bus.",
  "Ibiza on a budget: how to spend less",
  "Where the money goes on an Ibiza party trip, and seven ways to keep more of it.",
  "img/hamacas.jpg", body,
  [("What is the cheapest month to go to Ibiza?", "Prices are usually lowest at the start and end of the season, in late spring and late September to October, and highest in July and August."),
   ("Is it cheaper to buy Ibiza club tickets in advance?", "Usually yes. Online tickets bought ahead from the official seller are often cheaper than the door, and popular nights sell out.")]))

# 4. First time
body = f'''
<p>Your first trip to Ibiza goes fast. These are the things people tell us they wish they had known before landing.</p>

<h2>The nights start late</h2>
<p>Most clubs only get busy well after midnight and keep going until morning. Daytime and open-air parties finish earlier. A nap and a late dinner are part of the plan.</p>

<h2>Plan how you get home</h2>
<p>At closing time on big nights, taxis are the hardest thing on the island to find. Know your night bus, agree a meeting point, and keep the hotel address saved offline. Never drive after drinking.</p>

<h2>Buy tickets before the night</h2>
<p>Popular nights sell out and the door is often more expensive. Buy from the club's official ticket seller only, never from strangers outside.</p>

<h2>Look after yourself</h2>
<ul>
<li>It is hot: drink water between drinks and wear SPF 50 by day.</li>
<li>Keep your phone charged. A power bank is the most useful thing you can pack.</li>
<li>Bring comfortable shoes you have already worn in.</li>
<li>Keep an eye on your drink and on your mates.</li>
<li>In an emergency, call 112, the European emergency number.</li>
</ul>

<h2>Stay online</h2>
<p>Maps, taxis, tickets on your phone and finding your mates after the club all need data. Some UK mobile plans charge for roaming in Spain, so check yours before you fly. If yours does, a travel eSIM is a simple fix: you buy a data bundle online and install it before you land.</p>
{cta(ESIM, "See Spain eSIMs on Airalo", "line")}

<h2>Paperwork from the UK</h2>
<ul>
<li>Check your passport is valid for your whole trip and meets the EU entry rules for UK travellers.</li>
<li>Get a free UK Global Health Insurance Card (GHIC) and travel insurance.</li>
<li>Spain uses the euro and type C/F plugs.</li>
</ul>

<h2>See the island too</h2>
<p>Ibiza is more than its clubs. Locals call it Eivissa. The old town of Dalt Vila is a UNESCO World Heritage Site, the coves on the west coast are some of the clearest water in the Mediterranean, and Formentera is an easy ferry ride away from Ibiza Town.</p>
{cta(FLY, "Compare flights to Ibiza")}
'''
pages.append(("first-time-in-ibiza", "First time in Ibiza? What UK first-timers should know",
  "First trip to Ibiza from the UK? Club times, getting home safely, tickets, money, plugs, GHIC and what to see beyond the clubs.",
  "First time in Ibiza: what to know before you go",
  "The things first-timers wish they had known, from club times to getting home safely.",
  "img/luces_club.jpg", body,
  [("What time do Ibiza clubs open?", "Most clubs get busy well after midnight and run until morning. Daytime and open-air parties usually finish earlier."),
   ("What is the emergency number in Ibiza?", "112, the European emergency number, works across Spain including Ibiza.")]))

# 5. Opening and closing
body = f'''
<p>The Ibiza club season runs roughly from late April to mid October. The first and last parties of each club, the openings and closings, are the busiest nights of the year, and they shape when most people book.</p>

<h2>When do Ibiza clubs open in 2027?</h2>
<p>Most of the big clubs open between late April and May. Opening weekends have a special energy: everyone is back on the island, and the line-ups are announced to set the tone for the summer. The exact 2027 opening dates are set by each club, so check our 2027 dates section below before you book.</p>

<h2>Ibiza closing parties 2026: how the season ended</h2>
<p>Closings run from late September into mid October. In 2026 most of the big clubs closed in the second week of October. Closing parties are often the most emotional nights of the year, and the first to sell out.</p>

<h2>2027 dates</h2>
<p>Clubs usually announce their dates between January and March. We add them to our <a href="/#tickets">party calendar</a> as soon as each club confirms. Until then, treat any date you see online as a guess.</p>

<h2>How to plan around an opening or closing</h2>
<ol>
<li><b>Wait for the official date</b> before you book anything non-refundable.</li>
<li><b>Book the flight and hotel as soon as it is confirmed.</b> These weekends fill up first.</li>
<li><b>Buy the ticket from the official seller</b> early. Closings sell out.</li>
<li><b>Arrive the day before and leave two days after.</b> No 6am flight after a closing night.</li>
<li><b>Sort the airport transfer in advance.</b> Arrivals are at their busiest on these weekends.</li>
</ol>
{cta(FLY, "Compare flights to Ibiza")}
{cta(TAXI, "Book an airport transfer", "line")}
<p class="by">Party clips on this site were filmed by our team at the 2026 closings.</p>
'''
pages.append(("ibiza-opening-and-closing-parties", "Ibiza opening and closing parties: dates and how to plan",
  "When are Ibiza's opening and closing parties? How the club season works, when 2027 dates are announced and how to plan flights and hotels around them.",
  "Ibiza opening and closing parties: how to plan",
  "When the season starts and ends, when 2027 dates come out, and how to book around the biggest nights.",
  "video/amnesia_crowd.jpg", body,
  [("When does the Ibiza club season start and end?", "Roughly late April or May to mid October, with openings in spring and closings from late September into October."),
   ("When are Ibiza 2027 party dates announced?", "Clubs usually confirm their dates between January and March."),
   ("When did the Ibiza closing parties 2026 take place?", "Closings ran from late September into October, and most of the big clubs closed in the second week of October 2026."),
   ("When do Ibiza clubs open in 2027?", "Each club sets its own date. Openings normally fall between late April and May, but until a club confirms its 2027 date, treat any date you see online as a guess.")],
  "2026-11-17"))

# 6. Boat day
body = f'''
<p>A day on the water is the best way to recover from a night out, and the best photos of the trip. There are two main ways to do it.</p>

<h2>Ibiza boat parties</h2>
<p>Shared daytime boats with a DJ, a bar and swim stops along the coast. You buy a ticket per person, so they work well for small groups and solo travellers. Check what is included: drinks, food, snorkels and transfers to the port vary a lot.</p>

<h2>Private boat hire</h2>
<p>For bigger groups, hiring a whole boat can cost about the same per person and lets you choose the music, the coves and the timing. Larger boats come with a skipper; smaller ones can sometimes be hired without a licence, close to the coast. Ask what is included: fuel, skipper, drinks and cleaning are often extras.</p>

<h2>Where boats go</h2>
<ul>
<li>The coves of the west and south-west coast, with views of the rock island of Es Vedrà.</li>
<li>Formentera and the shallow turquoise water around it, on longer trips.</li>
<li>Protected Posidonia seagrass keeps the water clear: boats should anchor on sand, not on the meadows.</li>
</ul>

<div class="box"><h3>What to bring</h3>
<ul><li>SPF 50, a hat and water</li><li>Cash or card for the bar</li><li>A waterproof phone pouch</li><li>A towel and a dry layer for the trip back</li></ul></div>

{cta(TIQ, "See Ibiza boat trips on Tiqets")}
'''
pages.append(("ibiza-boat-day", "Ibiza boat party guide: boat parties vs private boat hire",
  "Ibiza boat party or private boat hire? How each works, what is included, where the boats go, what to wear and what to bring.",
  "Ibiza boat party or private boat hire?",
  "Two ways to spend a day on the water, and how to pick the right one for your group.",
  "img/velero.jpg", body,
  [("What should I wear to an Ibiza boat party?", "Swimwear with a light cover-up, a hat and sunglasses you would not mind losing. Most boats ask you to go barefoot on deck, so flat sandals are easiest for the port, and bring a dry layer for the trip back."),
   ("Do Ibiza boat parties include drinks?", "It depends on the boat. Some tickets include drinks or an open bar for part of the trip, others only include the cruise and sell drinks on board. Check what your ticket includes before you book."),
   ("Is a boat party or a private boat better for a group?", "Boat parties suit small groups and solo travellers because you pay per person. For larger groups a private boat can cost about the same per person and lets you choose the music, the coves and the timing.")],
  "2026-11-10"))

# 7. Ibiza clubs (published 2026-11-10, keyword "ibiza clubs")
body = f'''
<p>Ibiza clubs are the reason most UK groups book the trip: a handful of world-famous venues packed into a small island, each with its own kind of night. This guide explains where the clubs are, how a typical night works, what to wear and how to plan the season around them, so you can choose before you book flights and a hotel.</p>

<h2>Where the Ibiza clubs are: a quick map</h2>
<p>Almost every big club sits in one of four areas, all within a short taxi ride of each other. Our <a href="/#map">interactive map of Ibiza clubs and hotel zones</a> shows them all on the island.</p>
<div class="tw"><table>
<tr><th>Area</th><th>Clubs</th><th>Type of night</th></tr>
<tr><td><b>Playa d'en Bossa</b></td><td>Ushuaïa, Hï Ibiza, DC-10 (by the airport)</td><td>Open-air daytime parties into the evening, then big indoor nights</td></tr>
<tr><td><b>Ibiza Town</b></td><td>Pacha, Lío, Club Chinois</td><td>Classic club nights by the marina, dinner-and-show venues</td></tr>
<tr><td><b>Sant Rafel</b></td><td>Amnesia, [UNVRS]</td><td>The two inland superclubs, long nights until morning</td></tr>
<tr><td><b>San Antonio</b></td><td>Eden, Es Paradis, Ibiza Rocks, O Beach</td><td>Bay-front clubs and daytime pool parties</td></tr>
</table></div>
<p>Where you sleep matters more than people expect: staying near the club you go to most saves on taxis every night. Our <a href="/guides/where-to-stay-in-ibiza.html">where to stay in Ibiza guide</a> compares the four areas.</p>

<h2>The best Ibiza clubs for each kind of night</h2>
<p>There is no single best club: it depends on what your group wants from the night. Line-ups change every season, so check who is playing before you buy.</p>
<ul>
<li><b>Ushuaïa</b> is an open-air stage around a hotel pool. Parties run in daylight and finish around midnight, which leaves time for a second venue.</li>
<li><b>Hï Ibiza</b> is across the road from Ushuaïa. It opens late and runs until the morning, so the two are often done back to back.</li>
<li><b>Pacha</b>, by the marina in Ibiza Town, has been open since 1973 and is the one with the cherries logo.</li>
<li><b>Amnesia</b> has two rooms, the Main Room and the Terrace, and is famous for sunrise through the Terrace roof.</li>
<li><b>[UNVRS]</b> opened in 2025 on the site of the former Privilege, on the road between Ibiza Town and San Antonio.</li>
<li><b>DC-10</b> is a stripped-back club right by the runway, known for underground house and techno.</li>
</ul>

<h2>Ibiza clubs in San Antonio</h2>
<p>San Antonio is where many first trips start, and it has its own club scene, so you do not have to cross the island every night. Eden and Es Paradis face each other on the bay front, a short walk from the West End, and Es Paradis is known for its water parties under a glass pyramid. By day, Ibiza Rocks and O Beach run pool parties. The bigger superclubs are a taxi or night-bus ride away. If San Antonio is your base, it is worth checking the bay-front line-ups before paying for a taxi across the island.</p>
<p><a href="{bk("San Antonio, Ibiza")}" target="_blank" rel="noopener">See hotels in San Antonio →</a></p>

<h2>When do Ibiza clubs open and close?</h2>
<p>The club season runs roughly from late April to mid October. Most of the big clubs hold their opening parties between late April and May, and their closing parties from late September into October. Openings and closings are the busiest nights of the year and the first to sell out. Our <a href="/guides/ibiza-opening-and-closing-parties.html">opening and closing parties guide</a> explains how to plan around them.</p>
<p>On a normal night, clubs only get busy well after midnight and keep going until morning, while open-air and daytime venues finish earlier. A nap and a late dinner are part of the plan.</p>

<h2>Ibiza clubs calendar for 2027</h2>
<p>Clubs usually announce their season dates between January and March, and each club publishes its own weekly line-ups once the season is confirmed. Until then, treat any 2027 date you see online as a guess. We add the dates to our <a href="/#tickets">club tickets section</a> as each club confirms them. For tickets, always buy from the club's official seller, before the night: popular nights sell out and the door is often more expensive.</p>

<h2>Dress code for Ibiza clubs</h2>
<p>Ibiza is far more relaxed than a UK city-centre club. Most people wear light, comfortable summer clothes, and the main rule is to dress for heat and a long night on your feet.</p>
<ul>
<li>Wear shoes you have already broken in: you will stand and dance for hours.</li>
<li>Smart-casual is always safe. Beachwear works at daytime pool parties, but for night clubs leave the swimwear at the hotel.</li>
<li>Take photo ID: you must be 18 or over to get in.</li>
<li>Pack light: a small bag or a phone and card in your pocket is easiest.</li>
</ul>

<h2>Getting to and from the clubs</h2>
<p>In summer, night buses link the main resorts and clubs, and they are the cheapest way home. Taxis are the hardest thing on the island to find at closing time on big nights, so agree a plan with your group before you go in, and keep your hotel address saved offline. If you hire a car for beach days, leave it at the hotel on club nights: never drive after drinking.</p>
<p>Your phone does a lot of work on a club night: e-tickets, maps, taxis and finding your mates afterwards. If your UK plan charges for roaming in Spain, a travel eSIM with a data bundle is a simple fix.</p>
{cta(ESIM, "See Spain eSIMs on Airalo", "line")}

<h2>Plan the trip around the clubs</h2>
<ol>
<li><b>Choose your main nights first</b>, then book flights for those dates. Many UK airports fly direct to Ibiza in summer.</li>
<li><b>Book the hotel near the club</b> you will go to most.</li>
<li><b>Sort the airport run</b> before you fly. See <a href="/guides/ibiza-airport-to-hotel.html">Ibiza airport to your hotel</a>.</li>
<li><b>Keep one day free</b> for the beach or a <a href="/guides/ibiza-boat-day.html">boat party</a> to recover.</li>
</ol>
{cta(FLY, "Compare flights to Ibiza")}
{cta(TAXI, "Compare airport transfers on Kiwitaxi", "line")}
{cta(TIQ, "See Ibiza boat trips on Tiqets", "line")}
<p><a href="/#flights">Or plan flights and hotels for your dates on our homepage →</a></p>
'''
pages.append(("ibiza-clubs", "Ibiza clubs: where they are, when they open and what to wear",
  "Ibiza clubs explained for UK groups: where the big clubs are, the best club for each kind of night, San Antonio clubs, opening and closing times and the dress code.",
  "Ibiza clubs: a guide for UK party trips",
  "Where the big clubs are, which one suits your group, when they open and close, and what to wear.",
  "video/club_haze.jpg", body,
  [("What are the most famous Ibiza clubs?", "The best-known names include Pacha, Amnesia, Ushuaïa, Hï Ibiza, DC-10 and [UNVRS], which opened in 2025 on the site of the former Privilege. Line-ups change every season."),
   ("Are there clubs in San Antonio, Ibiza?", "Yes. Eden and Es Paradis are on the San Antonio bay front, and Ibiza Rocks and O Beach run daytime pool parties. The bigger superclubs are a taxi or night-bus ride away."),
   ("When do Ibiza clubs open and close for the season?", "Roughly late April or May to mid October. Openings are mostly in late April and May, closings from late September into October."),
   ("Are Ibiza clubs open in November?", "No, the big clubs are closed from the end of the season in October until the next spring. A few bars and smaller venues stay open, but the club season itself starts again around late April."),
   ("Is there a dress code for Ibiza clubs?", "Ibiza is relaxed: light, smart-casual summer clothes and comfortable shoes are fine almost everywhere. Keep swimwear for daytime pool parties and bring photo ID, as you must be 18 or over.")],
  "2026-11-10", "2026-11-10"))

# 8. Flights from Manchester (published 2026-11-17, keyword "flights to ibiza from manchester")
MANFLY = tp("https://www.aviasales.com/?origin=MAN&destination=IBZ", 4114, 100)
body = f'''
<p>Flights to Ibiza from Manchester are one of the easiest ways for groups in the North West to get to the island: one airport, a short flight and, in summer, direct routes most weeks of the season. This guide covers how long the flight takes, when direct flights run, how to search for fares without overpaying, and what to sort before you land.</p>

<h2>Direct flights to Ibiza from Manchester</h2>
<p>Ibiza is a seasonal destination, and so are most of its UK routes. Several airlines fly direct from Manchester (MAN) to Ibiza (IBZ) in the summer season, roughly from spring to October, with the most choice in June, July and August. In winter direct flights are rare or stop altogether, and you may need to change planes on the way, for example in Barcelona, Madrid or Palma.</p>
<p>Airlines change their schedules every season, so we do not list them here: run a search for your own dates and the results will show which airlines fly direct and on which days.</p>
{cta(MANFLY, "Search flights from Manchester to Ibiza")}

<h2>How long are flights to Ibiza from Manchester?</h2>
<p>A direct flight from Manchester to Ibiza takes around two and a half to three hours, depending on the aircraft, the route and the wind on the day. Ibiza is one hour ahead of the UK all year, so a flight that leaves at 10am lands at around 1.30pm to 2pm local time. With a change of plane the journey can take most of the day, so check the total travel time, not just the price.</p>

<h2>Cheap flights to Ibiza from Manchester: how to search smarter</h2>
<p>Nobody can promise a price, and fares move all the time. What you can control is how and when you search:</p>
<ul>
<li><b>Be flexible by a day or two.</b> Mid-week departures are often lower than Friday and Saturday, especially in July and August.</li>
<li><b>Look at shoulder months.</b> Late May, June and September still have the parties and warm sea, usually with lower fares than the school holidays.</li>
<li><b>Book big weekends early.</b> Opening and closing weekends fill up fast. Our <a href="/guides/ibiza-opening-and-closing-parties.html">opening and closing parties guide</a> explains when dates come out.</li>
<li><b>Compare the full price.</b> Add bags and seats before you compare: a low headline fare can end up higher once a hold bag is added.</li>
<li><b>Check nearby airports too.</b> Liverpool and Leeds Bradford may also have summer routes, and moving airport can be worth it for some dates.</li>
</ul>
<p>Our <a href="/guides/ibiza-on-a-budget.html">Ibiza on a budget guide</a> has more ways to keep the whole trip down, not just the flight.</p>

<h2>Booking flights for a group</h2>
<p>Group trips are where most booking mistakes happen. A few habits make it easier:</p>
<ol>
<li><b>Agree dates and a budget first</b>, then let one person search and share the options.</li>
<li><b>Book together, or at least on the same day.</b> Fares can rise as seats sell, so the last person to book may pay more.</li>
<li><b>Names must match passports exactly.</b> Changing a name later can cost a fee.</li>
<li><b>Share hold bags sensibly.</b> One hold bag between two or three people is often cheaper than everyone paying for their own, as long as you stay within the weight limit.</li>
<li><b>Check passports now.</b> For Spain, a UK passport must have been issued less than 10 years before the day you arrive and be valid for at least three months after the day you plan to leave. Check the latest GOV.UK travel advice for Spain before you fly.</li>
</ol>

<h2>Getting to Manchester Airport</h2>
<p>Manchester Airport has its own railway station and a Metrolink tram stop, both linked to the terminals, so many groups can get there without a car. If you fly early in the morning, check that the first train or tram runs early enough, or book an airport hotel or parking the night before. Check which terminal your flight leaves from on your booking: it depends on the airline.</p>

<h2>Packing for an Ibiza trip from Manchester</h2>
<ul>
<li>Check your airline's cabin bag size before you pack: rules differ and gate fees add up.</li>
<li>Put SPF 50, sunglasses and a change of clothes in your hand luggage, in case a hold bag arrives late.</li>
<li>Bring an EU plug adaptor and a power bank.</li>
<li>Take your free UK GHIC card and travel insurance.</li>
<li>Check your phone plan for roaming charges in Spain. If they are high, a travel eSIM with a data bundle is simple to set up before you leave. <a href="{ESIM}" target="_blank" rel="noopener sponsored">See Spain eSIMs on Airalo</a>.</li>
</ul>

<h2>When you land in Ibiza</h2>
<p>Ibiza Airport is in the south of the island, close to Playa d'en Bossa and a short drive from Ibiza Town. San Antonio and Sant Rafel are further, so plan the ride before you fly. You can take the bus, queue for a taxi or pre-book a transfer with a fixed price; our <a href="/guides/ibiza-airport-to-hotel.html">Ibiza airport to hotel guide</a> compares all three. For a group landing late on a summer weekend, a pre-booked transfer is usually the least stressful option.</p>
{cta(WPICK, "Pre-book an Ibiza airport pickup with Welcome Pickups", "line")}
{cta(TAXI, "Compare airport transfers on Kiwitaxi", "line")}
<p>Not sure where to stay yet? Our <a href="/guides/where-to-stay-in-ibiza.html">where to stay in Ibiza guide</a> compares the four main party areas.</p>

<h2>If your flight is delayed or cancelled</h2>
<p>If your flight arrives more than three hours late or is cancelled, you may be owed compensation under UK and EU rules. You can claim from the airline directly for free, or use a claims company that only charges if you are paid.</p>
{cta(DELAY, "Check your flight with AirHelp", "line")}

<h2>Plan the whole trip</h2>
<p>Pick Manchester as your airport on our homepage planner, set your dates and number of travellers, and it builds the flight and hotel searches for you.</p>
<p><a href="/?from=MAN#flights">Plan flights and hotels from Manchester for your dates →</a></p>
'''
pages.append(("flights-to-ibiza-from-manchester", "Flights to Ibiza from Manchester: flight time, direct routes and tips",
  "Flights to Ibiza from Manchester explained: how long the flight takes, when direct flights run, how to search for cheaper fares, group booking tips and what to book before you land.",
  "Flights to Ibiza from Manchester: a guide for UK groups",
  "How long the flight is, when direct routes run, how to search for fares and what to sort before you land.",
  "img/es_vedra_1.jpg", body,
  [("How long are flights to Ibiza from Manchester?", "A direct flight takes around two and a half to three hours. Ibiza is one hour ahead of the UK, so add an hour when you work out your local arrival time."),
   ("Are there direct flights to Ibiza from Manchester?", "Yes, in the summer season several airlines fly direct from Manchester to Ibiza. In winter direct flights are rare, so you may need to change in Spain. Search your dates to see which airlines fly direct."),
   ("How can I find cheap flights to Ibiza from Manchester?", "Be flexible by a day or two, look at late May, June or September, compare the price with bags included and book big weekends early. Fares change all the time, so compare before you book."),
   ("When is the best time to fly to Ibiza from Manchester for the parties?", "The club season runs roughly from late April to mid October. June and September have the parties with fewer crowds than July and August, while opening and closing weekends are the busiest."),
   ("What should I book before landing in Ibiza?", "Your hotel, club tickets for the big nights and a way from the airport to your hotel. A pre-booked transfer has a fixed price and is the easiest option for a group arriving late.")],
  "2026-11-17", "2026-11-17"))

# 9. Flights from London (published 2026-11-24, keyword "flights to ibiza from london")
LONFLY = tp("https://www.aviasales.com/?origin=LON&destination=IBZ", 4114, 100)
body = f'''
<p>Flights to Ibiza from London are the most common way UK groups start a party trip: the capital has several airports, the flight is short and in summer there are direct routes from more than one of them. This guide compares the London airports, explains how long the flight takes and when direct flights run, and gives practical tips for booking as a group.</p>

<h2>Which London airport for flights to Ibiza?</h2>
<p>"London" covers several airports, and which ones have direct routes to Ibiza (IBZ) changes from season to season. When you search with London as the origin, the results include all of them, so you can compare times and fares in one go. Here is what each airport is like to get to:</p>
<ul>
<li><b>Gatwick (LGW)</b> is south of London, with two terminals, North and South. The Gatwick Express runs from London Victoria, and Thameslink and Southern trains also stop at the airport station.</li>
<li><b>Stansted (STN)</b> is north-east of London, in Essex, with one terminal. The Stansted Express runs from London Liverpool Street.</li>
<li><b>Luton (LTN)</b> is north of London. Take a train to Luton Airport Parkway, then the short DART shuttle to the terminal.</li>
<li><b>Heathrow (LHR)</b> is west of London and linked by the Elizabeth line, the Piccadilly line and the Heathrow Express from Paddington. Check which terminal your flight uses.</li>
<li><b>London City (LCY)</b> is in east London, on the DLR. It is small and quick to get through, but has fewer routes to the Balearics.</li>
</ul>
<p>The best airport for your group is usually the one that is easiest for most of you to reach at the time of the flight. A cheaper fare from the far side of London can cost more once you add an early taxi or a night in an airport hotel.</p>
{cta(LONFLY, "Search flights from London to Ibiza")}

<h2>Direct flights to Ibiza from London</h2>
<p>Ibiza is a seasonal island and most UK routes follow the club season. Several airlines fly direct from London to Ibiza in summer, roughly from spring to October, with the most choice in June, July and August. In winter direct flights are rare or stop, and you may need to change in Spain, for example in Barcelona, Madrid or Palma.</p>
<p>Airlines and schedules change every year, so we do not list them here: search your own dates and the results show which airlines fly direct, from which London airport and on which days.</p>

<h2>How long is the flight from London to Ibiza?</h2>
<p>A direct flight from London to Ibiza takes around two and a half hours, give or take a little depending on the airport, the aircraft and the wind. Ibiza is one hour ahead of the UK all year, so a flight that leaves Gatwick at 9am lands at around 12.30pm local time. If you change planes, the trip can take most of the day, so compare the total journey time as well as the fare.</p>

<h2>Cheap flights to Ibiza from London: how to search smarter</h2>
<p>Nobody can promise a price, and fares move all the time. What you can control is how you search:</p>
<ul>
<li><b>Compare all London airports at once.</b> Search with London as the origin rather than one airport.</li>
<li><b>Be flexible by a day or two.</b> Mid-week flights are often lower than Friday and Saturday in peak summer.</li>
<li><b>Look at late May, June and September.</b> The clubs are open and the sea is warm, usually with lower fares than the school holidays.</li>
<li><b>Book opening and closing weekends early.</b> They fill fast; our <a href="/guides/ibiza-opening-and-closing-parties.html">opening and closing parties guide</a> explains when dates are announced.</li>
<li><b>Compare the full price.</b> Add hold bags and seats before you compare, as extras can change which flight is lower.</li>
</ul>
<p>For more ways to keep the whole trip down, see our <a href="/guides/ibiza-on-a-budget.html">Ibiza on a budget guide</a>.</p>

<h2>Booking London to Ibiza flights for a group</h2>
<ol>
<li><b>Agree dates, airport and budget first</b>, then let one person search and share the options.</li>
<li><b>Book on the same day.</b> Fares can rise as seats sell, so the last person to book may pay more.</li>
<li><b>Names must match passports exactly.</b> Changing a name later can cost a fee.</li>
<li><b>Share hold bags sensibly.</b> One hold bag between two or three people can work out cheaper, as long as you stay within the weight limit.</li>
<li><b>Check passports now.</b> For Spain, a UK passport must have been issued less than 10 years before the day you arrive and be valid for at least three months after the day you plan to leave. Check the latest GOV.UK travel advice for Spain before you fly.</li>
</ol>

<h2>Early flights from London: getting to the airport</h2>
<p>Many summer flights to Ibiza leave early in the morning. Before you book a dawn departure, check that the first train from your part of London reaches the airport in time, and allow for security queues on summer weekends. If it does not work, an airport hotel the night before or a pre-booked taxi is often less stressful than a long night with no sleep before a week of parties.</p>

<h2>What to pack in your hand luggage</h2>
<ul>
<li>Check your airline's cabin bag size before you pack: rules differ and gate fees add up.</li>
<li>Keep SPF 50, sunglasses and a change of clothes in your hand luggage in case a hold bag is late.</li>
<li>Bring an EU plug adaptor, a power bank, your free UK GHIC card and travel insurance details.</li>
<li>Check your phone plan for roaming charges in Spain. If they are high, a travel eSIM is easy to set up before you leave. <a href="{ESIM}" target="_blank" rel="noopener sponsored">See Spain eSIMs on Airalo</a>.</li>
</ul>

<h2>When you land in Ibiza</h2>
<p>Ibiza Airport is in the south of the island, close to Playa d'en Bossa and a short drive from Ibiza Town; San Antonio is further. You can take the bus, queue for a taxi or pre-book a transfer with a fixed price, and our <a href="/guides/ibiza-airport-to-hotel.html">Ibiza airport to hotel guide</a> compares all three. For a group landing on a busy summer weekend, a pre-booked transfer saves the taxi queue.</p>
{cta(WPICK, "Pre-book an Ibiza airport pickup with Welcome Pickups", "line")}
{cta(TAXI, "Compare airport transfers on Kiwitaxi", "line")}
<p>Still choosing a base? Our <a href="/guides/where-to-stay-in-ibiza.html">where to stay in Ibiza guide</a> compares the main party areas, and <a href="/guides/ibiza-clubs.html">our Ibiza clubs guide</a> shows where the big clubs are.</p>

<h2>If your flight is delayed or cancelled</h2>
<p>If your flight arrives more than three hours late or is cancelled, you may be owed compensation under UK and EU rules. You can claim from the airline directly for free, or use a claims company that only charges if you are paid.</p>
{cta(DELAY, "Check your flight with AirHelp", "line")}

<h2>Plan the whole trip</h2>
<p>Pick London on our homepage planner, set your dates and number of travellers, and it builds the flight and hotel searches for you.</p>
<p><a href="/?from=LON#flights">Plan flights and hotels from London for your dates →</a></p>
'''
pages.append(("flights-to-ibiza-from-london", "Flights to Ibiza from London: Gatwick, Stansted, Luton and Heathrow",
  "Flights to Ibiza from London explained: which London airport to fly from, how long the flight takes, when direct flights run, how to search for cheaper fares and group booking tips.",
  "Flights to Ibiza from London: a guide for UK groups",
  "Which London airport to use, how long the flight is, when direct routes run and what to sort before you land.",
  "img/islas_mar.jpg", body,
  [("How long is the flight from London to Ibiza?", "A direct flight takes around two and a half hours. Ibiza is one hour ahead of the UK, so add an hour when you work out your local arrival time."),
   ("Which London airports have flights to Ibiza?", "Direct routes change each season and can include Gatwick, Stansted, Luton and Heathrow. Search with London as the origin to compare every London airport for your dates."),
   ("Are there direct flights to Ibiza from London all year?", "No. Most direct flights run in the summer season, roughly spring to October. In winter you may need to change planes in Spain."),
   ("How can I find cheap flights to Ibiza from London?", "Compare all London airports at once, be flexible by a day or two, look at late May, June or September and compare prices with bags included. Fares change all the time, so check before you book."),
   ("How do I get to Gatwick or Stansted for an early flight?", "The Gatwick Express runs from London Victoria and the Stansted Express from Liverpool Street. For a very early flight, check the first train for your date or stay at an airport hotel the night before.")],
  "2026-11-24", "2026-11-24"))

for slug, title, desc, h1, lede, img, body, *rest in pages:
    faqs = rest[0] if rest else None
    updated = rest[1] if len(rest) > 1 else "2026-11-02"
    published = rest[2] if len(rest) > 2 else "2026-11-02"
    open(f"{OUT}/{slug}.html", "w", encoding="utf-8").write(page(slug, title, desc, h1, lede, img, body, faqs, updated, published))

# index
cards = "".join(f'<a class="card" href="/guides/{s}.html"><img src="/{img}" alt="" loading="lazy"><div><h2>{h1}</h2><p>{lede}</p></div></a>'
                for s, t, d, h1, lede, img, *_ in sorted(pages, key=lambda p: p[9] if len(p) > 9 else "2026-11-02", reverse=True))
idx = page("index", "Ibiza guides for UK party travellers · Ibiza Party Flights",
           "Practical Ibiza guides for UK party trips: flights from London and Manchester, Ibiza clubs, where to stay, airport transfers, budget tips, first-timer advice, opening and closing parties and boat parties.",
           "Ibiza guides", "Straight answers for planning a party trip to Ibiza from the UK.", None,
           f'</article><div class="cards">{cards}</div><article>')
open(f"{OUT}/index.html", "w", encoding="utf-8").write(idx)
print("ok", len(pages))
