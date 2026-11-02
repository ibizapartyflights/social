import json, html, os
import os; OUT=os.environ.get("OUT","../Web/guides")
MARK="793572"; TRS="588922"
from urllib.parse import quote
def tp(url,p,c): return f"https://tp.media/r?campaign_id={c}&marker={MARK}&p={p}&trs={TRS}&u={quote(url,safe='')}"
FLY=tp("https://www.aviasales.com/?destination=IBZ",4114,100)
TAXI=tp("https://kiwitaxi.com/en/spain/ibiza",647,1)
CAR=tp("https://localrent.com/en/spain/ibiza/",2043,87)
DELAY=tp("https://www.airhelp.com/en-gb/",9139,120)
ESIM="https://airalo.tpx.gr/tvyvKRQw"  # Airalo Spain eSIM
WPICK="https://tpx.gr/WPxEBccV"  # Welcome Pickups, Ibiza airport transfer
TIQ="https://tiqets.tpx.gr/heYwlurD"  # Tiqets, Ibiza attractions and boat trips
def bk(area): return "https://www.booking.com/searchresults.html?ss="+quote(area)
CSS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"guide.css")).read()
def page(slug,title,desc,h1,lede,img,body,faqs=None,updated="2026-11-02"):
    url=f"https://ibizapartyflights.co.uk/guides/{slug}.html" if slug!="index" else "https://ibizapartyflights.co.uk/guides/"
    graph=[{"@type":"Article","headline":h1,"description":desc,"image":f"https://ibizapartyflights.co.uk/{img}","datePublished":"2026-11-02","dateModified":updated,"inLanguage":"en-GB",
            "author":{"@type":"Organization","name":"Ibiza Party Flights","url":"https://ibizapartyflights.co.uk/"},"publisher":{"@id":"https://ibizapartyflights.co.uk/#org"},"mainEntityOfPage":url},
           {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ibizapartyflights.co.uk/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://ibizapartyflights.co.uk/guides/"}]+([] if slug=="index" else [{"@type":"ListItem","position":3,"name":h1,"item":url}])}]
    if slug=="index": graph=graph[1:]
    faqhtml=""
    if faqs:
        graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})
        faqhtml='<h2>Quick answers</h2><div class="faq">'+"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faqs)+"</div>"
    ld=json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)
    hero=f'<img class="hero" src="/{img}" alt="" width="1200" height="600">' if img else ""
    disc='' if slug=="index" else '<p class="disc"><b>How we earn.</b> Some links on this page are affiliate links: if you book through them, the seller may pay us a commission at no extra cost to you. It never changes what we recommend.</p>'
    by='' if slug=="index" else f'<p class="by">By Rubén and Carolina, Ibiza Party Flights · Updated {updated[8:10]} {["","January","February","March","April","May","June","July","August","September","October","November","December"][int(updated[5:7])]} {updated[:4]}</p>'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://ibizapartyflights.co.uk/img/og.jpg">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1726">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/img/fav32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Manrope:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
<script>
window.ipfLoadPartner = function () {{
  if (window.ipfPartnerLoaded) return; window.ipfPartnerLoaded = true;
  var s = document.createElement("script"); s.async = 1; s.setAttribute("data-cmp-ab", "2");
  s.src = "https://emrldco.com/NTg4OTIy.js?t=588922"; document.head.appendChild(s);
}};
try {{ if (localStorage.getItem("ipf_consent") === "yes") window.ipfLoadPartner(); }} catch (e) {{}}
</script>
<script src="/consent.js" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="logo" href="/"><img src="/img/logo.png" alt="" width="34" height="34">Ibiza Party Flights</a>
  <nav class="menu" aria-label="Main"><a href="/#plan">Flights</a><a href="/#areas">Hotels</a><a href="/#transfers">Transfers</a><a href="/#parties">Parties</a><a href="/guides/">Guides</a></nav>
</header>
<main>
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › {'Guides' if slug=='index' else '<a href="/guides/">Guides</a> › '+html.escape(h1)}</nav>
<article>
<h1>{html.escape(h1)}</h1>
<p class="lede">{lede}</p>
{by}
{hero}
{disc}
{body}
{faqhtml}
</article>
<aside class="more"><h2>Plan the trip</h2><div class="ctas">
<a class="btn primary" href="/#plan">Flights and hotels for your dates</a>
<a class="btn line" href="/guides/">All Ibiza guides</a></div></aside>
</main>
<footer>
<p><b>How we earn.</b> Ibiza Party Flights is free to use. When you book through our links we may earn a commission from the seller, at no extra cost to you. We are not affiliated with any club; club names belong to their owners.</p>
<p class="flinks"><a href="/contact.html">About and contact</a><a href="/privacy.html">Privacy policy</a><a href="/cookies.html">Cookie policy</a><a href="#" onclick="return ipfCookieSettings()">Cookie settings</a></p>
<p>© 2026 Ibiza Party Flights · Follow @ibizapartyflights on TikTok and Instagram</p>
</footer>
</div>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "ef089e38eae64ecd816234507af30767"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''
def cta(href,label,cls="primary"): return f'<p class="cta"><a class="btn {cls}" href="{href}" target="_blank" rel="noopener sponsored">{label}</a></p>'
