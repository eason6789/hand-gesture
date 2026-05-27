#!/usr/bin/env python3
import os, json, urllib.request, urllib.error, time, sys

api_key = os.environ.get("ZHIPU_API_KEY", "").strip()
url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
out_dir = "/Users/easonlv/progs/dividation/cards/faces"
os.makedirs(out_dir, exist_ok=True)

cards = [
    (2,"灭","Extinction","Ancient Chinese rune '灭' — cosmic void swallowing light, black hole spiral dissolving stars, obsidian shard borders, dark mystical tarot #0B0D10 #B89A63 gold #2B4A46 emerald"),
    (3,"连","Connection","Ancient Chinese rune '连' — golden thread linking two celestial bodies, constellation web, interwoven destiny, mystical tarot frame #0B0D10 #B89A63 gold"),
    (4,"孤","Solitude","Ancient Chinese rune '孤' — lone wolf beneath winter moon, frost patterns, isolated mountain peak, silver mist, mystical tarot #0B0D10 silver accents"),
    (5,"欲","Desire","Ancient Chinese rune '欲' — burning heart wreathed in flames, diamond-spark eyes, serpentine vines, rose-gold tendrils, dark mystical tarot #B89A63 gold #2B4A46"),
    (6,"轮","Cycle","Ancient Chinese rune '轮' — cosmic wheel of dharma, rotating zodiac rings, eight trigram symbols, golden axle, mystical mandala frame #0B0D10 #B89A63 gold"),
    (7,"时","Time","Ancient Chinese rune '时' — ancient clepsydra water clock, dripping golden droplets, zodiac ring, hourglass celestial, mystical tarot #0B0D10 #B89A63 gold"),
    (8,"情","Emotion","Ancient Chinese rune '情' — two entangled moths wings, heart vein patterns, moonlight bloom, rose-quartz crystal, mystical tarot #0B0D10 #2B4A46 #D8D4C8"),
    (9,"序","Order","Ancient Chinese rune '序' — celestial law tablets, balanced scale, ranked rune sequences, perfect geometric grid, mystical tarot #0B0D10 #B89A63 gold"),
    (10,"沌","Chaos","Ancient Chinese rune '沌' — turbulent primordial soup, swirling nebula, broken rune fragments, anarchic brushstrokes, mystical tarot #0B0D10 dark purple #B89A63 gold"),
    (11,"痕","Trace","Ancient Chinese rune '痕' — ancient footprints on cosmic sand, weathered scar patterns, ink-wash landscape, fossilized light, mystical tarot #0B0D10 #B89A63 gold"),
    (12,"寂","Silence","Ancient Chinese rune '寂' — empty temple bell, spider-web candlelight, still water reflection, moss-covered stone, mystical tarot #0B0D10 #D8D4C8 moonwhite"),
    (13,"燃","Burning","Ancient Chinese rune '燃' — three flame tongues, phoenix rising, ember particles, volcanic inscriptions, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (14,"凝","Stasis","Ancient Chinese rune '凝' — suspended ice crystal, frost flowering, frozen moment, crystalline structure, mystical tarot #0B0D10 #D8D4C8 ice-blue"),
    (15,"流","Flow","Ancient Chinese rune '流' — flowing water forming yin-yang, river-current patterns, koi fish, oceanic wave frame, mystical tarot #0B0D10 #2B4A46 #B89A63 gold"),
    (16,"触","Touch","Ancient Chinese rune '触' — two lightning sparks meeting, electric discharge, tesla coil edges, thunderous convergence, mystical tarot #0B0D10 #B89A63 gold"),
    (17,"视","Vision","Ancient Chinese rune '视' — all-seeing eye within triangle, ray-of-light pupils, optic-nerve golden threads, celestial vision, mystical tarot #0B0D10 #B89A63 gold"),
    (18,"念","Thought","Ancient Chinese rune '念' — brain-corridor essence, synaptic flash, spirit-matter threads, mind palace architecture, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (19,"纹","Pattern","Ancient Chinese rune '纹' — intricate Celtic knot forming rune shape, interlaced eternity loops, sacred geometry mandala, mystical tarot #0B0D10 #B89A63 gold"),
    (20,"墟","Ruins","Ancient Chinese rune '墟' — ancient civilization ruins, overgrown stone pillars, shattered star-map fragments, moonlit moss, mystical tarot #0B0D10 #B89A63 gold"),
    (21,"镜","Mirror","Ancient Chinese rune '镜' — infinite mirror recursion, reflective dimension fold, kaleidoscope pattern, fractal eternity, mystical tarot #0B0D10 #D8D4C8 #B89A63 gold"),
    (22,"绊","Bond","Ancient Chinese rune '绊' — two figures bound by golden chain, knot-of-destiny motifs, intertwined fates, sacred tether, mystical tarot #0B0D10 #B89A63 gold"),
    (23,"执","Obsession","Ancient Chinese rune '执' — chains wrapping glowing gem, inescapable binding, dark crystalline frame, obsessive patterns, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (24,"续","Continuity","Ancient Chinese rune '续' — infinite mobius-strip loop, seamless continuation lines, eternal flow pattern, mystical tarot #0B0D10 #B89A63 gold"),
    (25,"陨","Falling","Ancient Chinese rune '陨' — meteor shower streaking void, burning debris trail, fallen star crater, cosmic descent, mystical tarot #0B0D10 #B89A63 gold"),
    (26,"渊","Abyss","Ancient Chinese rune '渊' — deep ocean trench, bioluminescent creatures, pressure crystals, infinite descent, mystical tarot #0B0D10 #2B4A46 #D8D4C8"),
    (27,"契","Contract","Ancient Chinese rune '契' — two hands shaking over ancient seal, wax sigil with blood drop, oath-bounding light, mystical tarot #0B0D10 #B89A63 gold"),
    (28,"祭","Ritual","Ancient Chinese rune '祭' — altar with ceremonial fire, sacrificial bowl, rune-inscribed stone tablet, mystic smoke spirals, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (29,"兆","Omen","Ancient Chinese rune '兆' — lightning-split sky, scattered oracle bones, portent clouds, prophetic symbols, mystical tarot #0B0D10 #B89A63 gold"),
    (30,"启","Awakening","Ancient Chinese rune '启' — third eye opening, ray-of-truth beam, cascading enlightenment, divine consciousness, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
    (31,"隐","Hidden","Ancient Chinese rune '隐' — hidden cipher within sacred geometry, invisible ink revealed by moonlight, masked veil, secret patterns, mystical tarot #0B0D10 #B89A63 gold"),
    (32,"显","Manifest","Ancient Chinese rune '显' — radiant halo appearing from darkness, truth-manifesting light, materialized spirit, revealed mysteries, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
    (33,"缚","Binding","Ancient Chinese rune '缚' — golden rope coils trapping spirit, magical constraint sigils, binding pentagram, prisoner light, mystical tarot #0B0D10 #B89A63 gold"),
    (34,"赎","Redemption","Ancient Chinese rune '赎' — broken chain transforming to wings, redeemed soul ascending, golden aurora, forgiveness light, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
    (35,"噬","Consuming","Ancient Chinese rune '噬' — cosmic serpent eating its tail, void-mouth opening, consuming vortex, emptiness hungry, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (36,"塑","Shaping","Ancient Chinese rune '塑' — potter shaping cosmic clay, divine sculptor tools, forming reality, creative fire, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (37,"裂","Fracture","Ancient Chinese rune '裂' — shattered crystal forming rune, crackling energy along fault lines, breaking dimension, fault fractal, mystical tarot #0B0D10 silver"),
    (38,"愈","Healing","Ancient Chinese rune '愈' — glowing caduceus crossed with rune, healing light aura, herbalist mortar, wellness energy flow, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (39,"惑","Confusion","Ancient Chinese rune '惑' — labyrinth path within eye, maze corridors, disorienting spiral, puzzling mysteries, befuddlement, mystical tarot #0B0D10 #B89A63 gold"),
    (40,"觉","Awareness","Ancient Chinese rune '觉' — monk enlightenment under bodhi tree, wisdom-light aura, awakened consciousness, cosmic awareness, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
    (41,"忘","Forgetting","Ancient Chinese rune '忘' — fading memory fragments dissolving, forgotten symbol into mist, forgotten ruins, ethereally fading, mystical tarot #0B0D10 #D8D4C8 moonwhite"),
    (42,"铭","Inscription","Ancient Chinese rune '铭' — golden inscription on ancient stone tablet, chiseled rune depth, carved wisdom text, eternal record, mystical tarot #0B0D10 #B89A63 gold"),
    (43,"坠","Descent","Ancient Chinese rune '坠' — figure falling through cloudscape, descent trail, cloud-layer descent, gravity pulling down, mystical tarot #0B0D10 #B89A63 gold"),
    (44,"昇","Ascension","Ancient Chinese rune '昇' — spirit ascending on light-beam staircase, celestial rise, divine ascension, soul climbing heaven, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
    (45,"蚀","Erosion","Ancient Chinese rune '蚀' — time-weathered ancient stone, wind erosion patterns, century-worn texture, crumbling edges, eroded rune, mystical tarot #0B0D10 #B89A63 gold silver"),
    (46,"融","Merging","Ancient Chinese rune '融' — two elements dissolving into each other, fusion boundary glow, merging realms, united opposites, mystical tarot #0B0D10 #B89A63 gold #2B4A46"),
    (47,"断","Severance","Ancient Chinese rune '断' — sharp blade cutting golden thread, severed destiny, clean break line, sundered fate, decisive separation, mystical tarot #0B0D10 silver #B89A63 gold"),
    (48,"终","Completion","Ancient Chinese rune '终' — cycle completing into perfect circle, final endpoint glowing, full-circle closure, eternal completion, mystical tarot #0B0D10 #B89A63 gold #D8D4C8"),
]

def gen(idx, char, prompt):
    payload = json.dumps({"model": "cogview-4-250304", "prompt": prompt, "size": "1024x1360", "n": 1})
    req = urllib.request.Request(url, data=payload.encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            img_url = data["data"][0]["url"]
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=60) as ir:
                img_data = ir.read()
            fname = f"{out_dir}/card_{idx:02d}_{char}.png"
            with open(fname, "wb") as f:
                f.write(img_data)
            return True, len(img_data)
        except Exception as e:
            if attempt < 4:
                time.sleep(10)
            else:
                return False, str(e)
    return False, "exhausted"

generated = 0
failed = []
for idx, char, en, prompt in cards:
    fname = f"{out_dir}/card_{idx:02d}_{char}.png"
    if os.path.exists(fname):
        print(f"[{idx:02d}] {char} — exists, skip")
        continue
    print(f"[{idx:02d}] {char} ({en})...", end=" ", flush=True)
    ok, result = gen(idx, char, prompt)
    if ok:
        print(f"OK {result//1024}KB")
        generated += 1
    else:
        print(f"FAIL: {result}")
        failed.append((idx, char))
    time.sleep(5)

print(f"\n=== DONE: {generated} generated, {len(failed)} failed ===")
if failed:
    print("Failed:", [f"{c}({i})" for i,c in failed])