const IMG = n => `file://${process.cwd()}/${n}.jpg`;
const logo = `<svg width="54" height="54" viewBox="0 0 30 30"><circle cx="15" cy="15" r="14.2" fill="#0E1726" stroke="#ffffff" stroke-width="1.6"/><circle cx="15" cy="17" r="6.5" fill="#E8582A"/></svg>`;
const brand = `<div class="brand">${logo}<span>Ibiza Party Flights</span></div>`;
const cover = (img, kicker, title, sub, n, total) => `<div class="s cover" style="background-image:linear-gradient(180deg,rgba(14,23,38,.15) 0%,rgba(14,23,38,.25) 40%,rgba(14,23,38,.92) 100%),url(${IMG(img)})">
 ${brand}<div class="bottom"><div class="kicker">${kicker}</div><h1>${title}</h1><p class="sub">${sub}</p><div class="swipe">Swipe →</div></div><div class="num">${n}/${total}</div></div>`;
const card = (kicker, title, body, n, total, tag="") => `<div class="s card">${brand}
 <div class="mid">${tag?`<div class="tag">${tag}</div>`:""}<div class="kicker">${kicker}</div><h2>${title}</h2><div class="body">${body}</div></div><div class="num">${n}/${total}</div></div>`;
const cta = (title, body, n, total) => `<div class="s ctaS">${brand}<div class="mid"><h2>${title}</h2><div class="body">${body}</div>
 <div class="url">ibizapartyflights.co.uk</div><div class="small">Link in bio · @ibizapartyflights</div></div><div class="num">${n}/${total}</div></div>`;
const sets = {
 c1: [
  cover("piscina","Ibiza 2027","Your Ibiza party trip, planned in one place","✈️ Flights + 🪩 Parties + 🏨 Hotels",1,4),
  card("How it works","3 steps. Ibiza sorted.",`<ol><li><b>Pick your party</b><br>Openings, closings and the big nights.</li><li><b>Fly from your UK airport</b><br>We match flights to the party dates.</li><li><b>Sleep near the club</b><br>Hotels by area + airport transfer.</li></ol>`,2,4),
  card("No booking fee","You book direct with the sellers",`<p>Flights, hotels, transfers and tickets are booked with the companies that sell them.</p><p>You pay their price. If you book through our links we may earn a commission. It never changes your price.</p>`,3,4),
  cta("Follow for 2027 dates & tips","<p>Club opening dates drop early in the year. Follow so you plan before prices go up.</p>",4,4)],
 c2: [
  cover("hotel_playa","Where to stay","Ibiza for clubbing: 4 areas, honestly explained","Save this before you book 📌",1,6),
  card("Playa d'en Bossa","Next to Ushuaïa & Hï Ibiza","<p>Long beach and the main day-to-night clubs on one strip.</p><p><b>Good for:</b> big club nights on foot.<br><b>Heads up:</b> busy and loud in peak season.</p>",2,6,"1"),
  card("Ibiza Town","Near Pacha & the marina","<p>Old town, restaurants and the marina. Short taxis to the rest of the island.</p><p><b>Good for:</b> party + food + a bit of culture.</p>",3,6,"2"),
  card("Sant Rafel","Closest to [UNVRS] & Amnesia","<p>Inland, between Ibiza Town and San Antonio. Quieter.</p><p><b>Good for:</b> nights at the big inland clubs.</p>",4,6,"3"),
  card("San Antonio","Sunset bars & pool parties","<p>West coast sunsets, bars and pool parties. Usually the cheapest of the four.</p><p><b>Good for:</b> lads' and girls' holidays on a budget.</p>",5,6,"4"),
  cta("Compare hotels by area","<p>Pick your party dates and see hotels in each area on Booking.com.</p>",6,6)],
 c3: [
  cover("playa_gente","Ibiza airport","Landed. Now what? Airport → hotel, 3 ways","Save for your trip 📌",1,5),
  card("Option 1","Bus","<p>The cheapest way. In summer, buses run from the airport to Ibiza Town, Playa d'en Bossa and San Antonio.</p><p><b>Heads up:</b> can be packed with luggage at peak times.</p>",2,5,"1"),
  card("Option 2","Taxi","<p>Taxi rank outside arrivals, metered fares.</p><p><b>Heads up:</b> queues can be long on busy summer nights.</p>",3,5,"2"),
  card("Option 3","Pre-booked transfer","<p>Price fixed before you fly. Driver waits at arrivals. Cars and minivans for groups.</p><p class='ad'>Ad · we may earn a commission if you book through our link.</p>",4,5,"3"),
  cta("Party nights: never drive","<p>Book a taxi or transfer back from the club. Book your airport transfer in advance.</p>",5,5)]
};
module.exports = sets;
