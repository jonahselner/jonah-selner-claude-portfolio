"""Generate a fictional GoHighLevel-style data set for "Lakemont LASIK & Vision",
a made-up 3-location LASIK practice whose lead follow-up is run by Boost.

All people, phone numbers, emails and the clinic itself are invented.
Phone numbers use the 555 exchange; emails use example.com/.net/.org.

Usage:
  python generate.py --leads 6000 --start 2025-11-01 --end 2026-10-25 --out ../data
  python generate.py --leads 60 --start 2026-08-01 --end 2026-10-25 --out ../sample
"""
import argparse, csv, json, math, os, random, string
from datetime import datetime as DT, timedelta as TD, date as D
import texts as T

ap = argparse.ArgumentParser()
ap.add_argument("--leads", type=int, default=6000)
ap.add_argument("--start", default="2025-11-01")
ap.add_argument("--end", default="2026-10-25")
ap.add_argument("--out", default="../data")
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--ep-rate", type=float, default=0.95, help="existing-patient calls per open hour at full volume (scaled to lead volume)")
args = ap.parse_args()

R = random.Random(args.seed)
START = DT.fromisoformat(args.start)
END = DT.fromisoformat(args.end) + TD(hours=23, minutes=59)
EXPORT_AT = DT(2026, 10, 26, 9, 0)

AI_TEXT_LAUNCH = DT(2026, 1, 12)        # Conversation AI answers texts 24/7
VOICE_AI_LAUNCH = DT(2026, 5, 11)       # Voice AI screens the new-patient line
CARRIER_ISSUE = (DT(2026, 8, 4), DT(2026, 8, 29))   # Woodbury number filtered (30007)
SAT_STAFF_FIX = DT(2026, 9, 12)         # Saturday coverage added after missed-call review

def gid(n=20):
    return "".join(R.choice(string.ascii_letters + string.digits) for _ in range(n))

LOCATION_ID = gid()
PIPELINE_ID = gid()
STAGES = ["New Lead", "Attempting Contact", "Engaged", "Consult Scheduled", "Consult Showed",
          "No-Show", "Surgery Scheduled", "Long-Term Nurture"]
STAGE_IDS = {s: gid(24).lower() for s in STAGES}

# ---------------------------------------------------------------- time helpers
def is_dst(t):
    return DT(2026, 3, 8, 2) <= t < DT(2026, 11, 1, 2) or t < DT(2025, 11, 2, 2)

def to_utc(t):
    return t + TD(hours=5 if is_dst(t) else 6)  # US Central

def fz(t):  # GHL API style
    return to_utc(t).strftime("%Y-%m-%dT%H:%M:%S.") + f"{R.randint(0,999):03d}Z"

def fl(t):  # native CSV export style (local)
    return t.strftime("%Y-%m-%d %H:%M:%S")

def fus(t):  # Call Reporting style
    return t.strftime("%m/%d/%Y %I:%M %p")

def is_open(t, sat_end=13):
    wd = t.weekday()
    if wd < 5:
        return 8 <= t.hour < 19
    if wd == 5:
        return 9 <= t.hour < sat_end
    return False

def next_open(t):
    t2 = t.replace(second=0, microsecond=0)
    for _ in range(24 * 4 * 10):
        if is_open(t2):
            return t2
        t2 += TD(minutes=15)
        t2 = t2.replace(minute=(t2.minute // 15) * 15)
    return t2

def agent_time(t, jitter=(2, 75)):
    if is_open(t):
        return t
    return next_open(t) + TD(minutes=R.randint(*jitter))

def wf_time(t):
    """Workflows here only send 9:00-19:30 local; queue to 9:0x next morning."""
    if 9 <= t.hour < 19 or (t.hour == 19 and t.minute < 30):
        return t
    nt = t if t.hour < 9 else t + TD(days=1)
    return nt.replace(hour=9, minute=R.randint(0, 9), second=R.randint(0, 59))

def at_day(base, days, hour_range=(9, 18)):
    d = (base + TD(days=days)).replace(hour=R.randint(*hour_range), minute=R.randint(0, 59), second=R.randint(0, 59))
    return d

def sec(t, a, b):
    return t + TD(seconds=R.randint(a, b))

def mins(t, a, b):
    return t + TD(seconds=R.randint(int(a * 60), int(b * 60)))

# ---------------------------------------------------------------- reference data
LOCS = {"Edina": "+19525550111", "Maple Grove": "+17635550112", "Woodbury": "+16515550113"}
LOC_W = [0.38, 0.34, 0.28]
MAIN_LINE = "+16125550100"
TRACKING = {"Google Ads": "+16125550121", "Google Business Profile": "+16125550122",
            "Facebook": "+16125550123", "Website": MAIN_LINE}

AGENTS = [
    dict(name="Maya Torres", start=DT(2025, 1, 1), end=DT(2030, 1, 1), mult=1.05, speed=1.0),
    dict(name="Derek Liu", start=DT(2025, 1, 1), end=DT(2030, 1, 1), mult=0.9, speed=1.6),
    dict(name="Priya Natarajan", start=DT(2025, 1, 1), end=DT(2030, 1, 1), mult=1.3, speed=0.8),
    dict(name="Jordan Ellis", start=DT(2025, 1, 1), end=DT(2026, 6, 30), mult=0.8, speed=1.2),
    dict(name="Sam Okafor", start=DT(2026, 7, 6), end=DT(2030, 1, 1), mult=0.95, speed=1.0),
]
for a in AGENTS:
    a["id"] = gid()
    a["first"] = a["name"].split()[0]
FRONT_DESK = dict(name="Lakemont Front Desk", id=gid())

# true source -> behavior. "labels" are the messy values that land in the CRM Source field.
SOURCES = {
    "Facebook":   dict(w=.30, book=.13, invalid=.08, opt=1.6, kind="form", form="FB Lead Form - Free Consult Offer",
                       labels=["facebook", "Facebook Lead Ads", "fb_leadgen", "FB", "Facebook", ""], utm=("facebook", "paid_social"),
                       camps=["LASIK_FreeConsult_Broad", "LASIK_Lookalike_1pct", "LASIK_Retarget_30d"]),
    "Instagram":  dict(w=.06, book=.11, invalid=.06, opt=1.4, kind="form", form="IG Lead Form - Free Consult",
                       labels=["instagram", "Instagram", "ig", "facebook", ""], utm=("instagram", "paid_social"),
                       camps=["LASIK_Reels_Q1", "LASIK_Stories_Broad"]),
    "Google Ads": dict(w=.20, book=.30, invalid=.02, opt=0.8, kind="form", form="LASIK Self-Test (Google LP)",
                       labels=["google ads", "Google Ads", "adwords", "google / cpc", "ppc", "Website"], utm=("google", "cpc"),
                       camps=["Search_LASIK_Cost", "Search_LASIK_NearMe", "Search_Brand"]),
    "Organic":    dict(w=.13, book=.27, invalid=.02, opt=0.8, kind="form", form="Am I a Candidate? Quiz",
                       labels=["organic", "google / organic", "Website", "website form", ""], utm=("", ""), camps=[""]),
    "Google Business Profile": dict(w=.08, book=.36, invalid=.01, opt=0.6, kind="call", form="",
                       labels=["Google My Business", "GMB", "google business profile", "Inbound Call", "call"], utm=("", ""), camps=[""]),
    "Referral":   dict(w=.05, book=.45, invalid=.01, opt=0.5, kind="form", form="Refer-a-Friend Form",
                       labels=["Referral", "referral", "friend", "Patient Referral"], utm=("", ""), camps=[""]),
    "Website Chat": dict(w=.05, book=.24, invalid=.03, opt=0.8, kind="chat", form="Website Chat Widget",
                       labels=["chat widget", "Website Chat", "Website"], utm=("", ""), camps=[""]),
    "Financing Page": dict(w=.04, book=.30, invalid=.02, opt=0.8, kind="form", form="Financing Pre-Qualification",
                       labels=["Website", "financing form", "website form"], utm=("google", "cpc"), camps=["Search_LASIK_Financing"]),
    "Vision Fair Event": dict(w=.03, book=.17, invalid=.05, opt=1.2, kind="import", form="",
                       labels=["Event", "Vision Fair 2026", "csv import", ""], utm=("", ""), camps=[""]),
}
SRC_NAMES = list(SOURCES)

FIRST = """Aaliyah Aaron Abigail Adrian Aisha Alejandro Alexis Amir Ana Andre Angela Anthony Ava Ben Bianca Brandon Brianna
Caleb Camila Carlos Carmen Chloe Chris Connor Daniel Danielle Darius David Destiny Diego Dylan Elena Elijah Emily Emma
Eric Ethan Fatima Gabriel Grace Hannah Hector Ian Imani Isabella Jacob Jada James Jasmine Jason Javier Jenna Jessica
Jordan Jose Joshua Julia Justin Kayla Keisha Kevin Kyle Laura Lauren Leah Liam Lily Logan Lucas Luis Madison Malik Maria
Marcus Mariah Matthew Megan Mia Michael Michelle Mohammed Morgan Nadia Natalie Nathan Nicole Noah Olivia Omar Paige
Patrick Priya Rachel Rafael Rebecca Ryan Samantha Sara Sean Sofia Stephanie Tanya Taylor Terrell Tiffany Tyler Valeria
Vanessa Victor Whitney Xavier Yasmin Zach Zoe Brooke Cody Derrick Erin Gina Heather Holly Jamal Kara Kendra Kim Lena""".split()
LAST = """Adams Ahmed Alvarez Anderson Bailey Baker Banks Bennett Brooks Brown Bryant Campbell Carter Castillo Chen Clark
Coleman Collins Cook Cooper Cruz Davis Diaz Edwards Evans Fisher Flores Foster Garcia Gomez Gonzalez Gray Green Griffin
Hall Harris Hayes Hernandez Hill Howard Hughes Jackson James Jenkins Johnson Jones Kelly Khan Kim King Lee Lewis Long
Lopez Martin Martinez Mendoza Miller Mitchell Moore Morales Morgan Murphy Myers Nguyen Nelson Ortiz Owens Parker Patel
Perez Perry Peterson Phillips Powell Price Ramirez Reed Reyes Richardson Rivera Roberts Robinson Rodriguez Rogers Ross
Russell Sanchez Sanders Scott Shah Simmons Smith Stewart Sullivan Taylor Thomas Thompson Torres Turner Walker Ward
Washington Watson White Williams Wilson Wood Wright Young Zimmerman Okoye Haddad Kowalski Novak Bauer""".split()
AREA = ["612", "612", "651", "651", "952", "952", "763", "763", "320", "507"]
CITIES = [("Minneapolis", "55408"), ("St. Paul", "55105"), ("Edina", "55435"), ("Bloomington", "55420"), ("Maple Grove", "55369"),
          ("Plymouth", "55447"), ("Woodbury", "55125"), ("Eagan", "55123"), ("Eden Prairie", "55344"), ("Roseville", "55113"),
          ("Minnetonka", "55305"), ("Burnsville", "55337"), ("Blaine", "55434"), ("Lakeville", "55044"), ("Stillwater", "55082")]

used_phones = set()
def phone():
    while True:
        p = f"+1{R.choice(AREA)}555{R.randint(0, 9999):04d}"
        if p[-4:] != "1212" and p not in used_phones and p not in LOCS.values() and p not in TRACKING.values():
            used_phones.add(p)
            return p

def pretty_phone(p):
    d = p[2:]
    return R.choice([f"({d[:3]}) {d[3:6]}-{d[6:]}", f"{d[:3]}-{d[3:6]}-{d[6:]}", d, f"+1 {d[:3]} {d[3:6]} {d[6:]}", f"1{d}"])

def messy_case(s):
    r = R.random()
    return s.lower() if r < .06 else s.upper() if r < .08 else s

def email(first, last):
    dom = R.choice(["example.com", "example.com", "example.net", "example.org"])
    style = R.choice(["{f}.{l}", "{f}{l}", "{f}{l}{n}", "{fi}{l}", "{f}_{l}{n}", "{f}.{l}{n}"])
    e = style.format(f=first.lower(), l=last.lower(), fi=first[0].lower(), n=R.randint(1, 99)) + "@" + dom
    bad = R.random() < .025
    if bad:
        e = e.replace(".com", ".con").replace(".net", ".ent") if R.random() < .7 else e.replace("@", "")
    return e, bad

def pick(lst):
    return R.choice(lst)

# ---------------------------------------------------------------- output tables
messages, call_report, vai_logs, contacts_rows, opps, appts, forms, enrolls = [], [], [], [], [], [], [], []
truth = []
WF_IDS = {}
def wfid(name):
    if name not in WF_IDS:
        WF_IDS[name] = gid(8).lower() + "-" + gid(4).lower() + "-" + gid(4).lower() + "-" + gid(12).lower()
    return WF_IDS[name]

WF = {
    1: "01 | New Lead - Speed to Lead", 2: "02 | New Lead Nurture - 30 Day", 3: "03 | Consult Booked - Reminders",
    4: "04 | No-Show Recovery", 5: "05 | Long-Term Nurture - Monthly", 6: "06 | Financing Interest",
    7: "07 | Missed Call Text Back", 8: "08 | Voice AI - New Patient Line Routing", 9: "09 | Post-Consult Follow Up",
}

def enroll(c, n, t, status="finished", exit_t=None, reason="completed"):
    enrolls.append(dict(contactId=c["id"], workflowId=wfid(WF[n]), workflowName=WF[n], enrolledAt=fz(t),
                        status=status, exitedAt=fz(exit_t) if exit_t else "", exitReason=reason if exit_t else ""))

# ---------------------------------------------------------------- message writers
TYPE_NUM = {"TYPE_CALL": 1, "TYPE_SMS": 2, "TYPE_EMAIL": 3, "TYPE_WEBCHAT": 5, "TYPE_CAMPAIGN_VOICEMAIL": 10}

def touch(c, t):
    if t > c["last_activity"]:
        c["last_activity"] = t

def msg(c, t, mtype, direction, status, body="", user=None, source="", frm="", to="", error="",
        attachments="[]", ctype="text/plain", updated=None):
    if t > END:
        return None
    m = dict(id=gid(), direction=direction, status=status, type=TYPE_NUM[mtype], locationId=LOCATION_ID,
             attachments=attachments, body=body, contactId=c["id"], contentType=ctype,
             conversationId=c["conv"], dateAdded=fz(t), dateUpdated=fz(updated or sec(t, 1, 8)),
             userId=user["id"] if user else "", source=source, **{"from": frm}, to=to, error=error, messageType=mtype,
             _t=t)
    messages.append(m)
    touch(c, t)
    return m

def fill(s, c, **kw):
    a = kw.pop("agent", None) or c["agent"]
    return s.format(first=c["first_clean"], loc=c["loc"], clinic=T.CLINIC, agent=a["first"],
                    link="https://lakemontlasik.example.com/book", **kw)

def sms_out(c, t, body, kind="workflow", user=None):
    if t > END or c["dnd_sms_at"] and t >= c["dnd_sms_at"]:
        return None
    src = {"workflow": "workflow", "agent": "app", "ai": "api", "bulk": "bulk_actions"}[kind]
    frm = LOCS[c["loc"]]
    status, err = "delivered", ""
    if c["invalid"]:
        status, err = "failed", pick(["30003 - Unreachable destination handset", "30005 - Unknown destination handset", "30006 - Landline or unreachable carrier"])
    elif c["loc"] == "Woodbury" and CARRIER_ISSUE[0] <= t <= CARRIER_ISSUE[1] and R.random() < .38:
        status, err = "failed", "30007 - Message filtered by carrier"
    elif R.random() < .012:
        status, err = "undelivered", "30008 - Unknown error"
    elif R.random() < .01:
        status = "sent"
    m = msg(c, t, "TYPE_SMS", "outbound", status, body, user if kind == "agent" else None, src, frm, c["phone"], err)
    if m:
        c["sms_out"] += 1
        c["first_sms"] = c["first_sms"] or t
        c["last_sms"] = t
        if c["dnd_flag_pending"] and t > c["optout_t"]:
            c["texts_after_optout"] += 1
    return m

def sms_in(c, t, body, attachments="[]", ctype="text/plain"):
    if t > END:
        return None
    m = msg(c, t, "TYPE_SMS", "inbound", "delivered", body, None, "", c["phone"], LOCS[c["loc"]], "", attachments, ctype)
    if m:
        c["sms_in"] += 1
        c["first_sms"] = c["first_sms"] or t
        c["last_sms"] = t
    return m

def email_out(c, t, body):
    if t > END or c["dnd_email"]:
        return None
    if c["bad_email"]:
        return msg(c, t, "TYPE_EMAIL", "outbound", "failed", body, None, "workflow", ctype="text/html",
                   error="550 5.1.1 Recipient address rejected: User unknown")
    r = R.random()
    status, upd = ("clicked", mins(t, 5, 2000)) if r < .04 else ("opened", mins(t, 2, 3000)) if r < .29 else ("delivered", sec(t, 2, 20))
    return msg(c, t, "TYPE_EMAIL", "outbound", status, body, None, "workflow", ctype="text/html", updated=upd)

def rvm(c, t):
    if t > END or c["dnd_calls"]:
        return None
    return msg(c, t, "TYPE_CAMPAIGN_VOICEMAIL", "outbound", "failed" if c["invalid"] else "delivered", "", None, "workflow",
               MAIN_LINE, c["phone"], "Voicemail drop failed" if c["invalid"] else "")

def call(c, t, direction, status, dur, user=None, number=None, src_name="", voice_ai=False):
    """status uses GHL callStatus values: completed, no-answer, busy, failed, canceled, voicemail."""
    if t > END:
        return None
    number = number or LOCS[c["loc"]]
    frm, to = (number, c["phone"]) if direction == "outbound" else (c["phone"], number)
    m = msg(c, t, "TYPE_CALL", direction, status, "", user, "app" if direction == "outbound" else "", frm, to,
            "", "[]", "text/plain", updated=t + TD(seconds=dur + R.randint(5, 30)))
    # Call Reporting export: voicemail on outbound shows as completed (known GHL quirk); voice AI legs not separated
    rep_status = "completed" if (direction == "outbound" and status == "voicemail") else status
    first_time = ""
    if direction == "inbound":
        first_time = "Yes" if not c["called_in"] else "No"
        c["called_in"] = True
    call_report.append({"Date & Time": fus(t), "Contact Name": c["name_raw"], "Contact Phone": c["phone"],
                        "Direction": direction.capitalize(), "Call Status": rep_status, "Duration": dur,
                        "Source": src_name if direction == "inbound" else "", "Number": number,
                        "User": "Voice AI" if voice_ai else (user["name"] if user else ""),
                        "First Time Caller": first_time, "Recording": "Yes" if dur > 0 else "No", "_t": t})
    if user and dur and t <= END:
        team_seconds.append((t, dur, "existing" if c["existing"] else "lead", direction))
    return m

team_seconds = []

# ---------------------------------------------------------------- contacts
contacts = []

def active_agents(t):
    return [a for a in AGENTS if a["start"] <= t < a["end"]]

rr = [0]
def assign_agent(t):
    pool = active_agents(t)
    rr[0] += 1
    return pool[rr[0] % len(pool)]

def new_contact(created, src, existing=False):
    first, last = pick(FIRST), pick(LAST)
    em, bad = email(first, last)
    city, zipc = pick(CITIES)
    s = SOURCES.get(src, {})
    c = dict(id=gid(), conv=gid(), first_clean=first, first=messy_case(first), last=messy_case(last),
             name_raw=f"{first} {last}", phone=phone(), email=em, bad_email=bad, city=city, zip=zipc,
             created=created, last_activity=created, src=src, existing=existing,
             src_label=pick(s["labels"]) if s else "inbound call",
             loc=R.choices(list(LOCS), LOC_W)[0], agent=None if existing else assign_agent(created),
             invalid=(R.random() < s.get("invalid", 0)) if s else False,
             dnd_sms_at=None, dnd_calls=False, dnd_email=False, dnd_flag_pending=False, optout_t=None,
             texts_after_optout=0, called_in=False,
             sms_out=0, sms_in=0, first_sms=None, last_sms=None, tags=set(),
             procedure=R.choices(["LASIK", "Not Sure", "PRK", "EVO ICL", "SMILE"], [62, 22, 6, 6, 4])[0],
             wears=R.choices(["Glasses", "Contacts", "Both"], [38, 27, 35])[0],
             age=R.choices(["18-24", "25-34", "35-44", "45-54", "55+"], [12, 34, 28, 17, 9])[0],
             fin=R.random() < (.75 if src == "Financing Page" else .28),
             opp=None, outcome="", first_call_delay=None)
    contacts.append(c)
    return c

# ---------------------------------------------------------------- opportunity helpers
def opp_new(c, t):
    c["opp"] = dict(id=gid(), stage="New Lead", status="open", created=t, updated=t, stage_t=t, status_t=t,
                    value=R.choice([4400, 4400, 4400, 0, ""]), lost="", notes="")

def opp_set(c, t, stage=None, status=None, lost="", value=None):
    o = c["opp"]
    if t > END:
        return
    if stage and stage != o["stage"]:
        o["stage"], o["stage_t"] = stage, t
    if status and status != o["status"]:
        o["status"], o["status_t"] = status, t
    if lost:
        o["lost"] = lost
    if value is not None:
        o["value"] = value
    o["updated"] = max(o["updated"], t)

# ---------------------------------------------------------------- scheduling helpers
def consult_slot(t_booked, days_out):
    d = (t_booked + TD(days=days_out)).date()
    while True:
        wd = d.weekday()
        if wd == 6:
            d += TD(days=1); continue
        hour = R.choice([9, 10, 11]) if wd == 5 else R.choice([8, 9, 10, 11, 13, 14, 15, 16])
        return DT(d.year, d.month, d.day, hour, R.choice([0, 30]))

def day_str(t):
    return t.strftime("%A %b ") + str(t.day)

def time_str(t):
    return t.strftime("%I:%M %p").lstrip("0")

def responder(c, t):
    """Who answers an inbound text at time t: ('agent', time) or ('ai', time)."""
    if is_open(t):
        return "agent", mins(t, 1.5, 28 * c["agent"]["speed"])
    if t >= AI_TEXT_LAUNCH:
        return "ai", sec(t, 20, 95)
    return "agent", agent_time(t, (3, 60))

def reply(c, t, kind, body_agent, body_ai=None):
    who, rt = kind
    if who == "agent":
        return sms_out(c, rt, fill(body_agent, c), "agent", c["agent"]), rt
    return sms_out(c, rt, fill(body_ai or body_agent, c), "ai"), rt

# ---------------------------------------------------------------- booking flow
def book(c, t, via, by="agent"):
    """Create appointment and run reminders/show/surgery downstream. Returns end time."""
    days_out = R.choices([1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 20], [8, 12, 12, 11, 10, 9, 10, 9, 8, 6, 5])[0]
    start = consult_slot(t, days_out)
    if start <= t:
        start = consult_slot(t + TD(days=1), 1)
    return run_appointment(c, t, start, via, by)

def run_appointment(c, t, start, via, by, attempt=1):
    a = dict(id=gid(), contact=c, calendar=f"Free LASIK Consult - {c['loc']}", start=start,
             end=start + TD(minutes=90), status="confirmed", created=t, created_by=by, user=c["agent"])
    appts.append(a)
    opp_set(c, t, "Consult Scheduled")
    c["tags"].add("consult booked")
    enroll_t = t
    sms_out(c, sec(t, 30, 120), fill(T.WF03_CONFIRM, c, day=day_str(start), time=time_str(start)))
    email_out(c, sec(t, 60, 200), fill(T.WF03_CONFIRM_EMAIL, c, day=day_str(start), time=time_str(start)))
    days_out = (start.date() - t.date()).days
    confirmed = False
    # pre-visit reschedule
    if R.random() < .08 and days_out >= 3:
        rt = at_day(t, R.randint(1, max(1, days_out - 1)), (7, 21))
        sms_in(c, rt, pick(T.IN_RESCHEDULE))
        who = responder(c, rt)
        m, rt2 = reply(c, rt, who, "No problem! What day works better?", "No problem! What day works better for you?")
        sms_in(c, mins(rt2, 2, 120), pick(T.IN_SCHEDULE))
        new_start = consult_slot(start, R.randint(3, 10))
        a["status"] = "cancelled"
        enroll(c, 3, enroll_t, "finished", rt, "appointment cancelled")
        sms_out(c, mins(rt2, 10, 180), fill(pick(T.AGENT_BOOKED_TEXT), c, day=day_str(new_start), time=time_str(new_start)), "agent", c["agent"])
        if attempt < 3:
            return run_appointment(c, mins(rt2, 12, 185), new_start, "reschedule", by, attempt + 1)
    if days_out >= 4:
        t3 = (start - TD(days=3)).replace(hour=10, minute=R.randint(0, 20))
        sms_out(c, t3, fill(T.WF03_3DAY, c, day=day_str(start), time=time_str(start)))
        if R.random() < .45:
            sms_in(c, mins(t3, 1, 240), pick(T.IN_CONFIRM)); confirmed = True
    if days_out >= 1:
        t1 = (start - TD(days=1)).replace(hour=R.choice([10, 11]), minute=R.randint(0, 30))
        if t1 > t:
            sms_out(c, t1, fill(T.WF03_1DAY, c, time=time_str(start)))
            if R.random() < .35:
                sms_in(c, mins(t1, 1, 300), pick(T.IN_CONFIRM)); confirmed = True
    t2h = start - TD(hours=2)
    if t2h > t:
        sms_out(c, t2h, fill(T.WF03_2HR, c, time=time_str(start)))
        if R.random() < .05:
            sms_in(c, mins(t2h, 60, 110), pick(T.IN_LATE))
    if start > END:
        a["status"] = "confirmed"
        enroll(c, 3, enroll_t, "active")
        c["outcome"] = "booked_upcoming"
        return start
    p_show = .86 - .022 * max(0, days_out - 5) + (.05 if confirmed else 0) - (.08 if c["src"] in ("Facebook", "Instagram") else 0)
    enroll(c, 3, enroll_t, "finished", start, "appointment time reached")
    if R.random() > p_show:
        a["status"] = "noshow"
        opp_set(c, start + TD(hours=1), "No-Show")
        c["tags"].add("no-show")
        n1 = start + TD(hours=1, minutes=R.randint(0, 20))
        enroll(c, 4, n1, "finished", n1 + TD(days=4), "completed")
        sms_out(c, n1, fill(T.WF04[0], c))
        call(c, agent_time(at_day(start, 1, (9, 16))), "outbound", R.choice(["no-answer", "voicemail", "completed"]), R.randint(20, 200), c["agent"])
        if R.random() < .36 and attempt < 3:
            rt = mins(n1, 20, 60 * 30)
            sms_in(c, rt, pick(["So sorry! Can I reschedule?", "I forgot 🤦 can we do next week?", "Sorry something came up. Can I rebook?"]))
            who = responder(c, rt)
            nstart = consult_slot(rt, R.randint(2, 9))
            offer = lambda s: s.replace("{day}", day_str(nstart)).replace("{time}", time_str(nstart))
            m, rt2 = reply(c, rt, who, offer(pick(T.AGENT_OFFER_TIMES)), offer(T.AI_ANSWERS["schedule"][0]))
            sms_in(c, mins(rt2, 1, 90), pick(T.IN_ACCEPT))
            return run_appointment(c, mins(rt2, 2, 95), nstart, "no-show rebook", "Conversation AI" if who[0] == "ai" else by, attempt + 1)
        sms_out(c, at_day(start, 1, (10, 17)), fill(T.WF04[1], c))
        sms_out(c, at_day(start, 3, (10, 17)), fill(T.WF04[2], c))
        opp_set(c, start + TD(days=R.randint(10, 30)), status="lost", lost="No-Show - Unresponsive") if R.random() < .6 else None
        c["outcome"] = "no_show"
        return start
    a["status"] = "showed"
    opp_set(c, start + TD(hours=2), "Consult Showed")
    c["tags"].add("consult showed")
    if R.random() > .88:
        opp_set(c, start + TD(hours=3), status="lost", lost="Not a Candidate")
        c["outcome"] = "showed_not_candidate"
        return start
    procedure = "EVO ICL" if c["procedure"] == "EVO ICL" or R.random() < .05 else ("PRK" if R.random() < .1 else "LASIK")
    value = {"LASIK": R.choice([4400, 4400, 4800, 5200]), "PRK": 4000, "EVO ICL": 9000}[procedure]
    p_surg = .60 - (.12 if c["fin"] else 0) + (.06 if c["src"] == "Referral" else 0)
    if R.random() < p_surg:
        st = start + TD(hours=R.randint(2, 24 * 14))
        opp_set(c, st, "Surgery Scheduled", "won", value=value)
        c["tags"].add("surgery booked")
        c["outcome"] = "won"
        c["won"] = (st, value, procedure)
        return st
    pc = start + TD(days=2)
    enroll(c, 9, pc, "finished", pc + TD(days=14), "completed")
    for i, dd in enumerate([2, 7, 14]):
        sms_out(c, at_day(start, dd, (10, 17)), fill(T.WF09[i], c))
    if c["fin"]:
        enroll(c, 6, at_day(start, 2), "finished", at_day(start, 9), "completed")
        sms_out(c, at_day(start, 3, (10, 17)), fill(T.WF06[0], c))
    if R.random() < .14:
        rt = at_day(start, R.randint(8, 40), (9, 20))
        sms_in(c, rt, pick(["Ok I'm ready to schedule surgery", "Got approved for financing! What dates do you have?", "Hi, I'd like to move forward"]))
        who = responder(c, rt)
        reply(c, rt, who, "That's awesome {first}!! Let me get you scheduled - one sec 🎉", "Congratulations! I'll have a coordinator call you shortly to schedule your procedure.")
        opp_set(c, mins(rt, 30, 600), "Surgery Scheduled", "won", value=value)
        c["outcome"] = "won_late"
        c["won"] = (rt, value, procedure)
        return rt
    reason = R.choices(["Price", "Wants to Think About It", "Went Elsewhere", "Timing", ""], [40, 22, 14, 12, 12])[0]
    if reason:
        opp_set(c, start + TD(days=R.randint(14, 45)), status="lost", lost=reason)
    c["outcome"] = "showed_no_surgery"
    return start

# ---------------------------------------------------------------- text-booking conversation
def text_booking(c, t_in, opener=None, can_fail=False):
    """Lead texts in at t_in; returns appointment time or None."""
    sms_in(c, t_in, opener or pick(T.IN_OPEN))
    opp_set(c, t_in, "Engaged")
    t = t_in
    who = responder(c, t)
    if R.random() < .55:
        topic = pick(list(T.IN_QUESTION))
        if who[0] == "agent" or R.random() < .5:
            m, t = reply(c, t, who, pick(T.AGENT_ANSWERS[topic]), pick(T.AI_ANSWERS[topic]))
        else:
            m, t = reply(c, t, who, pick(T.AI_GREETING_REPLY), pick(T.AI_GREETING_REPLY))
        t = mins(t, 1, 180)
        sms_in(c, t, pick(T.IN_QUESTION[topic]) if R.random() < .3 else pick(T.IN_SCHEDULE))
        who = responder(c, t)
    nstart = consult_slot(t, R.choices([1, 2, 3, 5, 7, 10, 14], [10, 15, 15, 15, 15, 15, 15])[0])
    body = pick(T.AGENT_OFFER_TIMES) if who[0] == "agent" else pick(T.AI_ANSWERS["schedule"])
    m, t = reply(c, t, who, body.replace("{day}", day_str(nstart)).replace("{time}", time_str(nstart)),
                 T.AI_ANSWERS["schedule"][0].replace("{day}", day_str(nstart)).replace("{time}", time_str(nstart)))
    t = mins(t, 1, 240)
    if can_fail and R.random() < .3:
        sms_in(c, t, pick(T.IN_LATER))
        return None
    sms_in(c, t, pick(T.IN_ACCEPT))
    t = mins(t, .5, 6) if who[0] == "agent" else sec(t, 15, 60)
    if who[0] == "agent":
        sms_out(c, t, fill(pick(T.AGENT_BOOKED_TEXT), c, day=day_str(nstart), time=time_str(nstart)), "agent", c["agent"])
    else:
        sms_out(c, t, fill(T.AI_BOOKED[0], c, day=day_str(nstart), time=time_str(nstart)), "ai")
    return run_appointment(c, t, nstart, "text", "Conversation AI" if who[0] == "ai" else c["agent"]["name"])

# ---------------------------------------------------------------- voice AI on main line
def voice_ai_call(c, t, existing):
    dur = R.randint(28, 85) if existing else R.randint(22, 60)
    if R.random() < .06:
        kind, dur = "other", R.randint(4, 30)
    else:
        kind = "existing" if existing else "new"
    call(c, t, "inbound", "completed", dur, None, MAIN_LINE, "Website", voice_ai=True)
    summ = {"existing": T.VAI_SUMMARY_EXISTING, "new": T.VAI_SUMMARY_NEW, "other": T.VAI_SUMMARY_OTHER}[kind]
    tr = {"existing": T.VAI_TRANSCRIPT_EXISTING, "new": T.VAI_TRANSCRIPT_NEW, "other": T.VAI_TRANSCRIPT_OTHER}[kind]
    vai_logs.append({"Call ID": gid(), "Date & Time": fus(t), "Contact ID": c["id"], "Contact Name": c["name_raw"],
                     "From": c["phone"], "To": MAIN_LINE, "Agent": T.VAI_AGENT, "Duration (sec)": dur,
                     "Call Status": "Connected",
                     "Caller Type": {"existing": "Existing Patient", "new": "New Patient", "other": "Other"}[kind],
                     "Action Taken": {"existing": "Transferred to Front Desk", "new": "Transferred to Boost Concierge", "other": "Call Ended"}[kind],
                     "Summary": pick(summ).format(month=pick(["March", "June", "August", "last year"]), loc=c["loc"]),
                     "Transcript": tr.format(clinic=T.CLINIC),
                     "Sentiment": R.choices(["Positive", "Neutral", "Negative"], [35, 55, 10])[0], "_t": t})
    if kind == "existing" and R.random() < .8:
        c["tags"].add("existing patient")
    return kind, t + TD(seconds=dur)

def inbound_call_lead(c, t, number, src_name):
    """Lead calls in. Returns (answered_bool, end_time, by)."""
    sat_end = 13 if t < SAT_STAFF_FIX else 16
    if number == MAIN_LINE and t >= VOICE_AI_LAUNCH:
        kind, t = voice_ai_call(c, t, False)
        if kind == "other":
            return False, t, None
    open_ = is_open(t, sat_end)
    busy = .08 if t.weekday() < 5 else (.45 if t < SAT_STAFF_FIX else .1)
    if not open_ or R.random() < busy:
        st = "voicemail" if R.random() < .3 else "no-answer"
        call(c, t, "inbound", st, R.randint(15, 50) if st == "voicemail" else 0, None, number, src_name)
        tb = sec(t, 40, 120)
        enroll(c, 7, tb, "finished", tb, "completed")
        sms_out(c, tb, fill(pick(T.WF07), c))
        return False, tb, None
    dur = R.randint(180, 620)
    call(c, t, "inbound", "completed", dur, c["agent"], number, src_name)
    return True, t + TD(seconds=dur), c["agent"]

# ---------------------------------------------------------------- the lead lifecycle
SPEED_BANDS = [(5, 1.5), (15, 1.25), (60, 1.0), (240, .8), (1440, .65), (1e9, .5)]
slow_days = {}

def first_call_time(c, t0):
    a = c["agent"]
    if is_open(t0):
        d = t0.date()
        if d not in slow_days:
            slow_days[d] = R.random() < .13
        base = math.exp(R.gauss(math.log(4), 1.15)) * a["speed"] * (8 if slow_days[d] else 1) * (2.5 if t0.weekday() == 5 else 1)
        t = t0 + TD(minutes=min(base, 60 * 26))
        return agent_time(t)
    return agent_time(t0, (4, 80))

def simulate_lead(c):
    t0 = c["created"]
    s = SOURCES[c["src"]]
    opp_new(c, t0)
    ai_era = t0 >= AI_TEXT_LAUNCH
    after_hours = not is_open(t0)

    # ---- entry touch
    if s["kind"] == "form":
        forms.append(dict(contact=c, form=s["form"], t=t0, camp=pick(s["camps"]), utm=s["utm"]))
    elif s["kind"] == "chat":
        msg(c, t0, "TYPE_WEBCHAT", "inbound", "delivered", pick(["Hi how much is lasik?", "Do you do free consults?", "Hi! Interested in LASIK, can someone text me?", "what are your hours"]), ctype="text/plain")
        forms.append(dict(contact=c, form=s["form"], t=t0, camp="", utm=("", "")))

    if s["kind"] == "call":
        answered, t_end, by = inbound_call_lead(c, t0, TRACKING["Google Business Profile"], "Google Business Profile")
        c["first_call_delay"] = 0 if answered else None
        if answered and R.random() < s["book"] * 1.8:
            opp_set(c, t_end, "Engaged")
            sms_out(c, sec(t_end, 30, 200), fill("Thanks for calling {first}! You'll get a confirmation text with your consult details in just a sec. -{agent}", c), "agent", c["agent"])
            book(c, t_end, "inbound call")
            return
        fc = agent_time(t_end + TD(minutes=R.randint(5, 240))) if not answered else None
    else:
        enroll(c, 1, t0, "finished", t0 + TD(minutes=5), "completed")
        sms_out(c, sec(t0, 15, 75), fill(pick(T.WF01_SMS), c))
        email_out(c, sec(t0, 90, 240), fill(T.WF01_EMAIL[0], c))
        fc = first_call_time(c, t0)
        if c["fin"]:
            enroll(c, 6, t0, "finished", t0 + TD(days=7), "completed")

    delay_min = (fc - t0).total_seconds() / 60 if fc else 0
    c["first_call_delay"] = round(delay_min, 1) if fc else c["first_call_delay"]
    sm = next(m for lim, m in SPEED_BANDS if delay_min < lim)
    if after_hours and ai_era and s["kind"] != "call":
        # Conversation AI engages within minutes, so the slow next-morning callback no longer hurts
        sm = 1.3
        msg_t = sec(t0, 120, 300)
        sms_out(c, msg_t, fill("Hi {first}, this is the virtual assistant for {clinic} - our team is out for the night but I can get your free consult booked right now. What day works best for you?", c), "ai")
    p_book = s["book"] * sm * c["agent"]["mult"]
    if after_hours and not ai_era:
        p_book *= .8
    p_book = min(.72, p_book)
    if c["invalid"]:
        p_book = 0
    r = R.random()
    p_opt = .05 * s["opt"]
    if r < p_book:
        outcome = "book"
    elif r < p_book + p_opt:
        outcome = "optout"
    elif r < p_book + p_opt + .30 * (1 - p_book) and not c["invalid"]:
        outcome = "engaged_no"
    else:
        outcome = "ghost"
    c["outcome"] = outcome
    target_day = R.choices([0, 1, 2, 3, 5, 7, 10, 14, 21], [42, 14, 9, 7, 8, 7, 5, 5, 3])[0]
    if outcome == "optout":
        target_day = R.choices([1, 2, 3, 5, 7, 10, 14, 21, 30], [8, 8, 8, 8, 10, 8, 10, 30, 10])[0]

    # ---- build cadence
    touches = []
    if fc:
        touches.append((fc, "call", 0))
        touches.append((agent_time(fc + TD(hours=R.randint(2, 5))), "call", 0))
    for d in [1, 2, 3, 5, 7, 10, 14, 21, 30]:
        touches.append((wf_time(at_day(t0, d, (t0.hour if 9 <= t0.hour < 19 else 10,) * 2)), "sms", d))
    for d in [1, 3, 7, 14, 30]:
        touches.append((wf_time(at_day(t0, d, (8, 11))), "email", d))
    for d in [2, 10]:
        touches.append((wf_time(at_day(t0, d, (11, 16))), "rvm", d))
    for d in [1, 2, 4, 7, 10, 14, 21]:
        touches.append((agent_time(at_day(t0, d, (9, 17))), "call", d))
    touches.sort(key=lambda x: x[0])
    enroll(c, 2, wf_time(at_day(t0, 1)), "active")
    wf2 = enrolls[-1]

    opp_set(c, fc or t0, "Attempting Contact")
    done = False
    for (t, kind, d) in touches:
        if t > END:
            break
        hit = d >= target_day and outcome in ("book", "optout", "engaged_no") and not done
        if kind == "call":
            if c["dnd_calls"]:
                continue
            if hit and outcome == "book" and R.random() < (.6 if d == 0 else .35):
                dur = R.randint(240, 760)
                call(c, t, "outbound", "completed", dur, c["agent"])
                te = t + TD(seconds=dur)
                opp_set(c, te, "Engaged")
                tmp_start = None
                book_end = book(c, te, "outbound call")
                # agent personal confirmation (generic, appointment text follows from WF03)
                sms_out(c, sec(te, 20, 90), fill("Great chatting {first}! You'll get your confirmation text in just a sec. Text me here if anything comes up. -{agent}", c), "agent", c["agent"])
                done = True
                break
            if c["invalid"]:
                call(c, t, "outbound", R.choice(["failed", "failed", "no-answer"]), 0, c["agent"])
                continue
            st = R.choices(["no-answer", "voicemail", "busy", "completed"], [58, 30, 5, 7])[0]
            dur = {"no-answer": 0, "busy": 0, "voicemail": R.randint(22, 48), "completed": R.randint(15, 70)}[st]
            call(c, t, "outbound", st, dur, c["agent"])
            if d == 0 and st in ("no-answer", "voicemail") and R.random() < .6:
                sms_out(c, sec(t, 40, 240), fill(pick(T.AGENT_AFTER_NO_ANSWER), c), "agent", c["agent"])
        elif kind == "sms":
            body = fill(pick(T.WF02_SMS[d]), c)
            m = sms_out(c, t, body)
            if not m or m["status"] == "failed":
                continue
            if hit:
                rt = mins(t, 1, 60 * R.choice([.2, 1, 3, 8]))
                if outcome == "book":
                    text_booking(c, rt)
                    done = True
                    break
                if outcome == "optout":
                    c["optout_t"] = rt
                    if R.random() < .78:
                        sms_in(c, rt, pick(T.IN_STOP_STANDARD))
                        c["dnd_sms_at"] = rt
                    else:
                        sms_in(c, rt, pick(T.IN_STOP_NONSTANDARD))
                        c["dnd_flag_pending"] = True
                        lag = TD(hours=R.choice([2, 20, 60, 140]))
                        c["dnd_sms_at"] = rt + lag
                        sms_out(c, agent_time(rt + lag - TD(minutes=5)), fill("Sorry about that {first}, you've been removed from our list.", c), "agent", c["agent"])
                    c["dnd_calls"] = R.random() < .7
                    c["tags"].add("dnd")
                    opp_set(c, rt, status="lost", lost="Opted Out")
                    wf2.update(status="finished", exitedAt=fz(rt), exitReason="contact DND")
                    done = True
                    continue
                if outcome == "engaged_no":
                    done = True
                    branch = R.choices(["question_then_no", "not_interested", "later", "wrong", "who_then_silent"], [32, 25, 23, 7, 13])[0]
                    if branch == "question_then_no":
                        topic = pick(list(T.IN_QUESTION))
                        sms_in(c, rt, pick(T.IN_QUESTION[topic]))
                        who = responder(c, rt)
                        _, rt2 = reply(c, rt, who, pick(T.AGENT_ANSWERS[topic]), pick(T.AI_ANSWERS[topic]))
                        if R.random() < .6:
                            sms_in(c, mins(rt2, 5, 600), pick(T.IN_NOT_INTERESTED + T.IN_LATER))
                        lost = "Price" if topic in ("price", "financing", "insurance") else R.choice(["Not Interested", "No Response"])
                        opp_set(c, mins(rt2, 60, 3000), "Engaged", "lost", lost)
                    elif branch == "not_interested":
                        sms_in(c, rt, pick(T.IN_NOT_INTERESTED))
                        who = responder(c, rt)
                        _, rt2 = reply(c, rt, who, pick(T.AGENT_CLOSE_NOT_INTERESTED), pick(T.AGENT_CLOSE_NOT_INTERESTED))
                        opp_set(c, rt2, status="lost", lost=R.choice(["Not Interested", "Went Elsewhere", "Price"]))
                    elif branch == "later":
                        sms_in(c, rt, pick(T.IN_LATER))
                        who = responder(c, rt)
                        _, rt2 = reply(c, rt, who, pick(T.AGENT_LATER), pick(T.AGENT_LATER))
                        opp_set(c, rt2, "Long-Term Nurture")
                        c["nurture_from"] = rt2
                    elif branch == "wrong":
                        sms_in(c, rt, pick(T.IN_WRONG))
                        who = responder(c, rt)
                        reply(c, rt, who, T.AGENT_WRONG_NUMBER[0], T.AGENT_WRONG_NUMBER[0])
                        c["dnd_sms_at"] = mins(rt, 5, 600); c["dnd_calls"] = True
                        opp_set(c, rt, status="lost", lost="Wrong Number")
                    else:
                        sms_in(c, rt, pick(T.IN_QUESTION["who"]))
                        who = responder(c, rt)
                        reply(c, rt, who, pick(T.AGENT_ANSWERS["who"]), pick(T.AI_ANSWERS["who"]))
                    wf2.update(status="finished", exitedAt=fz(rt), exitReason="contact replied")
                    if branch != "later":
                        break
        elif kind == "email":
            email_out(c, t, fill(T.WF02_EMAIL[d], c))
        elif kind == "rvm":
            rvm(c, t)

    # ---- ghosts: a little noise
    if outcome in ("book", "optout", "engaged_no") and not done:
        c["outcome"] = "in_progress" if outcome == "book" else "ghost"
        outcome = "ghost"
    if outcome == "ghost" and not c["invalid"]:
        if R.random() < .1:
            rt = mins(t0, 60 * 24, 60 * 24 * 20)
            sms_in(c, rt, pick(T.IN_QUESTION["who"] + ["Hi", "Is this the eye place?"]))
            reply(c, rt, responder(c, rt), pick(T.AGENT_ANSWERS["who"]), pick(T.AI_ANSWERS["who"]))
        if R.random() < .1:
            rt = mins(t0, 60 * 6, 60 * 24 * 25)
            src_name, num = (c["src"], TRACKING.get(c["src"] if c["src"] in TRACKING else "Website", MAIN_LINE))
            answered, te, _ = inbound_call_lead(c, rt, num if R.random() < .5 else MAIN_LINE, src_name)
            if answered and R.random() < .4:
                book(c, te, "inbound call")
                c["outcome"] = "book_callback"
                return
        if R.random() < .04 and c["src"] in ("Facebook", "Instagram") and not c["invalid"]:
            sms_in(c, mins(t0, 60, 60 * 24 * 5), pick(T.IN_MMS_CAPTION), attachments='["https://storage.example.com/mms/' + gid(12) + '.jpg"]', ctype="image/jpeg")

    # ---- end of 30-day nurture
    if not done and wf2["status"] == "active":
        end30 = at_day(t0, 31)
        if end30 <= END:
            wf2.update(status="finished", exitedAt=fz(end30), exitReason="completed")
            opp_set(c, end30, "Long-Term Nurture")
            c["nurture_from"] = end30
            if R.random() < .45:
                opp_set(c, end30 + TD(days=R.randint(10, 60)), status="lost", lost="No Response")

    # ---- long-term nurture
    nf = c.get("nurture_from")
    if nf and not c["dnd_sms_at"]:
        enroll(c, 5, nf, "active")
        k = 0
        t = nf + TD(days=R.randint(25, 35))
        while t <= END and k < 6:
            m = sms_out(c, wf_time(t.replace(hour=R.randint(10, 17))), fill(T.WF05[(t.month + k) % len(T.WF05)], c))
            if m and m["status"] == "delivered":
                r = R.random()
                if r < .035:
                    appt_end = text_booking(c, mins(t, 2, 600), "YES", can_fail=True)
                    c["outcome"] = "revived_" + c["outcome"]
                    enrolls[-1]  # noqa
                    return
                if r < .055:
                    rt = mins(t, 2, 600)
                    sms_in(c, rt, pick(T.IN_STOP_STANDARD))
                    c["dnd_sms_at"] = rt
                    opp_set(c, rt, status="lost", lost="Opted Out")
                    return
            t += TD(days=R.randint(28, 34))
            k += 1

# ---------------------------------------------------------------- existing patient calls on the new-patient line
ep_pool = []
def existing_patient_calls():
    t = START.replace(hour=0, minute=0)
    while t < END:
        # calls arrive mostly during open hours, some after hours
        rate = args.ep_rate * (1.0 if is_open(t) else (.08 if 7 <= t.hour < 21 else 0))
        rate *= min(1.0, (args.leads / max(1, (END - START).days)) / 16.7)
        n = sum(1 for _ in range(int(rate * 3) + 1) if R.random() < rate / (int(rate * 3) + 1))
        for _ in range(n):
            ct = t + TD(minutes=R.randint(0, 59), seconds=R.randint(0, 59))
            if ep_pool and R.random() < .35:
                c = pick(ep_pool)
            else:
                c = new_contact(ct, None, existing=True)
                c["src_label"] = R.choice(["inbound call", "Inbound Call", "", "call"])
                c["agent"] = None
                ep_pool.append(c)
            if ct >= VOICE_AI_LAUNCH:
                voice_ai_call(c, ct, True)
            elif is_open(ct) and R.random() < .9:
                user = pick(active_agents(ct))
                dur = int(min(1100, math.exp(R.gauss(math.log(205), .45))))
                call(c, ct, "inbound", "completed", dur, user, MAIN_LINE, "Website")
                if R.random() < .7:
                    c["tags"].add("existing patient")
            else:
                st = "voicemail" if R.random() < .5 else "no-answer"
                call(c, ct, "inbound", st, R.randint(10, 60) if st == "voicemail" else 0, None, MAIN_LINE, "Website")
                if ct < VOICE_AI_LAUNCH:
                    c.setdefault("agent", None)
                    tb = sec(ct, 40, 120)
                    c2 = c
                    # missed-call text back fires for everyone, existing or not
                    m = msg(c2, tb, "TYPE_SMS", "outbound", "delivered", T.WF07[0].format(clinic=T.CLINIC), None, "workflow", LOCS[c2["loc"]], c2["phone"])
                    if m: c2["sms_out"] += 1
                    if R.random() < .25:
                        msg(c2, mins(tb, 2, 120), "TYPE_SMS", "inbound", "delivered", pick(T.IN_EXISTING_PT), None, "", c2["phone"], LOCS[c2["loc"]])
                        c2["sms_in"] += 1
        t += TD(hours=1)

# ---------------------------------------------------------------- bulk blasts
def bulk_blasts():
    for ds, body in T.BULK.items():
        bt = DT.fromisoformat(ds).replace(hour=11)
        if not (START <= bt <= END):
            continue
        for c in contacts:
            if c["existing"] or c["created"] > bt - TD(days=10) or (c["dnd_sms_at"] and c["dnd_sms_at"] <= bt):
                continue
            o = c["opp"]
            if not o or o["status"] == "won" or o["stage"] in ("Consult Scheduled", "Surgery Scheduled"):
                continue
            t = bt + TD(seconds=R.randint(0, 3600))
            m = sms_out(c, t, body.format(clinic=T.CLINIC), "bulk")
            if m and m["status"] == "delivered":
                r = R.random()
                if r < .025:
                    rt = mins(t, 1, 300); sms_in(c, rt, pick(T.IN_STOP_STANDARD)); c["dnd_sms_at"] = rt
                elif r < .05:
                    rt = mins(t, 1, 900)
                    if R.random() < .5 and c["agent"]:
                        text_booking(c, rt, "YES", can_fail=True)
                        c["outcome"] = "bulk_" + c["outcome"]
                    else:
                        sms_in(c, rt, pick(["YES", "Yes", "how much is it with the discount?", "Is this still going on?"]))

# ---------------------------------------------------------------- main
contacts_leads = []
def lead_times(n):
    season = {11: .85, 12: 1.1, 1: 1.4, 2: 1.2, 3: 1.25, 4: 1.05, 5: .9, 6: .85, 7: .8, 8: .85, 9: .9, 10: .95}
    days = []
    d = START
    while d <= END:
        w = season[d.month] * (1.15 if d.weekday() in (0, 1) else .75 if d.weekday() == 5 else .65 if d.weekday() == 6 else 1)
        days.append((d, w))
        d += TD(days=1)
    hours = list(range(24))
    hw = [1, .5, .3, .2, .2, .4, 1.2, 2.5, 3.5, 4, 4.2, 4.5, 5.5, 5, 4.5, 4.5, 4.8, 5, 5.5, 6.5, 7.5, 7, 5, 2.5]
    out = []
    for _ in range(n):
        dd = R.choices([x[0] for x in days], [x[1] for x in days])[0]
        h = R.choices(hours, hw)[0]
        out.append(dd.replace(hour=h, minute=R.randint(0, 59), second=R.randint(0, 59)))
    return sorted(out)

for t0 in lead_times(args.leads):
    src = R.choices(SRC_NAMES, [SOURCES[s]["w"] for s in SRC_NAMES])[0]
    if src == "Vision Fair Event":
        t0 = t0.replace(hour=R.choice([10, 14]), minute=R.randint(0, 5))
    c = new_contact(t0, src)
    contacts_leads.append(c)

# duplicates: same person submits again with a different email
for c in R.sample(contacts_leads, k=max(1, int(len(contacts_leads) * .025))):
    t = c["created"] + TD(days=R.randint(1, 45), minutes=R.randint(0, 600))
    if t > END:
        continue
    d = new_contact(t, c["src"])
    used_phones.discard(d["phone"])
    d.update(first_clean=c["first_clean"], first=c["first_clean"].lower(), last=c["last"], name_raw=c["name_raw"],
             phone=c["phone"], loc=c["loc"], invalid=c["invalid"], duplicate_of=c["id"])
    d["email"] = c["email"].replace("@", str(R.randint(1, 9)) + "@") if R.random() < .6 else c["email"].upper()
    contacts_leads.append(d)

for c in sorted(contacts_leads, key=lambda x: x["created"]):
    simulate_lead(c)
existing_patient_calls()
bulk_blasts()

# ---------------------------------------------------------------- write files
os.makedirs(args.out, exist_ok=True)

def write(name, rows, cols):
    with open(os.path.join(args.out, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

MSG_COLS = ["id", "direction", "status", "type", "locationId", "attachments", "body", "contactId", "contentType",
            "conversationId", "dateAdded", "dateUpdated", "userId", "source", "from", "to", "error", "messageType"]
messages.sort(key=lambda m: m["_t"])
write("ghl_messages_export.csv", messages, MSG_COLS)

call_report.sort(key=lambda r: r["_t"], reverse=True)
write("ghl_call_reporting_export.csv", call_report,
      ["Date & Time", "Contact Name", "Contact Phone", "Direction", "Call Status", "Duration", "Source", "Number", "User", "First Time Caller", "Recording"])

vai_logs.sort(key=lambda r: r["_t"], reverse=True)
write("ghl_voice_ai_call_logs.csv", vai_logs,
      ["Call ID", "Date & Time", "Contact ID", "Contact Name", "From", "To", "Agent", "Duration (sec)", "Call Status", "Caller Type", "Action Taken", "Summary", "Transcript", "Sentiment"])

crow = []
for c in contacts:
    s = SOURCES.get(c["src"] or "", {})
    form = next((f for f in forms if f["contact"] is c), None)
    dnd_any = bool(c["dnd_sms_at"] and c["dnd_sms_at"] <= END) or c["dnd_calls"]
    crow.append({"Contact Id": c["id"], "First Name": c["first"], "Last Name": c["last"], "Phone": c["phone"],
                 "Email": c["email"], "Created": fl(c["created"]), "Last Activity": fl(c["last_activity"]),
                 "Tags": ",".join(sorted(c["tags"] | ({"new lead"} if not c["existing"] else set()))),
                 "Source": c["src_label"], "Assigned To": c["agent"]["name"] if c["agent"] else "",
                 "City": c["city"], "State": "MN", "Postal Code": c["zip"],
                 "DND": "true" if dnd_any else "false",
                 "DND SMS": "true" if c["dnd_sms_at"] and c["dnd_sms_at"] <= END else "false",
                 "DND Calls": "true" if c["dnd_calls"] else "false",
                 "SMS Outgoing Count": c["sms_out"], "SMS Incoming Count": c["sms_in"],
                 "First SMS Time": fl(c["first_sms"]) if c["first_sms"] else "", "Last SMS Time": fl(c["last_sms"]) if c["last_sms"] else "",
                 "Procedure Interest": "" if c["existing"] else c["procedure"],
                 "Preferred Location": "" if c["existing"] or R.random() < .1 else c["loc"],
                 "Currently Wears": "" if c["existing"] or R.random() < .15 else c["wears"],
                 "Age Range": "" if c["existing"] or R.random() < .2 else c["age"],
                 "Interested in Financing": "" if c["existing"] else ("Yes" if c["fin"] else R.choice(["No", "No", ""])),
                 "Lead Form": form["form"] if form else "",
                 "utm_source": (form["utm"][0] if form and R.random() > .15 else ""),
                 "utm_medium": (form["utm"][1] if form and R.random() > .15 else ""),
                 "utm_campaign": (form["camp"] if form and R.random() > .2 else "")})
    if not c["existing"]:
        truth.append(dict(contactId=c["id"], true_source=c["src"], outcome=c["outcome"], agent=c["agent"]["name"],
                          first_call_delay_min=c["first_call_delay"], created=fl(c["created"]),
                          after_hours=not is_open(c["created"]), duplicate_of=c.get("duplicate_of", ""),
                          invalid_phone=c["invalid"], texts_after_nonstandard_optout=c["texts_after_optout"],
                          won_value=c.get("won", (None, 0))[1]))
crow.sort(key=lambda r: r["Created"], reverse=True)
write("ghl_contacts_export.csv", crow, list(crow[0].keys()))

orow = []
for c in contacts:
    o = c["opp"]
    if not o:
        continue
    orow.append({"Opportunity Name": f"{c['first']} {c['last']}".strip(), "Contact Name": f"{c['first']} {c['last']}",
                 "phone": c["phone"], "email": c["email"], "pipeline": "LASIK Consults", "stage": o["stage"],
                 "Lead Value": o["value"], "source": c["src_label"], "assigned": c["agent"]["name"] if c["agent"] else "",
                 "Created on": fl(o["created"]), "Updated on": fl(o["updated"]),
                 "lost reason ID": gid(20) if o["lost"] else "", "lost reason name": o["lost"],
                 "Followers": "", "Notes": "", "tags": ",".join(sorted(c["tags"])), "Engagement Score": "",
                 "status": o["status"], "Opportunity ID": o["id"], "Contact ID": c["id"],
                 "Pipeline Stage ID": STAGE_IDS[o["stage"]], "Pipeline ID": PIPELINE_ID,
                 "Days Since Last Stage Change": (EXPORT_AT - o["stage_t"]).days,
                 "Days Since Last Status Change": (EXPORT_AT - o["status_t"]).days,
                 "Days Since Last Updated": (EXPORT_AT - o["updated"]).days})
write("ghl_opportunities_export.csv", orow, list(orow[0].keys()))

arow = []
for a in appts:
    c = a["contact"]
    st = a["status"]
    if a["start"] > END:
        st = "confirmed"
    arow.append({"Appointment ID": gid(), "Contact ID": c["id"], "Contact Name": f"{c['first']} {c['last']}",
                 "Phone": c["phone"], "Email": c["email"], "Calendar": a["calendar"], "Title": f"Free LASIK Consult - {c['name_raw']}",
                 "Start Time": fl(a["start"]), "End Time": fl(a["end"]), "Appointment Status": st,
                 "Assigned To": a["user"]["name"] if a["user"] else "", "Created On": fl(a["created"]),
                 "Created By": a["created_by"] if isinstance(a["created_by"], str) else a["created_by"]})
arow.sort(key=lambda r: r["Start Time"])
write("ghl_appointments_export.csv", arow, list(arow[0].keys()) if arow else ["Appointment ID"])

frow = []
for f in forms:
    c = f["contact"]
    frow.append({"Submission ID": gid(24).lower(), "Form Name": f["form"], "Contact ID": c["id"],
                 "Name": f"{c['first']} {c['last']}", "Email": c["email"], "Phone": pretty_phone(c["phone"]),
                 "Submitted At": fl(f["t"]),
                 "Page URL": {"FB Lead Form - Free Consult Offer": "", "IG Lead Form - Free Consult": "",
                              "Website Chat Widget": "https://lakemontlasik.example.com/"}.get(f["form"], R.choice([
                                  "https://lakemontlasik.example.com/free-consult", "https://lakemontlasik.example.com/lasik-cost",
                                  "https://lakemontlasik.example.com/candidate-quiz", "https://lakemontlasik.example.com/financing"])),
                 "utm_source": f["utm"][0], "utm_medium": f["utm"][1], "utm_campaign": f["camp"],
                 "Currently Wears": c["wears"], "Age Range": c["age"], "Procedure Interest": c["procedure"],
                 "Interested in Financing": "Yes" if c["fin"] else "No",
                 "Message": R.choice(["", "", "", "Best time to call is after 5", "Do you take VSP?", "Interested in both eyes",
                                      "I have astigmatism", "Mornings only please", "Saw your ad on facebook"])})
frow.sort(key=lambda r: r["Submitted At"], reverse=True)
write("ghl_form_submissions_export.csv", frow, list(frow[0].keys()))

write("ghl_workflow_enrollments_api.csv", enrolls,
      ["contactId", "workflowId", "workflowName", "enrolledAt", "status", "exitedAt", "exitReason"])

write("_answer_key_contacts.csv", truth, list(truth[0].keys()))

users = [{"userId": a["id"], "name": a["name"], "role": "Boost Patient Concierge",
          "startDate": a["start"].date().isoformat() if a["start"] > DT(2025, 6, 1) else "",
          "endDate": a["end"].date().isoformat() if a["end"] < DT(2029, 1, 1) else ""} for a in AGENTS]
users.append({"userId": FRONT_DESK["id"], "name": FRONT_DESK["name"], "role": "Client Staff", "startDate": "", "endDate": ""})
write("ghl_users.csv", users, list(users[0].keys()))

# ---------------------------------------------------------------- summary
from collections import Counter
print("contacts", len(contacts), "leads", len(contacts_leads), "existing", len(ep_pool))
print("messages", len(messages), Counter(m["messageType"] for m in messages))
print("calls(report)", len(call_report), "voice ai", len(vai_logs), "appts", len(appts), "forms", len(forms))
print("outcomes", Counter(c["outcome"] for c in contacts_leads))
pre = [s for s in team_seconds if s[0] < VOICE_AI_LAUNCH]
post = [s for s in team_seconds if s[0] >= VOICE_AI_LAUNCH]
def per_lead(rows, a, b):
    leads = sum(1 for c in contacts_leads if a <= c["created"] < b)
    return sum(r[1] for r in rows) / 60 / max(1, leads)
if pre and post:
    pl = per_lead(pre, START, VOICE_AI_LAUNCH); po = per_lead(post, VOICE_AI_LAUNCH, END)
    print(f"team talk min per lead pre {pl:.2f} post {po:.2f} savings {1-po/pl:.1%}")
    print("existing-patient share of pre team time", sum(r[1] for r in pre if r[2] == 'existing') / sum(r[1] for r in pre))
