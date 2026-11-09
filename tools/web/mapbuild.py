#!/usr/bin/env python3
"""Adds the interactive island map panel to the homepage. Usage: mapbuild.py <index.html>"""
import sys, json, html

W, H = 600, 504
LON0, LON1, LAT0, LAT1 = 1.17, 1.67, 38.82, 39.14
def P(lat, lon):
    return (round((lon - LON0) / (LON1 - LON0) * W, 1), round((LAT1 - lat) / (LAT1 - LAT0) * H, 1))

COAST = [(39.118,1.515),(39.123,1.535),(39.110,1.548),(39.098,1.570),(39.082,1.590),(39.088,1.615),(39.074,1.600),
 (39.055,1.600),(39.040,1.612),(39.036,1.626),(39.026,1.612),(39.014,1.590),(39.003,1.582),(38.990,1.585),(38.985,1.560),
 (38.982,1.535),(38.972,1.528),(38.955,1.522),(38.944,1.530),(38.932,1.500),(38.918,1.480),(38.917,1.458),(38.903,1.458),
 (38.908,1.440),(38.903,1.432),(38.890,1.412),(38.872,1.402),(38.858,1.408),(38.838,1.407),(38.843,1.388),(38.840,1.366),
 (38.858,1.358),(38.866,1.336),(38.870,1.318),(38.860,1.302),(38.870,1.285),(38.866,1.262),(38.855,1.243),(38.872,1.228),
 (38.890,1.222),(38.914,1.220),(38.928,1.228),(38.942,1.232),(38.955,1.218),(38.966,1.216),(38.972,1.240),(38.968,1.268),
 (38.972,1.292),(38.981,1.305),(38.990,1.296),(38.997,1.284),(39.008,1.297),(39.022,1.290),(39.035,1.305),(39.048,1.322),
 (39.060,1.345),(39.068,1.370),(39.082,1.385),(39.085,1.410),(39.082,1.428),(39.092,1.450),(39.100,1.468),(39.106,1.488),
 (39.112,1.502)]

def smooth(pts):
    n = len(pts); d = f"M{pts[0][0]},{pts[0][1]}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i-1) % n], pts[i], pts[(i+1) % n], pts[(i+2) % n]
        c1 = (p1[0] + (p2[0]-p0[0]) / 6, p1[1] + (p2[1]-p0[1]) / 6)
        c2 = (p2[0] - (p3[0]-p1[0]) / 6, p2[1] - (p3[1]-p1[1]) / 6)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}"
    return d + "Z"

pts = [P(a, b) for a, b in COAST]
ISLAND = smooth(pts)
cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)

def blob(lat, lon, r):
    x, y = P(lat, lon)
    return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.7:.1f}" transform="rotate(-25 {x} {y})"/>'
ISLETS = blob(38.866, 1.198, 5) + blob(38.985, 1.212, 7) + blob(39.037, 1.648, 6)

CT = "https://www.clubtickets.com/"
# k: s = stay zone, c = club. Facts kept general on purpose: no prices, no line-ups, no 2027 dates.
POINTS = [
 dict(k="s", n="Playa d'en Bossa", lat=38.893, lon=1.412, q="Playa d'en Bossa", near="Ushuaïa · Hï Ibiza",
      d="The island's longest beach and its busiest party strip. Walk to the two big clubs, ten minutes from the airport."),
 dict(k="s", n="Ibiza Town", lat=38.910, lon=1.428, q="Ibiza Town", near="Pacha · Lío · Club Chinois",
      d="The capital: the old walled town, the marina and the port bars. Good base if you want dinner and a club in one walk."),
 dict(k="s", n="Talamanca", lat=38.925, lon=1.463, q="Talamanca, Ibiza", near="Pacha · the marina",
      d="A calm bay just round the corner from the marina. Quieter nights, short ride to Ibiza Town."),
 dict(k="s", n="Sant Rafel", lat=38.967, lon=1.413, q="Sant Rafel de Sa Creu", near="Amnesia · [UNVRS]",
      d="A village in the middle of the island, between the two superclubs. No beach, so plan your daytime rides."),
 dict(k="s", n="San Antonio", lat=38.961, lon=1.313, q="San Antonio, Ibiza", near="Eden · Es Paradis · Ibiza Rocks · O Beach",
      d="West coast bay, known for its sunsets and the widest choice of budget stays."),
 dict(k="s", n="Santa Eulària", lat=38.991, lon=1.531, q="Santa Eulalia del Rio", near="Akasha (Sant Carles)",
      d="East coast town with a promenade and restaurants. The relaxed option: clubs are a taxi ride away."),
 dict(k="s", n="Portinatx", lat=39.106, lon=1.516, q="Portinatx", near="none nearby",
      d="The far north: coves and clear water. For a recovery stay, well away from the clubs."),
 dict(k="c", n="Ushuaïa Ibiza", lat=38.886, lon=1.402, t="Open-air club · daytime into evening", a="Playa d'en Bossa", z=0,
      u="https://www.clubtickets.com/clubbing/ushuaia-ibiza", d="Open-air stage around a hotel pool. Parties run in daylight and finish around midnight."),
 dict(k="c", n="Hï Ibiza", lat=38.877, lon=1.396, t="Night club", a="Playa d'en Bossa", z=0,
      u="https://www.clubtickets.com/clubbing/hi-ibiza", d="Across the road from Ushuaïa. Opens late and runs until the morning."),
 dict(k="c", n="Pacha", lat=38.922, lon=1.440, t="Night club", a="Ibiza Town", z=1,
      u=CT, d="By the marina in Ibiza Town, open since 1973. The one with the cherries."),
 dict(k="c", n="Club Chinois", lat=38.914, lon=1.449, t="Night club", a="Ibiza Town marina", z=1,
      u=CT, d="A smaller club at the marina, close to the port restaurants."),
 dict(k="c", n="Lío", lat=38.905, lon=1.452, t="Cabaret restaurant and club", a="Ibiza Town marina", z=1,
      u=CT, d="Dinner with a cabaret show that turns into a club after midnight."),
 dict(k="c", n="[UNVRS]", lat=38.958, lon=1.394, t="Superclub", a="Sant Rafel", z=3,
      u="https://www.clubtickets.com/clubbing/unvrs-ibiza", d="Opened in 2025 on the site of the former Privilege, on the road between Ibiza Town and San Antonio."),
 dict(k="c", n="Amnesia", lat=38.948, lon=1.408, t="Superclub", a="Sant Rafel", z=3,
      u=CT, d="Two rooms, the Main Room and the Terrace. Famous for sunrise through the Terrace roof."),
 dict(k="c", n="DC-10", lat=38.872, lon=1.380, t="Club · day and night sessions", a="Next to the airport", z=0,
      u=CT, d="A stripped-back club right by the runway, known for underground house and techno."),
 dict(k="c", n="Eden", lat=38.983, lon=1.311, t="Night club", a="San Antonio", z=4,
      u=CT, d="On the San Antonio bay front, a short walk from the West End."),
 dict(k="c", n="Es Paradis", lat=38.974, lon=1.319, t="Night club", a="San Antonio", z=4,
      u=CT, d="Opposite Eden, under a glass pyramid. Known for its water parties."),
 dict(k="c", n="Ibiza Rocks", lat=38.992, lon=1.303, t="Hotel pool parties · daytime", a="San Antonio", z=4,
      u=CT, d="A hotel built around a stage and a pool. Daytime parties through the season."),
 dict(k="c", n="O Beach", lat=38.970, lon=1.299, t="Pool club · daytime", a="San Antonio bay", z=4,
      u=CT, d="Daytime pool club on the bay, with beds and shows."),
 dict(k="c", n="Pikes", lat=38.997, lon=1.327, t="Hotel with small parties", a="Hills above San Antonio", z=4,
      u="", d="A hotel in an old farmhouse with intimate parties. Entry is limited, so check with the venue."),
 dict(k="c", n="528 Ibiza", lat=38.985, lon=1.343, t="Open-air venue", a="Hills above San Antonio", z=4,
      u=CT, d="Open-air venue in the hills, formerly Benimussa Park."),
 dict(k="c", n="Cova Santa", lat=38.903, lon=1.345, t="Restaurant and open-air venue", a="Sant Josep road", z=1,
      u=CT, d="Terraces built around a natural cave, inland on the road to Sant Josep."),
 dict(k="c", n="Akasha", lat=39.030, lon=1.563, t="Small club", a="Sant Carles (Las Dalias)", z=5,
      u=CT, d="An intimate club at Las Dalias, the market venue in the north-east."),
]
for p in POINTS:
    p["x"], p["y"] = P(p["lat"], p["lon"])

def pin(i, p):
    kind = "stay" if p["k"] == "s" else "club"
    label = html.escape(f'{p["n"]}, {"hotel zone" if kind == "stay" else "club, " + p["a"]}', quote=True)
    if kind == "stay":
        shape = '<circle class="halo" r="20"/><circle class="pulse" r="20"/><rect class="mk" x="-5.5" y="-5.5" width="11" height="11"/>'
    else:
        shape = '<circle class="pulse" r="11"/><rect class="mk" x="-5" y="-5" width="10" height="10" transform="rotate(45)"/>'
    return (f'<g class="pin {kind}" data-i="{i}" tabindex="0" role="button" aria-label="{label}" '
            f'transform="translate({p["x"]},{p["y"]})"><circle class="hit" r="15"/>{shape}<circle class="sel" r="13"/></g>')

# stay zones first so club pins sit on top
PINS = "".join(pin(i, p) for i, p in enumerate(POINTS) if p["k"] == "s") + "".join(pin(i, p) for i, p in enumerate(POINTS) if p["k"] == "c")
CHIPS = "".join(f'<button type="button" class="chip {"stay" if p["k"]=="s" else "club"}" data-i="{i}">{html.escape(p["n"])}</button>' for i, p in enumerate(POINTS))

ax, ay = P(38.881, 1.362)
def lab(lat, lon, t, anchor="start"):
    x, y = P(lat, lon); return f'<text x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'
LABELS = (lab(39.012, 1.262, "SANT ANTONI", "end") + lab(38.898, 1.478, "EIVISSA") + lab(38.972, 1.556, "STA EULÀRIA")
          + lab(39.126, 1.548, "PORTINATX") + lab(38.846, 1.196, "ES VEDRÀ") + lab(38.893, 1.352, "IBZ", "end"))

contours = "".join(f'<use href="#isl" transform="translate({cx*(1-s):.1f},{cy*(1-s):.1f}) scale({s})" opacity="{o}"/>'
                   for s, o in ((.86,.5),(.7,.4),(.52,.32),(.34,.25)))
grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(60, W, 60)) + "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(63, H, 63))
rings = "".join(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}"/>' for r in (90, 170, 250, 330))

SVG = f'''<svg class="isle" id="isle" viewBox="0 0 {W} {H}" role="group" aria-label="Map of Ibiza with hotel zones and clubs">
  <defs>
    <path id="isl" d="{ISLAND}"/>
    <clipPath id="islClip"><use href="#isl"/></clipPath>
    <linearGradient id="islFill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3150FF" stop-opacity=".55"/><stop offset=".55" stop-color="#0A1A8F" stop-opacity=".75"/><stop offset="1" stop-color="#7B3CFF" stop-opacity=".5"/></linearGradient>
    <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#38E1FF" fill-opacity=".35"/></pattern>
    <linearGradient id="sweepG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C8FF2E" stop-opacity="0"/><stop offset="1" stop-color="#C8FF2E" stop-opacity=".3"/></linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g class="seagrid" aria-hidden="true">{grid}</g>
  <g class="rings" aria-hidden="true">{rings}</g>
  <g aria-hidden="true">
    <use href="#isl" class="shadow" transform="translate(0,10)"/>
    <use href="#isl" fill="url(#islFill)"/>
    <g clip-path="url(#islClip)"><rect width="{W}" height="{H}" fill="url(#dots)"/><g class="contours">{contours}</g>
      <g class="sweep"><path d="M{cx:.0f},{cy:.0f} L{cx+420:.0f},{cy-70:.0f} A426,426 0 0 1 {cx+420:.0f},{cy+70:.0f}Z" fill="url(#sweepG)"/></g></g>
    <use href="#isl" class="coast" filter="url(#glow)"/>
    <g class="islets">{ISLETS}</g>
    <g class="labels">{LABELS}</g>
    <g class="plane" transform="translate({ax},{ay})"><circle r="9"/><path d="M0,-6 L1.6,-1.5 L6.5,1.5 L6.5,3 L1.6,1.6 L1.2,4.6 L2.8,5.8 L2.8,6.8 L0,6 L-2.8,6.8 L-2.8,5.8 L-1.2,4.6 L-1.6,1.6 L-6.5,3 L-6.5,1.5 L-1.6,-1.5Z" transform="rotate(45) scale(.8)"/></g>
    <g class="cross" id="cross"><line id="crossX" x1="0" x2="{W}" y1="0" y2="0"/><line id="crossY" y1="0" y2="{H}" x1="0" x2="0"/></g>
  </g>
  <g id="pins">{PINS}</g>
  <text class="readout" id="readout" x="6" y="{H-8}" text-anchor="start" aria-hidden="true">38.98°N 1.43°E</text>
</svg>'''

SECTION = f'''  <!-- ISLAND MAP -->
  <section class="panel gut" id="map" data-label="MAP">
    <div class="inner mapwrap">
      <div class="maphead anim">
        <div class="step"><b>MAP</b>THE ISLAND AT A GLANCE</div>
        <h2 class="scr">Where to stay, where to party</h2>
      </div>
      <div class="mapstage">
        <div class="maptabs" role="group" aria-label="Show on map">
          <button type="button" class="on" data-f="all" aria-pressed="true">ALL</button><button type="button" data-f="stay" aria-pressed="false"><i class="sq"></i>STAY</button><button type="button" data-f="club" aria-pressed="false"><i class="di"></i>CLUBS</button>
        </div>
        {SVG}
      </div>
      <div class="mapside">
        <div class="card mapinfo" id="mapinfo" aria-live="polite">
          <span class="mono cmd" id="miCmd">&gt; scan --island IBIZA</span>
          <h3 id="miName">Pick a point</h3>
          <p class="mono mitag" id="miTag">HOVER OR TAP THE MAP</p>
          <p class="midesc" id="miDesc">Squares are hotel zones, diamonds are clubs. Choose one to see what it is, what is nearby and where to book.</p>
          <dl class="mikv" id="miKv"></dl>
          <div class="miact"><a class="btn lime" id="miGo" href="#" target="_blank" rel="noopener" hidden></a><button type="button" class="btn" id="miZone" hidden></button></div>
          <p class="small" id="miSmall">stylised map · positions are approximate</p>
        </div>
        <div class="chips" id="chips" aria-label="All points">{CHIPS}</div>
      </div>
    </div>
    <a class="next" href="#transfers">NEXT: AIRPORT RIDE <i>↓</i></a>
  </section>

'''

CSS = '''
/* island map */
#map{background:radial-gradient(ellipse 80% 60% at 35% 50%,#0A1A8F 0%,#06106A 45%,#0B0B0D 100%)}
.mapwrap{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,380px);grid-template-areas:"head head" "stage side";gap:14px 28px;align-items:center}
.maphead{grid-area:head}.mapstage{grid-area:stage;position:relative;min-width:0}.mapside{grid-area:side;min-width:0;display:grid;gap:12px}
.maphead h2{font-weight:900;text-transform:uppercase;font-size:clamp(26px,4.2vw,54px);line-height:.92;letter-spacing:-.03em;margin:10px 0 0}
.isle{display:block;width:100%;height:auto;max-height:min(62svh,560px);overflow:visible;transform:perspective(1200px) rotateX(calc(var(--trx,0deg)*.6 + 8deg)) rotateY(calc(var(--try,0deg)*.5));transition:transform .3s ease-out}
.seagrid line{stroke:#38E1FF;stroke-opacity:.09;stroke-width:1}
.rings circle{fill:none;stroke:#38E1FF;stroke-opacity:.13;stroke-dasharray:2 7}
.isle .shadow{fill:#000;opacity:.35}
.isle .coast{fill:none;stroke:#38E1FF;stroke-width:1.6}
.contours use{fill:none;stroke:#C8FF2E;stroke-width:1}
.islets ellipse{fill:#3150FF;fill-opacity:.5;stroke:#38E1FF;stroke-width:1}
.labels text{font:500 11px var(--mono);letter-spacing:.08em;fill:#F2F2F2;fill-opacity:.7}
.plane circle{fill:#0B0B0D;stroke:#F2F2F2;stroke-opacity:.6}.plane path{fill:#F2F2F2}
.cross line{stroke:#C8FF2E;stroke-opacity:.55;stroke-width:1;stroke-dasharray:3 5}.cross{opacity:0;transition:opacity .2s}.isle.has-sel .cross{opacity:1}
.readout{font:500 12px var(--mono);letter-spacing:.06em;fill:#C8FF2E}
.pin{cursor:pointer;outline:none}
.pin .hit{fill:transparent}
.pin .halo{fill:#C8FF2E;fill-opacity:.12;stroke:#C8FF2E;stroke-opacity:.5;stroke-dasharray:2 4}
.pin.stay .mk{fill:#C8FF2E;stroke:#0B0B0D;stroke-width:1.5}
.pin.club .mk{fill:#38E1FF;stroke:#0B0B0D;stroke-width:1.5}
.pin .pulse{fill:none;stroke-width:1.5;opacity:0}
.pin.stay .pulse{stroke:#C8FF2E}.pin.club .pulse{stroke:#38E1FF}
.pin .sel{fill:none;stroke:#fff;stroke-width:2;opacity:0}
.pin.on .sel,.pin:focus-visible .sel{opacity:1}
.pin.on .mk{fill:#fff}
.isle.f-stay .pin.club,.isle.f-club .pin.stay{opacity:.12;pointer-events:none}
@media (prefers-reduced-motion:no-preference){
  .sweep{transform-origin:''' + f"{cx:.0f}px {cy:.0f}px" + ''';animation:sweep 7s linear infinite}
  @keyframes sweep{to{transform:rotate(360deg)}}
  .pin .pulse{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite}
  .pin.club .pulse{animation-delay:.9s}
  @keyframes ping{0%{transform:scale(.4);opacity:.9}100%{transform:scale(1.5);opacity:0}}
  .pin .sel{transform-box:fill-box;transform-origin:center}.pin.on .sel{animation:selp 1.2s ease-in-out infinite}
  @keyframes selp{50%{transform:scale(1.25)}}
}
.maptabs{position:absolute;left:0;top:0;z-index:2;display:flex;gap:6px}
.maptabs button{font:500 11px var(--mono);letter-spacing:.06em;color:var(--ink);background:rgba(11,11,13,.7);border:1px solid #33333B;padding:7px 10px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.maptabs button.on{background:var(--lime);color:#000;border-color:var(--lime)}
.maptabs .sq{width:8px;height:8px;background:var(--lime);display:block}.maptabs .di{width:8px;height:8px;background:var(--cyan);display:block;transform:rotate(45deg)}
.maptabs button.on .sq,.maptabs button.on .di{background:#000}
.mapinfo{border-color:#3150FF;box-shadow:0 0 0 1px rgba(56,225,255,.15),0 0 40px rgba(49,80,255,.25);min-height:268px}
.mapinfo h3{font-weight:900;text-transform:uppercase;font-size:clamp(22px,2.6vw,30px);line-height:1;letter-spacing:-.02em;margin:0 0 6px}
.mitag{color:var(--cyan);margin:0 0 10px}
.midesc{margin:0 0 12px;font-size:14.5px;line-height:1.45;color:#D8D8DE}
.mikv{margin:0 0 14px;display:grid;gap:0;border-top:1px solid #2E2E36}
.mikv div{display:grid;grid-template-columns:104px 1fr;gap:10px;padding:7px 0;border-bottom:1px solid #2E2E36;font-family:var(--mono);font-size:11.5px}
.mikv dt{color:var(--dim);letter-spacing:.06em}.mikv dd{margin:0;color:var(--ink)}
.miact{display:flex;gap:8px;flex-wrap:wrap}
.miact .btn{padding:11px 14px;font-size:12.5px}
.chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px;scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.chip{flex:none;font:500 11px var(--mono);letter-spacing:.04em;color:var(--ink);background:rgba(11,11,13,.6);border:1px solid #33333B;padding:7px 10px;cursor:pointer;white-space:nowrap}
.chip.stay{border-left:3px solid var(--lime)}.chip.club{border-left:3px solid var(--cyan)}
.chip.on{background:#fff;color:#000;border-color:#fff}
.chips.f-stay .chip.club,.chips.f-club .chip.stay{display:none}
@media (max-width:860px){
  .mapwrap{grid-template-columns:1fr;grid-template-areas:"head" "stage" "side";gap:10px}
  .isle{max-height:34svh;transform:none}
  .maphead h2{font-size:clamp(20px,6vw,30px);margin-top:8px}
  .mapinfo h3{font-size:21px}.mapinfo .mono.cmd{margin-bottom:6px}.mitag{margin-bottom:6px}
  .mikv div:nth-child(3){display:none}
  .miact{flex-wrap:nowrap}.miact .btn{flex:1;justify-content:center;padding:10px 8px;font-size:11.5px;white-space:nowrap}
  #miSmall{display:none}
  .mapside{grid-template-areas:"chips" "info"}.chips{grid-area:chips}.mapinfo{grid-area:info;min-height:0;padding:14px}
  .midesc{font-size:13.5px;margin-bottom:8px}.mikv{margin-bottom:10px}.mikv div{padding:5px 0}
  .labels text{font-size:14px}.readout{font-size:15px}
  #map{padding-top:calc(72px + env(safe-area-inset-top,0px))}
}
'''

JS = '''
  // island map: hover, focus or tap a point to read it; hotel links use the dates from the flight form
  (function(){
    const PTS = ''' + json.dumps([{k:v for k,v in p.items()} for p in POINTS], ensure_ascii=False, separators=(",",":")) + ''';
    const isle = $("isle"), pins = [...isle.querySelectorAll(".pin")], chips = [...document.querySelectorAll("#chips .chip")], chipBox = $("chips");
    const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
    const fmt = s => s ? new Date(s + "T12:00").toLocaleDateString("en-GB",{day:"numeric",month:"short"}) : "";
    let cur = -1, touched = false, tour = null;
    function show(i, lock){
      const p = PTS[i]; if (!p) return; cur = i;
      pins.forEach(g => g.classList.toggle("on", +g.dataset.i === i));
      chips.forEach(c => { const on = +c.dataset.i === i; c.classList.toggle("on", on); if (on && lock) chipBox.scrollTo({left: c.offsetLeft - chipBox.offsetLeft - chipBox.clientWidth/2 + c.offsetWidth/2, behavior: reduce ? "auto" : "smooth"}); });
      isle.classList.add("has-sel");
      $("crossX").setAttribute("y1", p.y); $("crossX").setAttribute("y2", p.y); $("crossY").setAttribute("x1", p.x); $("crossY").setAttribute("x2", p.x);
      $("readout").textContent = p.lat.toFixed(3) + "°N " + p.lon.toFixed(3) + "°E";
      const stay = p.k === "s", go = $("miGo"), zb = $("miZone");
      $("miCmd").textContent = (stay ? "> scan --zone " : "> locate --club ") + p.n.toUpperCase().replace(/[^A-Z0-9À-Ü]+/g, "_");
      $("miName").textContent = p.n;
      $("miTag").textContent = (stay ? "HOTEL ZONE" : "CLUB · " + p.a.toUpperCase()) + " · " + p.lat.toFixed(2) + "°N " + p.lon.toFixed(2) + "°E";
      $("miDesc").textContent = p.d;
      const d = $("dep").value, r = $("ret").value, pax = $("pax").value;
      const rows = stay
        ? [["CLUBS NEARBY", p.near], ["YOUR DATES", fmt(d) + " → " + fmt(r) + " · " + pax + " guests"], ["PRICES", "Live on Booking.com"]]
        : [["TYPE", p.t], ["2027 EVENTS", "Not announced yet"], ["STAY NEARBY", PTS[p.z].n]];
      $("miKv").innerHTML = rows.map(x => "<div><dt>" + esc(x[0]) + "</dt><dd>" + esc(x[1]) + "</dd></div>").join("");
      if (stay){
        go.hidden = false; go.textContent = "Hotels and prices ↗";
        go.href = "https://www.booking.com/searchresults.html?ss=" + encodeURIComponent(p.q) + "&checkin=" + d + "&checkout=" + r + "&group_adults=" + pax;
        zb.hidden = true; $("miSmall").textContent = "opens Booking.com with the dates from your flight search";
      } else {
        go.hidden = !p.u; if (p.u){ go.href = p.u; go.textContent = "Official tickets ↗"; }
        zb.hidden = false; zb.textContent = "Hotels nearby"; zb.onclick = () => { stop(); show(p.z, true); };
        $("miSmall").textContent = p.u ? "tickets via Clubtickets · we add 2027 dates as each club confirms them" : "book direct with the venue";
      }
    }
    function stop(){ touched = true; clearInterval(tour); tour = null; }
    pins.forEach(g => { const i = +g.dataset.i;
      g.addEventListener("pointerenter", e => { if (e.pointerType === "mouse"){ stop(); show(i); } });
      g.addEventListener("click", () => { stop(); show(i, true); });
      g.addEventListener("focus", () => { stop(); show(i); });
      g.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " "){ e.preventDefault(); stop(); show(i, true); } });
    });
    chips.forEach(c => c.addEventListener("click", () => { stop(); show(+c.dataset.i, true); }));
    document.querySelectorAll(".maptabs button").forEach(b => b.addEventListener("click", () => {
      const f = b.dataset.f; stop();
      document.querySelectorAll(".maptabs button").forEach(o => { const on = o === b; o.classList.toggle("on", on); o.setAttribute("aria-pressed", on); });
      isle.classList.remove("f-stay","f-club"); chipBox.classList.remove("f-stay","f-club");
      if (f !== "all"){ isle.classList.add("f-" + f); chipBox.classList.add("f-" + f); }
      if (cur >= 0 && f !== "all" && (PTS[cur].k === "s") !== (f === "stay")) show(PTS.findIndex(p => (p.k === "s") === (f === "stay")));
    }));
    ["dep","ret","pax"].forEach(id => $(id).addEventListener("change", () => { if (cur >= 0) show(cur); }));
    // until the visitor touches the map, it tours the main points on its own
    const order = [0, 7, 8, 1, 9, 3, 12, 13, 4, 15, 14, 5];
    let step = 0;
    new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting && !touched && !tour){ show(order[step % order.length]); if (!reduce) tour = setInterval(() => { step++; show(order[step % order.length]); }, 3200); }
      else if (!e.isIntersecting && tour){ clearInterval(tour); tour = null; }
    }), {threshold:.5}).observe($("map"));
  })();
'''

path = sys.argv[1]
h = open(path, encoding="utf-8").read()
assert 'id="map"' not in h, "map already present"
def rep(a, b, count=1):
    global h
    assert h.count(a) == count, (h.count(a), a[:70]); h = h.replace(a, b)
rep("</style>\n", CSS + "</style>\n") if h.count("</style>\n") == 1 else None
rep("  <!-- 04 TRANSFERS -->", SECTION + "  <!-- 04 TRANSFERS -->") if "<!-- 04 TRANSFERS -->" in h else rep('  <section class="panel gut" id="transfers"', SECTION + '  <section class="panel gut" id="transfers"')
rep('<a class="next" href="#transfers">NEXT: AIRPORT RIDE <i>↓</i></a>\n  </section>\n\n  <!-- ISLAND MAP -->', '<a class="next" href="#map">NEXT: ISLAND MAP <i>↓</i></a>\n  </section>\n\n  <!-- ISLAND MAP -->')
rep('<a href="#tickets" data-scr>TICKETS</a>', '<a href="#tickets" data-scr>TICKETS</a><a href="#map" data-scr>MAP</a>')
rep("  // screen-to-screen transitions\n", JS + "\n  // screen-to-screen transitions\n")
open(path, "w", encoding="utf-8").write(h)
print("ok", len(h))
