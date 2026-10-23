/*
  Portfolio entries. This is the ONLY file that changes when something is added.
  Newest first within each type. Fields:

  id          unique kebab-case slug (used as the card's #anchor)
  type        "app" | "skill" | "dashboard"
  name        display name
  tagline     one sentence: what it does, concretely
  problem     one sentence: the real problem at Boost it solved
  highlights  3–5 short, specific bullets
  stack       tools/tech (short labels)
  stats       optional, up to 3 { value, label } proof points
  links       [{ label, url, primary? }]; first primary link is the main button
  added       "YYYY-MM" the entry was added
*/
window.PORTFOLIO = [
  {
    id: "secret-shop",
    type: "app",
    name: "Secret Shop",
    tagline:
      "Mystery-shops how fast an elective or specialty practice responds to a new patient inquiry, then scores it and writes the report.",
    problem:
      "Practices believed they followed up fast. Secret Shop measures it: a real-looking web inquiry, a dedicated tracking number, and five days of every call and text logged.",
    highlights: [
      "Seven-step shop workflow: enter a practice, spin up a local tracking number, submit the inquiry, track for five days",
      "Deterministic 100-point rubric: 70 points for speed to first response, 30 for texting back",
      "One-page web and PDF report for slow responders, generated from the same data model so they never disagree",
      "Signed call, SMS and voicemail webhooks with retry de-duplication and a full audit log",
      "Two AI tools: built the production app with ChatGPT Codex (28 feature branches, merged by pull request), then used Claude Code to turn it into this read-only public demo",
    ],
    stack: ["ChatGPT Codex", "Claude Code", "TypeScript", "Express", "Twilio", "Postgres", "PDFKit"],
    stats: [
      { value: "13", label: "Practices shopped (demo)" },
      { value: "70 / 30", label: "Speed / text rubric" },
      { value: "5 days", label: "Tracking window" },
    ],
    links: [
      { label: "Open the demo", url: "https://boost-secret-shop.vercel.app/", primary: true },
      { label: "Sample report", url: "https://boost-secret-shop.vercel.app/bramblewood-dental-r1002" },
      { label: "Sample PDF", url: "https://boost-secret-shop.vercel.app/bramblewood-dental-r1002.pdf" },
    ],
    added: "2026-10",
  },
  {
    id: "boost-flow",
    type: "app",
    name: "BoostFlow",
    tagline:
      "A live call guide for patient concierges: each practice's call policy, turned into a step-by-step flow they follow while on the phone.",
    problem:
      "Every practice had its own policies buried in long documents. Concierges needed the right script, rule and link in the moment, not after the call.",
    highlights: [
      "Six-stage call flow: greet, triage, qualify, educate, schedule, close",
      "Emergency protocol that surfaces on its own, with an ordered escalation list and urgent transfer form",
      "Appointment-type reference (costs, validations, treatments) plus scheduler, callback and transfer shortcuts",
      "One app, many practices: each clinic's policy loads from its own config, with a dated change log",
    ],
    stack: ["Vibe coded with Claude", "HTML / JS", "Netlify"],
    stats: [
      { value: "6", label: "Call stages" },
      { value: "1 app", label: "Per-practice configs" },
    ],
    links: [
      {
        label: "Example: Dell Laser Consultants",
        url: "https://sensational-tarsier-0fed51.netlify.app/index.html?clinic=dell-laser-consultants",
        primary: true,
      },
      {
        label: "Example: Still Waters",
        url: "https://sensational-tarsier-0fed51.netlify.app/index.html?clinic=still-waters",
        primary: true,
      },
    ],
    added: "2026-10",
  },
  {
    id: "jonah-voice",
    type: "skill",
    name: "Jonah's voice",
    tagline:
      "A Claude Skill for drafting and editing anything I send, post or publish as myself, so it sounds like me: plainspoken, direct and short.",
    problem:
      "Claude's default drafts don't sound like any particular person. Anything going out under my name has to sound like me, without a rewrite every time.",
    highlights: [
      "Five hard rules on every draft: no em dashes, no stock \"not X, but Y\" reversals, invent nothing, no inflation, keep my words when editing",
      "Separate guidance for emails and texts, articles and posts, reports, scripts, and personal notes",
      "Before-and-after examples that show the edit to make, like \"leverage\" becoming \"use\"",
      "A checklist Claude runs before handing over any draft, including a search for em dashes",
    ],
    stack: ["Claude Skill", "SKILL.md"],
    stats: [
      { value: "5", label: "Hard rules" },
      { value: "5", label: "Formats covered" },
      { value: "7", label: "Pre-handoff checks" },
    ],
    links: [
      {
        label: "Read the SKILL.md",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/jonah-voice/SKILL.md",
        primary: true,
      },
    ],
    added: "2026-10",
  },
];
