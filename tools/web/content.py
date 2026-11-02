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

<h2>When is opening season?</h2>
<p>Most of the big clubs open between late April and May. Opening weekends have a special energy: everyone is back on the island, and the line-ups are announced to set the tone for the summer.</p>

<h2>When are the closing parties?</h2>
<p>Closings run from late September into mid October. In 2026 most of the big clubs closed in the second week of October. Closing parties are often the most emotional nights of the year, and the first to sell out.</p>

<h2>2027 dates</h2>
<p>Clubs usually announce their dates between January and March. We add them to our <a href="/#parties">party calendar</a> as soon as each club confirms. Until then, treat any date you see online as a guess.</p>

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
   ("When are Ibiza 2027 party dates announced?", "Clubs usually confirm their dates between January and March.")]))

# 6. Boat day
body = f'''
<p>A day on the water is the best way to recover from a night out, and the best photos of the trip. There are two main ways to do it.</p>

<h2>Boat parties</h2>
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

<p class="cta"><a class="btn line" href="https://www.getyourguide.com/s/?q=Ibiza%20boat%20party" target="_blank" rel="noopener">See Ibiza boat trips on GetYourGuide</a></p>
'''
pages.append(("ibiza-boat-day", "Ibiza boat parties vs private boat hire",
  "Boat party or private boat hire in Ibiza? What each costs to organise, what is included, where the boats go and what to bring.",
  "Ibiza boat days: boat party or private hire?",
  "Two ways to spend a day on the water, and how to pick the right one for your group.",
  "img/velero.jpg", body))

for slug, title, desc, h1, lede, img, body, *rest in pages:
    faqs = rest[0] if rest else None
    open(f"{OUT}/{slug}.html", "w", encoding="utf-8").write(page(slug, title, desc, h1, lede, img, body, faqs))

# index
cards = "".join(f'<a class="card" href="/guides/{s}.html"><img src="/{img}" alt="" loading="lazy"><div><h2>{h1}</h2><p>{lede}</p></div></a>'
                for s, t, d, h1, lede, img, *_ in pages)
idx = page("index", "Ibiza guides for UK party travellers · Ibiza Party Flights",
           "Practical Ibiza guides for UK party trips: where to stay, airport transfers, budget tips, first-timer advice, opening and closing parties and boat days.",
           "Ibiza guides", "Straight answers for planning a party trip to Ibiza from the UK.", None,
           f'</article><div class="cards">{cards}</div><article>')
open(f"{OUT}/index.html", "w", encoding="utf-8").write(idx)
print("ok", len(pages))
