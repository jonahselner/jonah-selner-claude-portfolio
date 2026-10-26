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
  note        optional small line under the stats (e.g. "The demo uses sample data.")
  added       "YYYY-MM" the entry was added
*/
window.PORTFOLIO = [
  {
    id: "secret-shop",
    type: "app",
    name: "Secret Shop",
    tagline:
      "Mystery-shops a practice's website form, then times how long it takes them to call or text back. It scores the response and writes the report.",
    problem:
      "A slow call back can lose the patient. Secret Shop shows a practice exactly how long theirs took, with a timestamp on every call and text.",
    highlights: [
      "Enter a practice, get a local tracking number, submit the inquiry, then log every response for five days",
      "Scored out of 100: 70 points for how fast they respond, 30 for whether they text back",
      "Slow responders get a one-page report and PDF, built from the same data so the two always match",
      "Signed call, SMS and voicemail webhooks, with duplicate retries ignored and every event in an audit log",
      "I built the production app with ChatGPT Codex (28 feature branches, merged by pull request), then used Claude Code to turn it into this read-only demo",
    ],
    stack: ["ChatGPT Codex", "Claude Code", "TypeScript", "Express", "Twilio", "Postgres", "PDFKit"],
    stats: [
      { value: "13", label: "Practices shopped (demo)" },
      { value: "70 / 30", label: "Speed / text rubric" },
      { value: "5 days", label: "Tracking window" },
    ],
    note: "The demo uses sample data.",
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
      "A call guide for patient concierges. It turns each practice's call policy into steps they follow while they're on the phone.",
    problem:
      "Each practice has its own call rules. Concierges need the right script and link while the patient is still on the line.",
    highlights: [
      "Six call stages: greet, triage, qualify, educate, schedule and close",
      "An emergency protocol with who to call, in order, and an urgent transfer form",
      "Reference tabs for costs, validations and treatments, plus shortcuts to schedule, call back or transfer",
      "One app for every practice. Each clinic's policy loads from its own config and keeps a dated change log",
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
    id: "concierge-candidate-screening",
    type: "skill",
    name: "Concierge candidate screening",
    tagline:
      "Drop in a batch of resumes, recruiter transcripts and interview videos. Claude calls each candidate GREEN, YELLOW or RED and writes a one-page summary for the recruiter plus a one-page review per person.",
    problem:
      "We hire bilingual patient concierges in Latin America through an outside recruiter. Every interview slot spent on a weak fit is wasted, and a thin resume or a shallow recruiter screen can hide a great candidate.",
    highlights: [
      "Scores each candidate on 10 criteria with clear non-negotiables. Every YELLOW comes with one specific check and what each answer means: \"confirms a weekend shift → GREEN, weekdays only → RED\"",
      "Handles the recruiter videos so nobody has to watch them: pulls frames to check the interview setup and measures pitch and volume variation in the candidate's answers as a read on energy",
      "Says plainly what it can't judge. Accent can't be heard from files, so it reads the transcript for comprehension problems and leaves the rest to the live interview",
      "Catches the misses people make in both directions, like a recruiter screening for the wrong role, or a Colombian candidate who doesn't list Spanish because it's obvious",
      "Ignores age, sex, family status and appearance, even when a resume lists them",
    ],
    stack: ["Claude Skill", "SKILL.md", "Python", "ffmpeg", "python-docx", "skill-creator evals"],
    stats: [
      { value: "10", label: "Rubric criteria" },
      { value: "18 / 18", label: "Test checks passed" },
      { value: "1 page", label: "Per document" },
    ],
    note: "Tested on 3 synthetic batches. The same prompts without the skill passed 39% of the checks.",
    links: [
      {
        label: "Read the SKILL.md",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/concierge-candidate-screening/SKILL.md",
        primary: true,
      },
      {
        label: "Sample summary (PDF)",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/concierge-candidate-screening/samples/Sample_Executive_Summary.pdf",
      },
      {
        label: "Sample review (PDF)",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/concierge-candidate-screening/samples/Sample_Candidate_Review_YELLOW.pdf",
      },
      {
        label: "Test cases",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/tree/main/skills/concierge-candidate-screening/evals",
      },
    ],
    added: "2026-10",
  },
  {
    id: "aesthetics-consult-router",
    type: "skill",
    name: "Aesthetic consult booking",
    tagline:
      "A call-center agent types a few words about what a med spa lead wants. Claude returns one booking instruction: which consult, the fee, and a line the agent can say.",
    problem:
      "Agents on a live call aren't clinicians, and the lead is waiting. They need to know whether \"Morpheus8\" or \"my neck looks tired\" is a Visia consult or a filler consult without putting anyone on hold.",
    highlights: [
      "Maps brands, treatments, body areas and plain-language worries to one of seven consults, with the fee",
      "Always one answer. When it's a true toss-up, it gives the agent one question to ask and what to book for each answer",
      "Safety comes first: a possible complication after filler goes straight to clinical staff, and stroke or vision symptoms get a 911 instruction",
      "Handles the edge cases agents get wrong, like a lip flip (neurotoxin, not filler) and PicoSure for a tattoo vs. dark spots",
      "Waxing, facials and massage skip the consult and transfer straight to scheduling. Medical concerns outside aesthetics get pointed to the right doctor",
    ],
    stack: ["Claude Skill", "SKILL.md", "Reference catalog"],
    stats: [
      { value: "7", label: "Consult types" },
      { value: "250+", label: "Example lead phrasings" },
      { value: "4", label: "Safety escalations" },
    ],
    links: [
      {
        label: "Read the SKILL.md",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/aesthetics-consult-router/SKILL.md",
        primary: true,
      },
      {
        label: "Service catalog",
        url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/aesthetics-consult-router/references/catalog.md",
      },
    ],
    added: "2026-10",
  },
  {
    id: "jonah-voice",
    type: "skill",
    name: "Jonah's voice",
    tagline:
      "Teaches Claude to write like me when it drafts or edits anything I send, post or publish: plainspoken, direct and short.",
    problem:
      "Claude's default drafts don't sound like anyone in particular. Anything going out under my name should sound like me without a rewrite.",
    highlights: [
      "Five hard rules on every draft: no em dashes, no stock \"not X, but Y\" reversals, invent nothing, no inflation, keep my words when editing",
      "Separate guidance for emails and texts, articles and posts, reports, scripts, and personal notes",
      "Before-and-after examples that show the edit to make, like \"leverage\" becoming \"use\"",
      "A checklist Claude runs before it hands over any draft, including a search for em dashes",
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
