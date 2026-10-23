import json, sys, time, urllib.parse, urllib.request
out = sys.argv[1]
for page in sys.argv[2:]:
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "parse", "page": page, "prop": "wikitext", "format": "json", "formatversion": 2, "redirects": 1})
    req = urllib.request.Request(url, headers={"User-Agent": "ClasicoData/1.0 (research; contact via github MOSESCI)"})
    d = json.load(urllib.request.urlopen(req))
    t = d.get("parse", {}).get("wikitext", "")
    fn = out + "/" + page.replace(" ", "_").replace("–", "-") + ".txt"
    open(fn, "w", encoding="utf-8").write(t)
    print(page, len(t), t.count("ootball box"), d.get("error", {}).get("info", ""))
    time.sleep(1)
