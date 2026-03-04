import urllib.request, json, os, time

os.makedirs("img", exist_ok=True)

def nasa_dl(obj_id, query):
    dest = f"img/{obj_id}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"  skip {obj_id}")
        return True
    try:
        q = urllib.request.quote(query)
        url = f"https://images-api.nasa.gov/search?q={q}&media_type=image&page_size=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        items = data.get("collection", {}).get("items", [])
        if not items:
            print(f"  x {obj_id} - no results: {query}")
            return False
        nasa_id = items[0]["data"][0]["nasa_id"]
        asset_url = f"https://images-api.nasa.gov/asset/{urllib.request.quote(nasa_id)}"
        req2 = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=15) as r2:
            assets = json.loads(r2.read())
        hrefs = [i["href"] for i in assets.get("collection", {}).get("items", [])
                 if i["href"].lower().endswith((".jpg", ".jpeg"))]
        if not hrefs:
            print(f"  x {obj_id} - no jpg assets")
            return False
        img_url = hrefs[0]
        for h in hrefs:
            if "medium" in h or "1024" in h or "orig" in h:
                img_url = h
                break
        req3 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req3, timeout=20) as r3:
            imgdata = r3.read()
        if len(imgdata) > 5000:
            with open(dest, "wb") as f:
                f.write(imgdata)
            print(f"  ok {obj_id} ({len(imgdata)//1024}KB)")
            return True
        print(f"  x {obj_id} - too small")
        return False
    except Exception as e:
        print(f"  x {obj_id}: {e}")
        return False

OBJECTS = {
    "m42": "Orion Nebula",
    "ic434": "Horsehead Nebula",
    "ngc1977": "NGC 1977 nebula Orion",
    "m78": "Messier 78 reflection nebula",
    "m1": "Crab Nebula",
    "ngc2174": "Monkey Head Nebula",
    "ngc2244": "Rosette Nebula",
    "ngc1499": "California Nebula",
    "ic1805": "Heart Nebula",
    "ic1848": "Soul Nebula",
    "ngc2261": "Hubble Variable Nebula",
    "ngc2392": "Clown Face Nebula",
    "ngc7000": "North America Nebula",
    "ic5070": "Pelican Nebula Cygnus",
    "ngc6992": "Veil Nebula",
    "ngc6960": "Veil Nebula western filament",
    "ic5146": "Cocoon Nebula",
    "ngc6888": "Crescent Nebula",
    "m57": "Ring Nebula",
    "m27": "Dumbbell Nebula",
    "ngc6543": "Cat Eye Nebula",
    "ngc7293": "Helix Nebula",
    "ngc6302": "Butterfly Nebula",
    "m8": "Lagoon Nebula",
    "m20": "Trifid Nebula",
    "m16": "Pillars of Creation",
    "m17": "Omega Nebula",
    "ngc7635": "Bubble Nebula",
    "ngc281": "Pacman Nebula",
    "ngc6334": "Cat Paw Nebula",
    "ngc6357": "NGC 6357 star forming",
    "ic1396": "Elephant Trunk Nebula",
    "ngc7822": "Cepheus star forming region",
    "ngc2070": "Tarantula Nebula",
    "ic2177": "Seagull Nebula",
    "ngc1893": "Tadpoles Nebula",
    "sh2155": "Cave Nebula",
    "ngc40": "NGC 40 planetary nebula",
    "sh2240": "Simeis 147 supernova remnant",
    "ngc896": "IC 1795 nebula Perseus",
    "ngc2068b": "Barnard Loop Orion",
    "ngc2264": "Cone Nebula",
    "ngc2359": "NGC 2359 nebula",
    "sh2101": "Cygnus X-1 nebula",
    "ngc1333": "NGC 1333",
    "ngc2023": "NGC 2023",
    "ngc6820": "NGC 6820 emission nebula",
    "sh2132": "Sh2-132 nebula Cepheus",
    "vdb1": "IC 1396 Cepheus nebula",
    "sh2157": "Sh2-157 nebula Cassiopeia",
    "m31": "Andromeda Galaxy",
    "m33": "Triangulum Galaxy",
    "ngc891": "NGC 891 edge-on spiral",
    "m74": "M74 galaxy",
    "m81": "Messier 81 spiral galaxy",
    "m82": "Cigar Galaxy",
    "m51": "Whirlpool Galaxy",
    "m101": "Pinwheel Galaxy",
    "m63": "Sunflower Galaxy",
    "m64": "Black Eye Galaxy",
    "ngc4565": "Needle Galaxy",
    "ngc4631": "Whale Galaxy",
    "ngc4038": "Antennae Galaxies",
    "m65m66": "Messier 66 Leo galaxy",
    "ngc3628": "NGC 3628 spiral galaxy",
    "m84virgo": "Virgo Cluster",
    "m87": "M87 galaxy",
    "m102": "NGC 5866 lenticular galaxy",
    "m106": "NGC 4258",
    "ngc5128": "Centaurus A",
    "ngc6946": "Fireworks Galaxy",
    "ngc7331": "NGC 7331",
    "ic342": "IC 342",
    "ngc2903": "NGC 2903 Leo galaxy",
    "ngc4594": "Sombrero Galaxy",
    "ngc253": "Sculptor Galaxy",
    "ngc2403": "NGC 2403 spiral galaxy",
    "ngc247": "NGC 247",
    "ngc4725": "NGC 4725 barred spiral",
    "ngc2841": "NGC 2841",
    "ngc7479": "NGC 7479 barred galaxy",
    "ngc7814": "Little Sombrero",
    "ngc3521": "NGC 3521 spiral galaxy",
    "ngc5055": "Messier 63 galaxy",
    "ngc4490": "Cocoon Galaxy",
    "ngc5139": "Omega Centauri",
    "ngc1232": "NGC 1232 face-on galaxy",
    "ngc300": "NGC 300",
    "ngc6744": "NGC 6744",
    "ngc2976": "NGC 2976 dwarf galaxy",
    "ngc3077": "NGC 3077 galaxy M81 group",
    "ngc4244": "NGC 4244",
    "ngc4559": "NGC 4559 spiral galaxy",
    "ngc4649": "NGC 4649",
    "ngc5907": "NGC 5907 edge-on galaxy",
    "ngc4216": "NGC 4216 galaxy Virgo",
    "ngc1316": "Fornax A",
    "ngc4762": "NGC 4762 lenticular",
    "ngc772": "NGC 772 unbarred spiral",
    "m13": "Messier 13 globular",
    "m92": "Messier 92 globular",
    "m3": "Messier 3 globular",
    "m5": "Messier 5 globular",
    "m15": "Messier 15 globular",
    "m2": "M2 globular cluster",
    "m22": "M22 globular cluster",
    "m10": "Messier 10 globular",
    "m12": "Messier 12 globular",
    "m4": "M4 globular cluster",
    "m80": "Messier 80 globular",
    "ngc104": "47 Tucanae",
    "ngc6397": "NGC 6397 globular cluster southern",
    "m56": "Messier 56 globular Lyra",
    "m107": "Messier 107 globular",
    "m62": "Messier 62 globular",
    "m79": "Messier 79 globular Lepus",
    "ngc5024": "Messier 53 globular cluster",
    "ngc6752": "NGC 6752",
    "m45": "Pleiades",
    "ngc869": "Double Cluster",
    "ngc884b": "Perseus cluster",
    "ngc7789": "NGC 7789 open cluster Cassiopeia",
    "ngc457": "ET Cluster",
    "m35": "Messier 35 open cluster Gemini",
    "m36": "Messier 36 Auriga cluster",
    "m37": "Messier 37 Auriga cluster",
    "m38": "Messier 38 Auriga cluster",
    "m34": "Messier 34 open cluster",
    "m11": "Wild Duck Cluster",
    "m41": "Messier 41 open cluster Canis",
    "m50": "Messier 50 open cluster",
    "m52": "Messier 52 open cluster",
    "m67": "Messier 67 old cluster Cancer",
    "m44": "Beehive Cluster",
    "m47": "Messier 47 open cluster",
    "m46": "Messier 46 open cluster",
    "m48": "Messier 48 open cluster Hydra",
    "m39": "Messier 39 open cluster Cygnus",
    "m29": "Messier 29 open cluster",
    "m26": "Messier 26 open cluster Scutum",
    "ngc752": "NGC 752 open cluster",
    "ngc2362": "NGC 2362 cluster",
    "ngc6231": "NGC 6231 open cluster Scorpius",
    "ngc6633": "NGC 6633 open cluster",
    "luna": "Moon surface",
    "giove": "Jupiter",
    "saturno": "Saturn",
    "marte": "Mars",
    "venere": "Venus",
    "urano": "Uranus",
    "nettuno": "Neptune",
    "albireo": "Albireo beta Cygni colored double star",
    "mizar": "Mizar Alcor Ursa Major",
    "epsilonlyrae": "double double star Lyra",
    "etacas": "Eta Cassiopeiae binary star",
}

ok = fail = 0
for obj_id, query in OBJECTS.items():
    if nasa_dl(obj_id, query):
        ok += 1
    else:
        fail += 1
    time.sleep(0.3)

print(f"\nOK={ok}  FAIL={fail}")
