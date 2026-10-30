# Lakemont LASIK & Vision: sample GoHighLevel data

A year of fictional lead follow-up data for a made-up 3-location LASIK practice ("Lakemont LASIK & Vision", Twin Cities, MN: Edina, Maple Grove, Woodbury). Boost runs the practice's lead engagement inside GoHighLevel (GHL). The data looks like what you'd get by exporting that GHL sub-account. It's the raw material for the dashboards in this portfolio.

**Everything is invented.** No real patients, practice or messages. Phone numbers use the 555 exchange, emails use `example.com/.net/.org`, and IDs are random.

## Status

- `sample/`: a 60-lead review set across Nov 2025–Oct 2026, small enough to read thread by thread.
- `full/`: the full year. About 6,100 leads plus 1,800 existing patients who call in, 169k message rows, 43k calls, 1,400 Voice AI calls and 2,100 appointments. The message log is split into monthly files in `full/messages/` (by UTC date) to keep each file small. Stack them back together before analysis.

## Why it's split into many files

GHL doesn't have a single export. Each area of the app exports on its own, with its own column names, date formats and quirks. Each file below matches one of those sources. Pulling them together is the point of the demo.

| File | Where it comes from in GHL | One row per |
|---|---|---|
| `ghl_messages_export.csv` | Conversations messages (API / marketplace export). Columns match a real export exactly | message: SMS, call, email, voicemail drop, webchat |
| `ghl_call_reporting_export.csv` | Reporting → Call Reporting → Export | call |
| `ghl_voice_ai_call_logs.csv` | AI Agents → Voice AI → Call Logs → Export | Voice AI call on the main line |
| `ghl_contacts_export.csv` | Contacts → Export (incl. SMS thread stats + custom fields) | contact |
| `ghl_opportunities_export.csv` | Opportunities → Export ("LASIK Consults" pipeline) | opportunity |
| `ghl_appointments_export.csv` | Calendars → appointment list | appointment |
| `ghl_form_submissions_export.csv` | Sites → Forms → Submissions | form submission |
| `ghl_workflow_enrollments_api.csv` | Not a native export; pulled via API | workflow enrollment |
| `ghl_users.csv` | Settings → Team | user (Boost concierges + client front desk) |
| `_answer_key_contacts.csv` | **Not GHL.** Ground truth from the generator (true source, outcome, speed-to-lead) for checking that dashboards find the right answer | lead |

Join key: `contactId` / `Contact ID` / `Contact Id`. The inconsistent naming is how GHL actually exports. `ghl_call_reporting_export.csv` has **no contact ID**; join it on phone number.

## Message export columns

`id, direction, status, type, locationId, attachments, body, contactId, contentType, conversationId, dateAdded, dateUpdated, userId, source, from, to, error, messageType`

- `messageType` / `type`: `TYPE_SMS`/2, `TYPE_CALL`/1, `TYPE_EMAIL`/3, `TYPE_WEBCHAT`/5, `TYPE_CAMPAIGN_VOICEMAIL`/10 (ringless voicemail drop)
- `status`: SMS `delivered/sent/failed/undelivered`; email `delivered/opened/clicked/failed`; calls use GHL call statuses `completed/no-answer/voicemail/busy/failed`
- `source`: `workflow` (automation), `app` (a concierge in the UI, `userId` filled), `api` (Conversation AI texting bot), `bulk_actions` (promo blasts)
- `error`: real Twilio-style codes, e.g. `30007 - Message filtered by carrier`, `30006 - Landline or unreachable carrier`
- Timestamps are UTC (`...Z`). Other files use local Central time, in different formats.

## Who's doing the work

- **Workflows:** speed-to-lead text/email, a 30-day nurture, consult reminders (3-day / 1-day / 2-hour), no-show recovery, monthly long-term nurture, financing, missed-call text back, post-consult follow-up
- **Boost patient concierges** (Maya, Derek, Priya, Jordan → left June 2026, Sam → started July 2026): outbound calls, personal texts, booking
- **Conversation AI** (from Jan 12, 2026): answers texts after hours and books consults
- **Voice AI** (from May 11, 2026): answers the main line and screens callers. Existing patients go to the client's front desk, and only new patients reach Boost.

## Stories planted in the data

| Question | What the data shows |
|---|---|
| Does speed to lead matter? | For leads that arrive during business hours, the booking rate falls from ~45% (called within 5 min) to ~32% (5–15 min) and ~25% (over an hour) |
| Which sources actually convert? | Facebook brings ~1/3 of leads but books worst (~20%). Google Business Profile calls and referrals book best. The CRM `Source` field is messy (`fb_leadgen`, `FB`, `Facebook Lead Ads`, blank…), so this takes real cleanup to see |
| ROI by channel | Opportunity values ($4,000–$9,000) on won deals, tied back to source and UTM campaign |
| How much follow-up does a lead get? | ~13 texts, ~6 calls, ~5 emails and 1–2 voicemail drops per lead, on average, mostly unseen by the practice |
| Voice AI time savings | Concierge talk time per lead drops ~32% after launch, because existing patients no longer reach the team |
| After-hours leads | Before Conversation AI, after-hours leads book at ~19%. After it starts replying within minutes, they book at ~32% |
| Deliverability | Woodbury's texting number gets carrier-filtered (30007) in August 2026: ~35% failure vs ~5% normal |
| Missed calls | Saturday inbound calls go unanswered ~38% of the time, dropping to ~14% after Saturday coverage is added Sept 12 |
| Compliance | Some opt-outs are non-standard ("please stop texting me") and keep getting texts for hours or days until someone flags them |
| Lost reasons | "Price" leads keep receiving promo blasts, and some come back |
| GHL quirks | Outbound voicemails show as `completed` in Call Reporting. Duplicate contacts (same phone, different email) and bad emails are included |

## Regenerate

```bash
cd generator
python3 generate.py --leads 60   --seed 7  --out ../sample   # review set
python3 generate.py --leads 6000 --seed 42 --out ../full     # full set
```

Plain Python 3, no dependencies. `texts.py` holds all message copy.
