"""Message copy library for the fictional Lakemont LASIK & Vision account.

Everything here is invented. Merge fields use str.format:
{first} {loc} {agent} {clinic} {day} {time} {link} {phone}
"""

CLINIC = "Lakemont LASIK & Vision"
SHORT = "Lakemont LASIK"

# ---------- Workflow 01: speed to lead ----------
WF01_SMS = [
    "Hi {first}! Thanks for your interest in LASIK at {clinic}. This is the patient care team - when's a good time for a quick call to get your FREE consult on the books? Reply STOP to opt out.",
    "Hi {first}, thanks for reaching out to {clinic}! We got your request for a free LASIK consultation. A patient coordinator will call you shortly from this number. Reply STOP to opt out.",
    "{first}, this is {clinic} 👋 We just got your info! Are you hoping to come in at our {loc} office? Reply STOP to opt out.",
]
WF01_EMAIL = [
    "<p>Hi {first},</p><p>Thanks for requesting a free LASIK consultation with {clinic}! One of our patient coordinators will reach out shortly. Prefer to pick your own time? <a href=\"{link}\">Book here</a>.</p><p>See clearly soon,<br>The {clinic} Team</p>",
]

# ---------- Workflow 02: 30-day new lead nurture (keyed by day) ----------
WF02_SMS = {
    1: ["Hi {first}, it's the {clinic} team! We tried calling yesterday. Your free consult takes about 90 min and includes a full eye mapping. Want me to send a few times this week?",
        "Morning {first}! Quick follow up from {clinic} - would mornings or afternoons work better for your free LASIK consult?"],
    2: ["{first}, did you know most of our patients are back to work the day after LASIK? Happy to answer any questions - just reply here.",
        "Hey {first} - just checking in. Any questions I can answer about LASIK before your free consult?"],
    3: ["Hi {first}! We have a few openings at our {loc} office this week. Want me to grab one for you?"],
    5: ["{first}, lots of people ask about cost - LASIK at {clinic} starts at $2,200/eye and financing starts around $99/mo. Want to see if you qualify? 🙂",
        "Quick q {first} - are you currently wearing glasses, contacts, or both? Helps us prep for your consult."],
    7: ["Hi {first}, it's been a week! Still thinking about LASIK? Our consults are free and there's zero pressure. Reply YES and I'll send times."],
    10: ["{first}, here's what a recent patient said: 'I wish I'd done this 10 years ago.' Want to find out if you're a candidate? Reply YES."],
    14: ["Hi {first}! Checking back in - would you like to schedule your free LASIK consult, or should I check back later?"],
    21: ["Last check-in from {clinic}, {first}! Should we keep your free consult request open? Reply YES to schedule or STOP to opt out."],
    30: ["Hi {first}, we're closing out your consult request. If you ever want to revisit LASIK just text us here anytime!"],
}
WF02_EMAIL = {
    1: "<p>Hi {first},</p><p>What happens at a LASIK consult? We map your corneas, measure your prescription and answer every question. It's free and there's no obligation.</p><p><a href=\"{link}\">Pick a time</a></p>",
    3: "<p>{first}, is LASIK safe? Here are the 5 questions our surgeons hear most - and their honest answers.</p><p><a href=\"{link}\">Read more</a></p>",
    7: "<p>Hi {first}, glasses and contacts add up. Most patients find LASIK pays for itself in under 10 years.</p><p><a href=\"{link}\">See the math</a></p>",
    14: "<p>{first}, financing for LASIK starts around $99/mo with approved credit. <a href=\"{link}\">Check your options</a> - it won't affect your credit score.</p>",
    30: "<p>Hi {first}, we'll stop emailing about your consult request for now. Whenever you're ready, <a href=\"{link}\">we're here</a>.</p>",
}

# ---------- Workflow 03: appointment reminders ----------
WF03_CONFIRM = "You're booked, {first}! ✅ Free LASIK consult at {clinic} - {loc} on {day} at {time}. Please wear glasses instead of contacts for 3 days before. Reply C to confirm."
WF03_CONFIRM_EMAIL = "<p>Hi {first}, your free LASIK consultation is confirmed for <b>{day} at {time}</b> at our {loc} office.</p><p><b>Important:</b> please stop wearing soft contacts 3 days before your visit.</p>"
WF03_3DAY = "Reminder {first}: your LASIK consult is {day} at {time} ({loc}). Don't forget - glasses only starting today! Reply C to confirm or R to reschedule."
WF03_1DAY = "See you tomorrow {first}! {time} at {clinic} {loc}. Plan for about 90 min and bring a driver if possible since we may dilate. Reply R to reschedule."
WF03_2HR = "Hi {first}, see you at {time} today! {clinic} - {loc}. Reply here if you're running late."

# ---------- Workflow 04: no-show ----------
WF04 = [
    "Hi {first}, we missed you today! Totally get it, life happens. Want to pick a new time for your free consult?",
    "{first}, still want to find out if you're a LASIK candidate? We can usually get you in this week - just reply with a day that works.",
    "Hi {first}, last note from us about rescheduling. Reply anytime and we'll get you back on the calendar!",
]

# ---------- Workflow 05: long-term nurture / reactivation ----------
WF05 = [
    "Hi {first}! It's {clinic}. Still thinking about ditching the glasses? We have consult openings this month - reply YES for times.",
    "{first}, new year, new view? 🎉 Free LASIK consults are open in {loc}. Reply YES and we'll send times.",
    "Hi {first}, tax refund season is a popular time for LASIK. Want to see if you're a candidate? Reply YES.",
    "{first}, quick check-in from {clinic} - summer is a great time for LASIK (no fogged-up sunglasses!). Interested in a free consult?",
    "Hi {first}! Have FSA/HSA dollars left before Dec 31? Many patients use them toward LASIK. Reply YES to learn more.",
]

# ---------- Workflow 06: financing ----------
WF06 = [
    "Hi {first}, thanks for checking out financing! Most patients are pre-approved in under 2 min with no hit to credit. Want me to send the link?",
    "{first}, just following up on financing - plans start around $99/mo. Any questions I can answer?",
]

# ---------- Workflow 07: missed call text back ----------
WF07 = [
    "Hi, sorry we missed your call! This is {clinic}. How can we help? You can text us right here.",
    "Sorry we missed you! This is the {clinic} patient care team. Are you calling about a free LASIK consultation?",
]

# ---------- Workflow 09: post consult ----------
WF09 = [
    "Hi {first}, it was great meeting you at your consult! Any questions come up since? Happy to help with next steps.",
    "{first}, just a reminder your consult pricing is good for 30 days. Want to look at surgery dates?",
    "Hi {first}! Checking in - would you like to talk through financing options for your procedure?",
]

# ---------- Bulk blasts ----------
BULK = {
    "2025-11-28": "Black Friday at {clinic}: $500 off LASIK for consults booked by Dec 5! Reply YES to grab a time. Reply STOP to opt out.",
    "2026-03-02": "Tax refund special from {clinic}! $400 off LASIK when you book your free consult in March. Reply YES. Reply STOP to opt out.",
    "2026-07-13": "Summer LASIK event 😎 Free consults + $300 off at {clinic} through July. Reply YES for times. Reply STOP to opt out.",
}

# ---------- Concierge (human) outbound ----------
AGENT_AFTER_NO_ANSWER = [
    "Hi {first}, this is {agent} with {clinic}. Just tried giving you a call about your free LASIK consult! When's a good time to chat?",
    "Hey {first}, {agent} here from {clinic} - sorry I missed you! Do you prefer I text you some times instead?",
    "Hi {first}! {agent} from {clinic}. I left you a voicemail - feel free to text me back here, whatever's easier 🙂",
]
AGENT_AFTER_CALL_BOOKED = [
    "Great chatting {first}! You're all set for {day} at {time} at our {loc} office. You'll get a confirmation text shortly. -{agent}",
    "Thanks {first}! Locked you in for {day} at {time} ({loc}). Text me here if anything comes up. -{agent}",
]
AGENT_OFFER_TIMES = [
    "I have {day} at {time} or the following morning at our {loc} office - would either of those work?",
    "Sure! How about {day} at {time} at {loc}? I can also do a Saturday morning if that's easier.",
    "We have {day} at {time} open in {loc}. Want me to grab it for you?",
]
AGENT_BOOKED_TEXT = [
    "Perfect, you're booked for {day} at {time}! You'll get a confirmation text in a sec. 🎉",
    "Done! {day} at {time} at our {loc} office. See you then {first}!",
]
AGENT_ANSWERS = {
    "price": ["Great question! LASIK at {clinic} starts at $2,200/eye, and the consult is free. We also have financing starting around $99/mo. Want me to find you a consult time?",
              "Pricing depends on your eyes but most patients are between $2,200-$2,800 per eye. The free consult gives you an exact quote. Want to come in?"],
    "financing": ["Yes! We work with CareCredit and Alphaeon - plans start around $99/mo and many are 0% for 12-24 months. Want me to send the pre-qual link?"],
    "candidacy": ["Most adults over 18 with a stable prescription are candidates, but the only way to know for sure is the free eye mapping at your consult. Want to come in this week?"],
    "insurance": ["Most insurance doesn't cover LASIK since it's elective, but some plans (like VSP and EyeMed) offer discounts, and you can use FSA/HSA funds. Want to book a free consult?"],
    "recovery": ["Most patients are back to work the next day! The procedure itself takes about 10 min for both eyes. Want to set up your free consult?"],
    "pain": ["Totally normal question! We use numbing drops so it's not painful - most people say it feels like light pressure for a few seconds. Want to book a consult to learn more?"],
    "who": ["Hi! This is {agent} with {clinic} - you requested info about a free LASIK consult on our website. Still interested?"],
    "schedule": ["Absolutely, let me take a look!"],
}
AGENT_CLOSE_NOT_INTERESTED = [
    "No problem at all {first}, thanks for letting me know! If anything changes just text us here.",
    "Understood! I'll make a note. Wishing you the best {first}!",
]
AGENT_WRONG_NUMBER = ["So sorry about that! I'll remove this number from our list."]
AGENT_LATER = ["Totally understand! Want me to check back in a couple months?", "No rush at all! I'll follow up in a few weeks. 🙂"]

# ---------- Conversation AI (bot) ----------
AI_GREETING_REPLY = [
    "Thanks for the reply, {first}! I can help you schedule your free LASIK consultation. Would mornings or afternoons work better?",
    "Hi {first}! Happy to help. Our {loc} office has consult openings this week - what day works best for you?",
]
AI_ANSWERS = {
    "price": ["Great question! LASIK at {clinic} typically starts at $2,200 per eye, and your consultation is free. Financing is available from about $99/month. Would you like me to find you a consult time?"],
    "financing": ["Yes, we offer financing through CareCredit and Alphaeon, with plans from around $99/month. I can schedule your free consult where the team can go over options. What day works for you?"],
    "candidacy": ["Many adults with a stable prescription are good candidates! The free consultation includes a full eye mapping to confirm. Would you like to book one?"],
    "insurance": ["LASIK is usually considered elective, but many patients use FSA/HSA funds or vision plan discounts. Want me to schedule a free consult so the team can review your options?"],
    "recovery": ["Most patients return to normal activities the next day! Would you like to schedule a free consultation to learn more?"],
    "pain": ["Numbing drops are used, so most patients report only brief pressure. Would you like to book a free consult to talk with the team?"],
    "who": ["Hi! This is the virtual assistant for {clinic}. You recently requested information about a free LASIK consultation. Are you still interested?"],
    "schedule": ["I can help with that! I have {day} at {time} available at our {loc} office. Does that work?"],
}
AI_BOOKED = ["You're all set for {day} at {time} at our {loc} office! You'll receive a confirmation shortly. Anything else I can help with?"]
AI_HANDOFF = [
    "Let me have one of our patient coordinators follow up with you on that first thing tomorrow!",
    "Good question - I'll have a team member reach out to you directly to help with that.",
]

# ---------- Inbound (lead) replies, deliberately messy ----------
IN_OPEN = ["Yes", "yes please", "Yes I'm interested", "Hi yes", "yeah", "Interested!", "Hi! I filled out the form", "Yes. Can you call after 5?", "ok", "yes what times do u have"]
IN_QUESTION = {
    "price": ["How much does it cost?", "how much is lasik", "What's the price for both eyes", "Whats the cost? I just want a ballpark", "how much $$"],
    "financing": ["Do you guys do payment plans?", "Do you take care credit", "is there financing", "Can I make payments?"],
    "candidacy": ["I have astigmatism can I still get it?", "Im 52 is that too old?", "I was told years ago my corneas are thin. Can I still do it?", "Can I get lasik if I have dry eyes?"],
    "insurance": ["Does insurance cover this?", "I have VSP do you take that", "Can I use my HSA?"],
    "recovery": ["How long is recovery? I can't miss much work", "how many days off work"],
    "pain": ["Does it hurt?", "honestly I'm scared, does it hurt", "Am I awake for it?"],
    "who": ["Who is this?", "who is this", "What is this about?", "?"],
}
IN_SCHEDULE = ["Thursday afternoon works", "Do you have anything Saturday?", "Mornings are better", "Next week sometime", "Any evening appts?", "Tues or Wed after 3"]
IN_ACCEPT = ["Yes that works", "Perfect", "Sure!", "That works 👍", "ok book it", "Yes please", "Sounds good"]
IN_CONFIRM = ["C", "c", "Confirmed", "C thank you", "Yes I'll be there", "👍"]
IN_RESCHEDULE = ["R", "Can I reschedule?", "Something came up, need a different day", "I need to move my appt"]
IN_NOT_INTERESTED = ["Not interested", "No thanks", "I'm not interested anymore", "I decided not to do it", "Too expensive for me right now", "I already had it done somewhere else"]
IN_LATER = ["Maybe in a few months", "Not right now, maybe next year", "I'm waiting until after the holidays", "Busy right now, can you check back in the spring?"]
IN_WRONG = ["Wrong number", "You have the wrong person", "I never signed up for this", "who? wrong number"]
IN_STOP_STANDARD = ["STOP", "Stop", "stop", "UNSUBSCRIBE"]
IN_STOP_NONSTANDARD = ["Please stop texting me", "Take me off your list", "remove me", "Stop texting me please", "Don't text me anymore"]
IN_LATE = ["Running about 10 min late sorry!", "Stuck in traffic, be there in 15"]
IN_EXISTING_PT = [
    "Hi I had surgery last month, can I move my post op appt?",
    "This is for Dr. office? I need a copy of my records",
    "My eyes have been really dry since surgery is that normal",
    "Hi, I'm an existing patient. Need to talk to billing",
]
IN_MMS_CAPTION = ["Here's my prescription", "This is my current rx", ""]

# ---------- Voice AI ----------
VAI_AGENT = "Lakemont New Patient Screener"
VAI_SUMMARY_EXISTING = [
    "Caller is an existing patient asking about a post-op appointment. Identified as existing patient and transferred to front desk.",
    "Existing patient calling about billing statement. Transferred to front desk.",
    "Caller had LASIK in {month} and has questions about dry eye drops. Routed to front desk.",
    "Existing patient needed to reschedule a follow-up visit. Transferred to front desk.",
    "Caller requesting medical records for an existing patient. Routed to front desk.",
]
VAI_SUMMARY_NEW = [
    "New patient interested in a LASIK consultation. Confirmed not an existing patient. Transferred to patient concierge.",
    "Caller saw a Google ad and wants pricing and consult availability. New patient. Transferred to concierge team.",
    "New caller asking whether astigmatism disqualifies them. Confirmed new patient and transferred to concierge.",
    "Caller wants to book a free consult at the {loc} office. New patient - transferred to concierge.",
]
VAI_SUMMARY_OTHER = [
    "Caller is a vendor asking for the office manager. Took a message.",
    "Caller hung up during greeting.",
    "Wrong number. Call ended.",
]
VAI_TRANSCRIPT_EXISTING = "AI: Thanks for calling {clinic}! Are you a new patient interested in vision correction, or an existing patient? | Caller: Existing, I had my surgery there. | AI: Thanks! I'll connect you with our front desk team now."
VAI_TRANSCRIPT_NEW = "AI: Thanks for calling {clinic}! Are you a new patient interested in vision correction, or an existing patient? | Caller: New, I wanted to ask about LASIK. | AI: Great! Let me connect you with a patient coordinator who can help you schedule a free consultation."
VAI_TRANSCRIPT_OTHER = "AI: Thanks for calling {clinic}! Are you a new patient interested in vision correction, or an existing patient? | Caller: [no response]"
