// Consult Finder routing engine. Mirrors the aesthetics-consult-router skill.
// Pure function: route(text) -> result object. Runs in browser and Node.
(function (root) {
  const C = {
    tox:    { kind: "book", name: "Consult For Neurotoxin", fee: "Free", short: "Neurotoxin" },
    filler: { kind: "book", name: "Injectable Filler Consult", fee: "Free", short: "Filler" },
    visia:  { kind: "book", name: "Visia Consult", fee: "$50", short: "Visia" },
    body:   { kind: "book", name: "Body Contouring Consult", fee: "$50", short: "Body Contouring" },
    tattoo: { kind: "book", name: "Consult For Tattoo Removal", fee: "$50", short: "Tattoo Removal" },
    lhr:    { kind: "book", name: "Laser Hair Removal Consult", fee: "Free", short: "Laser Hair Removal" },
    prf:    { kind: "book", name: "Consult Hair Prf Restoration", fee: "Free", short: "Hair PRF" },
  };

  // Terms: "word" = whole word; "stem*" = prefix. Weight 3 for brands/devices.
  // Longest terms are matched first and consumed, so "chin dimpling" never also counts as "dimpl*".
  const T = {
    tox: [
      ["botox",3],["botx",3],["bottox",3],["dysport",3],["xeomin",3],["daxxify",3],["jeuveau",3],["nuceiva",3],
      ["neuromodulator*",3],["neurotoxin*",3],["tox",3],["baby botox",3],["lip flip",3],
      ["wrinkle*",1],["lines",1],["forehead*",1],["crows feet",2],["crow s feet",2],["frown*",2],["11s",2],["elevens",2],
      ["between my eyes",2],["between my brows",2],["between my eyebrows",2],["bunny lines",2],["squint*",1],
      ["expression lines",2],["raise my eyebrows",2],["eyebrows",1],["brow lift",2],["brows pull",2],
      ["neck bands",2],["neck cords",2],["bands",1],["platysma*",2],["sweat*",2],["hyperhidrosis",3],
      ["grind*",2],["clench*",2],["tmj",2],["masseter",3],["slim my jaw*",2],["jaw slimming",2],["jaw is huge",2],
      ["gummy smile",2],["chin dimpl*",2],["chin keeps dimpling",2],["migraine*",2],
      ["prevent*",1],["wrinkle at the edges",3],["lip lines",2],["get ahead",1],["angry",2],["mean",1],["upset",1],["stressed",1],["forehead moving",2],
    ],
    filler: [
      ["filler*",3],["juvederm",3],["juviderm",3],["voluma",3],["volbella",3],["vollure",3],["volux",3],
      ["restylane",3],["lyft",3],["kysse",3],["defyne",3],["refyne",3],["sculptra",3],["radiesse",3],["belotero",3],
      ["rha",3],["revanesse",3],["versa",3],["teosyal",3],["skinvive",3],["skin booster*",3],["kybella",3],["kybela",3],["belkyra",3],
      ["biostimulator*",3],["collagen stimulator*",3],["hydrated from the inside",2],
      ["double chin",2],["under my chin",2],["under chin",2],["chin fat",2],["dissolve*",2],
      ["lip",1],["lips",2],["fuller",2],["plump*",2],["cheek*",2],["under eye*",2],["under my eyes",2],["tear trough*",3],
      ["hollow*",2],["sunken",2],["gaunt",2],["deflated",2],["volume",2],["fullness",2],["shadows",1],["dark circles",2],
      ["nasolabial",3],["smile lines",2],["nose to my mouth",2],["marionette",3],["corners of my mouth",2],["mouth area",2],["aged a lot",2],
      ["stronger jawline",2],["jawline",1],["chin",1],["profile",1],["10 years ago",1],["fuller before",2],
    ],
    visia: [
      ["microneedl*",3],["morpheus*",3],["skinpen",3],["potenza",3],["vivace",3],["genius rf",3],["secret rf",3],["rf microneedling",3],
      ["prp facial",3],["prf facial",3],["vampire facial",3],["vampire",2],["peel*",3],["vi peel",3],["perfect derma",3],
      ["obagi",3],["skinmedica",3],["skinceuticals",3],["tca",3],["fraxel",3],["co2",3],["resurfacing",3],
      ["photofacial",3],["photo facial",3],["photorejuvenation",3],["bbl",3],["broadband",3],["limelight",3],["moxi",3],["halo",3],
      ["clear brilliant",3],["clear and brilliant",3],["laser genesis",3],["laser toning",3],["ipl",2],["pico*",2],
      ["ultherapy",2],["ulthera",2],["thermage",2],["microderm*",3],["dermaplan*",3],["visia",3],["skin analysis",3],
      ["acne",2],["break out",2],["breaking out",2],["breakout*",2],["pimple*",2],["cystic",2],["scar*",2],["pitting",2],
      ["pores",2],["texture",2],["rough",1],["collagen",1],["rosacea",3],["redness",2],["red",1],["blotchy",2],["flush*",1],
      ["spider vein*",3],["broken capillar*",3],["capillar*",2],["vascular",2],["veins",1],["melasma",3],["pigment*",2],["hyperpigment*",3],
      ["dark spot*",2],["sun spot*",2],["age spot*",2],["brown spot*",2],["spots",1],["freckle*",1],["sun damage",2],
      ["stretch mark*",3],["wart*",3],["skin",1],["crepey",2],["crepe*",2],["loose neck",2],["neck sagging",2],["sagging neck",2],
      ["turkey neck",2],["neck skin",2],["tighten my skin",2],["skin tightening",2],["anti aging laser",2],["laser treatment",1],
      ["look better",1],["what i need",1],["where to start",1],["look at my skin",2],
    ],
    body: [
      ["evolvex",3],["evolve",3],["inmode",3],["coolsculpt*",3],["fat freez*",3],["cryolipolysis",3],["sculpsure",3],["warmsculpt*",3],
      ["trusculpt*",3],["emsculpt*",3],["emtone",3],["vanquish",3],["velashape",3],["cellulaze",3],["aveli",3],["qwo",3],["exilis",3],["hifem",3],
      ["cellulite",3],["dimpl*",1],["stubborn fat",3],["fat",2],["love handles",3],["muffin top",3],["belly",2],["stomach",2],["tummy",2],
      ["abdomen",2],["pouch*",1],["thigh*",2],["saddlebag*",3],["hips",2],["bra fat",3],["back fat",3],["arms",1],["flabby",2],
      ["loose skin",1],["having kids",1],["body contour*",3],["body sculpt*",3],["sculpt*",2],["inches",2],["problem area*",2],
      ["goal weight",2],["diet*",1],["exercise",1],["muscle ton*",3],["body",1],["slim down",2],["specific area",2],["specific spot",2],
    ],
    tattoo: [
      ["tattoo*",3],["tatoo*",3],["tat",2],["tats",2],["ink",2],["cover up",2],["enlighten",3],["revlite",3],["astanza",3],["q switched",3],
    ],
    lhr: [
      ["laser hair",3],["hair removal",3],["remove hair",3],["shav*",2],["razor*",2],["ingrown*",2],["unwanted hair",3],["facial hair",3],
      ["chin hair",3],["lip hair",3],["hair on my upper lip",3],["upper lip",1],["mustache",3],["moustache",3],["peach fuzz",2],
      ["bikini",2],["brazilian laser",3],["underarm*",2],["armpit*",2],["back hair",3],["chest hair",3],["leg hair",3],["smooth legs",2],
      ["hair free",2],["soprano",3],["gentlemax",3],["gentlelase",3],["gentleyag",3],["lightsheer",3],["splendor",3],["electrolysis",3],
      ["pcos",2],["permanent hair",3],["tired of waxing",3],["sick of waxing",3],["waxing irritates",3],["low maintenance",1],["hair reduction",3],["permanent*",2],["coarse",1],
    ],
    prf: [
      ["thinning",3],["hair loss",3],["losing my hair",3],["losing hair",3],["bald*",3],["receding",3],["hairline",3],["widow s peak",3],
      ["part is getting wider",3],["part wider",3],["scalp",2],["ponytail",2],["alopecia",3],["shedding",3],["falling out",3],
      ["prp for hair",3],["prf for hair",3],["prp hair",3],["prf hair",3],["prf",2],["prp",2],["exosome*",3],["kerafactor",3],["nutrafol",3],
      ["hair restoration",3],["crown",2],["hair is so fine",3],["hair won t grow",3],["hair isn t growing",3],["lost a lot of hair",3],
      ["hair used to be",3],["hair after",2],["lose a lot of hair",3],["lose hair",3],["lose my hair",3],
    ],
  };

  const MO = [
    { re: /\b(massage|deep tissue|hot stone|theragun|couples|body brush|dry brush)\b/, name: "Massage", label: (t) =>
      /prenatal|pregnan|motherhood/.test(t) ? "Prenatal Massage" : /couples/.test(t) ? "Couples Massage" :
      /deep tissue/.test(t) ? "Deep Tissue Massage" : /hot stone/.test(t) ? "Hot Stone Massage" : "Massage" },
    { re: /\b(wax|waxed|waxing|brazilian)\b/, name: "Waxing", label: (t) =>
      /brazilian/.test(t) ? "Brazilian Wax" : /bikini/.test(t) ? "Bikini Wax" : /brow/.test(t) ? "Brow Wax" :
      /\blip\b/.test(t) ? "Lip Wax" : /\bleg/.test(t) ? "Leg Wax" : "Waxing" },
    { re: /\b(facial|facials|hydrafacial)\b/, name: "Facial", label: (t) =>
      /hydrat/.test(t) ? "Hydrating Facial" : /men/.test(t) ? "Men's Facial" : /anti ?aging/.test(t) ? "Anti-Aging Facial" : "Facial" },
  ];

  function norm(s) {
    return " " + String(s || "").toLowerCase().replace(/['’]/g, " ").replace(/\+/g, " ")
      .replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim() + " ";
  }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  // Flatten and sort longest-first.
  const ALL = [];
  for (const cat in T) for (const [term, w] of T[cat]) {
    const stem = term.endsWith("*");
    const base = stem ? term.slice(0, -1) : term;
    ALL.push({ cat, w, len: base.length, re: new RegExp(" " + esc(base) + (stem ? "[a-z]*" : "") + "(?= )", "g") });
  }
  ALL.sort((a, b) => b.len - a.len);

  function score(t) {
    const s = {}, first = {};
    let work = t;
    for (const term of ALL) {
      work = work.replace(term.re, (m, off) => {
        s[term.cat] = (s[term.cat] || 0) + term.w;
        if (first[term.cat] === undefined || off < first[term.cat]) first[term.cat] = off;
        return " " + "_".repeat(m.length - 1);
      });
    }
    return Object.keys(s).map((cat) => ({ cat, score: s[cat], first: first[cat] }))
      .sort((a, b) => b.score - a.score || a.first - b.first);
  }

  const has = (t, re) => re.test(t);

  function book(cat, why, extra) {
    return Object.assign({ kind: "book", cat }, C[cat], { why }, extra || {});
  }

  function route(input) {
    const t = norm(input);
    if (t.trim() === "") return null;

    // 1. Emergencies
    if (has(t, /\b(vision|blind|blurry|can t see|cant see|double vision|chest pain|can t breathe|cant breathe|trouble breathing|hard to breathe|short of breath|stroke|slurr\w*|face is drooping|numb on one side)\b/))
      return { kind: "911", title: "Tell them to call 911", why: "Possible emergency. Do not book." };

    // 2. Possible complication after a treatment
    const recent = has(t, /\b(ago|after|yesterday|last week|last night|since|got|had|did|from my|this morning|days?|weeks?)\b/);
    const treated = has(t, /\b(filler|botox|tox|dysport|injection|injected|laser|peel|microneedl\w*|morpheus|kybella|treatment|sculptra|coolsculpt\w*|lips? done|appointment)\b/);
    const symptom = has(t, /\b(pain|painful|hurts?|hurting|white|blanch\w*|pale|dusky|purple|blue|blister\w*|pus|infect\w*|hot|burn\w*|burned|swell\w*|swollen|lump\w*|droop\w*|trouble swallowing|can t swallow|rash|bleeding|scabb?\w*|oozing|necrosis)\b/);
    const strong = has(t, /\b(blanch\w*|pus|infected|infection|necrosis|blister\w* after|oozing)\b/);
    if ((recent && treated && symptom) || strong)
      return { kind: "urgent", title: "Transfer to clinical staff now", why: "Possible complication. Do not book." };

    const pregnant = has(t, /\b(pregnan\w*|expecting|breastfeed\w*|breast feeding|nursing|weeks along|months along)\b/);
    const minor = has(t, /\b(under 18|minor|1[0-7] ?(yo|year old|years old|yr old)|teen\w*|high school|my son is 1[0-7]|my daughter is 1[0-7])\b/);

    // 3. MO services (unless they want permanent hair removal or a skin treatment)
    const laserCue = has(t, /\b(laser|permanent|tired of waxing|sick of waxing|hate waxing|instead of waxing|stop waxing|irritat\w*)\b/);
    const skinTxCue = has(t, /\b(photo ?facial|vampire facial|prp facial|prf facial|facial hair)\b/);
    for (const m of MO) {
      if (!has(t, m.re)) continue;
      if (m.name === "Waxing" && laserCue) continue;
      if (m.name === "Facial" && skinTxCue) continue;
      return { kind: "mo", title: "Transfer to MO", service: m.label(t), why: "No consult needed." };
    }

    // 4. Outside scope (non-appearance)
    const looks = has(t, /\b(look|looks|looking|appear\w*)\b/);
    const nonCosmetic = has(t, /\b(no energy|low energy|energy|fatigue\w*|fatigued|always tired|tired all the time|exhausted|insomnia|can t sleep|depress\w*|anxiety|anxious|joint pain|back pain|knee pain|arthritis|diabetes|blood pressure|thyroid|semaglutide|ozempic|wegovy|mounjaro|tirzepatide|glp ?1|weight loss pill\w*|testosterone|trt|hormone therapy|hrt|iv drip|iv therapy|medical condition|fever|cough|rash)\b/);
    const wantsWeightLoss = has(t, /\b(lose weight|weight loss|losing weight|diet pills?)\b/);
    let ranked = score(t);
    const top = ranked[0];
    if (nonCosmetic && !looks && (!top || top.score < 3))
      return { kind: "advise", title: "Not something we treat", why: "Suggest their primary care doctor." };
    if (wantsWeightLoss && !(ranked.find((r) => r.cat === "body" && r.score >= 3)))
      return { kind: "advise", title: "Not something we treat", why: "Suggest their primary care doctor." };

    const note = pregnant ? "Pregnant: book for after delivery and nursing. Note due date."
               : minor ? "Under 18: parent or guardian must attend." : null;

    // 5. Tiebreakers
    if (has(t, /\bpico\w*|\bq switched|\bnd ?yag\b|\benlighten\b/) && has(t, /\b(tattoo\w*|tatoo\w*|ink)\b/))
      return book("tattoo", "Pico for a tattoo.", { note });
    if (has(t, /\bipl\b/) && has(t, /\bhair\b/)) return book("lhr", "IPL for hair.", { note });
    if (has(t, /\b(thermage|ulthera\w*|rf|radiofrequency|skin tightening|tighten\w*)\b/) &&
        has(t, /\b(body|stomach|belly|tummy|thigh\w*|arms?|abdomen|knees?|butt|buttocks|legs?)\b/) && !has(t, /\bneck|face|jaw\b/))
      return book("body", "Tightening on the body.", { note });
    if (has(t, /\bneck\b/) && !has(t, /\b(botox|tox|dysport|xeomin|filler)\b/)) {
      if (has(t, /\b(bands?|cords?)\b/)) return book("tox", "Neck bands.", { note });
      if (has(t, /\b(double chin|under (my |the )?chin|fat)\b/)) return book("filler", "Fat under the chin.", { note });
      if (has(t, /\b(loose|sag\w*|crep\w*|turkey|wrinkl\w*|lax\w*|skin|droop\w*|aging)\b/)) return book("visia", "Neck skin tightening.", { note });
    }

    // "Hair" alone
    if (has(t, /\bhair\b/) && (!top || top.score < 2))
      return { kind: "ask", title: "Ask one question", ask: "Remove hair, or hair thinning?",
        options: [{ label: "Remove", res: book("lhr", "Unwanted hair.", { note }) },
                  { label: "Thinning", res: book("prf", "Hair thinning or loss.", { note }) }] };

    // "Look tired / sad / older" with no clear cue
    const vague = has(t, /\b(tired|sad|older|old|aged|aging|exhausted|worn|run down|haggard|droopy)\b/);
    const toxScore = (ranked.find((r) => r.cat === "tox") || {}).score || 0;
    const fillScore = (ranked.find((r) => r.cat === "filler") || {}).score || 0;
    if (vague && toxScore < 2 && fillScore < 2 && (!top || top.cat === "tox" || top.cat === "filler"))
      return { kind: "ask", title: "Ask one question", ask: "Lines, or hollow / lost fullness?",
        options: [{ label: "Lines", res: book("tox", "Lines and wrinkles.", { note }) },
                  { label: "Hollow", res: book("filler", "Lost volume.", { note }) }] };

    // 6. Best match
    if (!top) return book("visia", "Not sure. Visia sorts it out.", { note, fallback: true });
    const res = book(top.cat, WHY[top.cat], { note });
    const second = ranked[1];
    if (second && second.score >= 2 && second.cat !== top.cat) res.also = C[second.cat].short;
    return res;
  }

  const WHY = {
    tox: "Lines from movement.", filler: "Volume and shape.", visia: "Skin concern.",
    body: "Fat or body shaping.", tattoo: "Tattoo removal.", lhr: "Unwanted hair.", prf: "Hair thinning or loss.",
  };

  const api = { route, CONSULTS: C };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ConsultEngine = api;
})(this);
