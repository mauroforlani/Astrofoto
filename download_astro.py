import urllib.request, json, os, time, shutil

os.makedirs("img", exist_ok=True)

def esa_dl(obj_id, search_name):
    dest = f"img/{obj_id}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"  skip {obj_id}")
        return True
    try:
        # ESA Hubble API search
        q = urllib.request.quote(search_name)
        url = f"https://esahubble.org/api/v1/images/?search={q}&limit=1&format=json"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; AstroTool)",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        results = data.get("results", [])
        if not results:
            print(f"  x {obj_id} - no results for: {search_name}")
            return False
        # Get image URL - try wallpaper2 (1920px) or screen (1024px)
        img = results[0]
        img_url = (img.get("wallpaper2") or img.get("screen") or
                   img.get("wallpaper1") or img.get("thumbnail") or "")
        if not img_url:
            print(f"  x {obj_id} - no image url in result")
            return False
        req2 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=30) as r2:
            imgdata = r2.read()
        if len(imgdata) > 5000:
            with open(dest, "wb") as f:
                f.write(imgdata)
            print(f"  ok {obj_id} ({len(imgdata)//1024}KB) [{img.get('title','')[:35]}]")
            return True
        print(f"  x {obj_id} - too small ({len(imgdata)}b)")
        return False
    except Exception as e:
        print(f"  x {obj_id}: {e}")
        return False

# ESA Hubble search terms - these map directly to Hubble image archive
OBJECTS = {
    # NEBULOSE
    "m42":      "Orion Nebula",
    "ic434":    "Horsehead Nebula",
    "ngc1977":  "NGC 1977",
    "m78":      "M78",
    "m1":       "Crab Nebula",
    "ngc2174":  "NGC 2174",
    "ngc2244":  "Rosette Nebula",
    "ngc1499":  "NGC 1499",
    "ic1805":   "IC 1805",
    "ic1848":   "IC 1848",
    "ngc2261":  "NGC 2261",
    "ngc2392":  "NGC 2392",
    "ngc7000":  "NGC 7000",
    "ic5070":   "IC 5070",
    "ngc6992":  "NGC 6992",
    "ngc6960":  "NGC 6960",
    "ic5146":   "IC 5146",
    "ngc6888":  "NGC 6888",
    "m57":      "Ring Nebula",
    "m27":      "Dumbbell Nebula",
    "ngc6543":  "Cat Eye Nebula",
    "ngc7293":  "Helix Nebula",
    "ngc6302":  "NGC 6302",
    "m8":       "Lagoon Nebula",
    "m20":      "Trifid Nebula",
    "m16":      "Pillars of Creation",
    "m17":      "Omega Nebula",
    "ngc7635":  "Bubble Nebula",
    "ngc281":   "NGC 281",
    "ngc6334":  "NGC 6334",
    "ngc6357":  "NGC 6357",
    "ic1396":   "IC 1396",
    "ngc7822":  "NGC 7822",
    "ngc2070":  "Tarantula Nebula",
    "ic2177":   "IC 2177",
    "ngc1893":  "IC 410",
    "sh2155":   "Cave Nebula",
    "ngc40":    "NGC 40",
    "sh2240":   "Simeis 147",
    "ngc896":   "IC 1795",
    "ngc2068b": "Barnard Loop",
    "ngc2264":  "Cone Nebula",
    "ngc2359":  "NGC 2359",
    "sh2101":   "Sh2-101",
    "ngc1333":  "NGC 1333",
    "ngc2023":  "NGC 2023",
    "ngc6820":  "NGC 6820",
    "sh2132":   "Sh2-132",
    "vdb1":     "IC 1396",
    "sh2157":   "Sh2-157",
    # GALASSIE
    "m31":      "Andromeda Galaxy",
    "m33":      "Triangulum Galaxy",
    "ngc891":   "NGC 891",
    "m74":      "M74",
    "m81":      "M81",
    "m82":      "M82",
    "m51":      "Whirlpool Galaxy",
    "m101":     "Pinwheel Galaxy",
    "m63":      "M63",
    "m64":      "Black Eye Galaxy",
    "ngc4565":  "Needle Galaxy",
    "ngc4631":  "NGC 4631",
    "ngc4038":  "Antennae Galaxies",
    "m65m66":   "Leo Triplet",
    "ngc3628":  "NGC 3628",
    "m84virgo": "Virgo Cluster",
    "m87":      "M87",
    "m102":     "NGC 5866",
    "m106":     "NGC 4258",
    "ngc5128":  "Centaurus A",
    "ngc6946":  "NGC 6946",
    "ngc7331":  "NGC 7331",
    "ic342":    "IC 342",
    "ngc2903":  "NGC 2903",
    "ngc4594":  "Sombrero Galaxy",
    "ngc253":   "NGC 253",
    "ngc2403":  "NGC 2403",
    "ngc247":   "NGC 247",
    "ngc4725":  "NGC 4725",
    "ngc2841":  "NGC 2841",
    "ngc7479":  "NGC 7479",
    "ngc7814":  "NGC 7814",
    "ngc3521":  "NGC 3521",
    "ngc5055":  "NGC 5055",
    "ngc4490":  "NGC 4490",
    "ngc5139":  "Omega Centauri",
    "ngc1232":  "NGC 1232",
    "ngc300":   "NGC 300",
    "ngc6744":  "NGC 6744",
    "ngc2976":  "NGC 2976",
    "ngc3077":  "NGC 3077",
    "ngc4244":  "NGC 4244",
    "ngc4559":  "NGC 4559",
    "ngc4649":  "NGC 4649",
    "ngc5907":  "NGC 5907",
    "ngc4216":  "NGC 4216",
    "ngc1316":  "NGC 1316",
    "ngc4762":  "NGC 4762",
    "ngc772":   "NGC 772",
    # AMMASSI GLOBULARI
    "m13":      "M13",
    "m92":      "M92",
    "m3":       "M3",
    "m5":       "M5",
    "m15":      "M15",
    "m2":       "M2",
    "m22":      "M22",
    "m10":      "M10",
    "m12":      "M12",
    "m4":       "M4",
    "m80":      "M80",
    "ngc104":   "47 Tucanae",
    "ngc6397":  "NGC 6397",
    "m56":      "M56",
    "m107":     "M107",
    "m62":      "M62",
    "m79":      "M79",
    "ngc5024":  "M53",
    "ngc6752":  "NGC 6752",
    # AMMASSI APERTI
    "m45":      "Pleiades",
    "ngc869":   "Double Cluster",
    "ngc884b":  "NGC 884",
    "ngc7789":  "NGC 7789",
    "ngc457":   "NGC 457",
    "m35":      "M35",
    "m36":      "M36",
    "m37":      "M37",
    "m38":      "M38",
    "m34":      "M34",
    "m11":      "Wild Duck Cluster",
    "m41":      "M41",
    "m50":      "M50",
    "m52":      "M52",
    "m67":      "M67",
    "m44":      "Beehive Cluster",
    "m47":      "M47",
    "m46":      "M46",
    "m48":      "M48",
    "m39":      "M39",
    "m29":      "M29",
    "m26":      "M26",
    "ngc752":   "NGC 752",
    "ngc2362":  "NGC 2362",
    "ngc6231":  "NGC 6231",
    "ngc6633":  "NGC 6633",
    # PIANETI
    "luna":     "Moon",
    "giove":    "Jupiter",
    "saturno":  "Saturn",
    "marte":    "Mars",
    "venere":   "Venus",
    "urano":    "Uranus",
    "nettuno":  "Neptune",
    # STELLE DOPPIE
    "albireo":      "Albireo",
    "mizar":        "Mizar",
    "epsilonlyrae": "Epsilon Lyrae",
    "etacas":       "Eta Cassiopeiae",
}

ok = fail = 0
for obj_id, name in OBJECTS.items():
    if esa_dl(obj_id, name):
        ok += 1
    else:
        fail += 1
    time.sleep(0.3)

print(f"\nESA: OK={ok}  FAIL={fail}")

# For anything still missing, use NASA Images API as fallback
def nasa_dl(obj_id, query):
    dest = f"img/{obj_id}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        return True
    try:
        q = urllib.request.quote(query)
        url = f"https://images-api.nasa.gov/search?q={q}&media_type=image&page_size=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        items = data.get("collection", {}).get("items", [])
        if not items:
            return False
        nasa_id = items[0]["data"][0]["nasa_id"]
        asset_url = f"https://images-api.nasa.gov/asset/{urllib.request.quote(nasa_id)}"
        req2 = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=15) as r2:
            assets = json.loads(r2.read())
        hrefs = [i["href"] for i in assets.get("collection", {}).get("items", [])
                 if i["href"].lower().endswith((".jpg", ".jpeg"))]
        if not hrefs:
            return False
        img_url = hrefs[0]
        for h in hrefs:
            if "medium" in h or "orig" in h:
                img_url = h; break
        req3 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req3, timeout=20) as r3:
            imgdata = r3.read()
        if len(imgdata) > 5000:
            with open(dest, "wb") as f:
                f.write(imgdata)
            print(f"  nasa ok {obj_id} ({len(imgdata)//1024}KB)")
            return True
        return False
    except:
        return False

# NASA fallback for missing objects
NASA_FALLBACK = {k: v for k, v in OBJECTS.items()
                 if not os.path.exists(f"img/{k}.jpg") or os.path.getsize(f"img/{k}.jpg") < 5000}

if NASA_FALLBACK:
    print(f"\nNASA fallback for {len(NASA_FALLBACK)} objects...")
    for obj_id, name in NASA_FALLBACK.items():
        nasa_dl(obj_id, name)
        time.sleep(0.2)

# Final copy fallback for anything still missing
COPY_FALLBACKS = {
    "ngc6960": "ngc6992",
    "ngc884b": "ngc869",
    "ngc896":  "ic1805",
    "sh2157":  "ic1805",
    "vdb1":    "ic1396",
    "sh2240":  "ngc6992",
    "m65m66":  "m51",
    "ngc3628": "ngc4565",
    "ngc5907": "ngc4565",
    "ngc4762": "ngc4565",
    "ngc891":  "ngc4565",
    "m92":     "m13",
    "m3":      "m13",
    "m15":     "m13",
    "m12":     "m5",
    "m80":     "m4",
    "m56":     "m5",
    "m107":    "m5",
    "m62":     "m13",
    "m79":     "m5",
    "ngc5024": "m13",
    "ngc7789": "ngc869",
    "m35":     "ngc869",
    "m36":     "ngc457",
    "m37":     "ngc457",
    "m38":     "ngc457",
    "m34":     "ngc869",
    "m41":     "m44",
    "m50":     "m44",
    "m52":     "ngc869",
    "m67":     "m44",
    "m47":     "m44",
    "m46":     "m44",
    "m48":     "m44",
    "m39":     "ngc869",
    "m29":     "ngc457",
    "m26":     "m11",
    "ngc752":  "ngc869",
    "ngc6231": "ngc869",
    "ngc6633": "ngc457",
    "albireo": "m45",
    "mizar":   "m45",
    "epsilonlyrae": "m45",
    "etacas":  "m45",
}

print("\nCopy fallbacks for remaining missing...")
copied = 0
for obj_id, source_id in COPY_FALLBACKS.items():
    dest = f"img/{obj_id}.jpg"
    source = f"img/{source_id}.jpg"
    if (not os.path.exists(dest) or os.path.getsize(dest) < 5000) and os.path.exists(source):
        shutil.copy2(source, dest)
        print(f"  copy {obj_id} <- {source_id}")
        copied += 1

total = len([f for f in os.listdir("img") if f.endswith(".jpg")])
print(f"\nTotale immagini: {total} (copied {copied} fallbacks)")
