/*
  Portfolio entries. This is the ONLY file that changes when something is added.
  Keep every field short: someone hiring should get each tile in five seconds.

  id         unique kebab-case slug (the tile's #anchor)
  type       "app" | "skill" | "dashboard"
  name       display name
  icon       "timer" | "phone" | "pen" | "split" | "star" | "users" | "chart" | "mail" | "spark"
  tone       icon tile color: "blue" | "navy" | "deep" | "orange"
  subtitle   4 to 8 plain words under the name: what it is, for someone who has never seen it
  tagline    one sentence, about 15 to 20 words: what it does
  builtWith  AI tools, shown under "How it works", e.g. ["Claude Code"], ["ChatGPT Codex", "Claude Code"], ["Claude Skill", "Evals"]
  stats      up to 2 { value, label } proof points
  why        one or two sentences, shown under "How it works"
  points     up to 3 short bullets, shown under "How it works"
  tech       optional small tech labels, shown under "How it works"
  note       optional footnote, e.g. "The demo uses sample data."
  links      [{ label, url, primary? }]; the primary link is the tile's main button
  added      "YYYY-MM"
*/
window.PORTFOLIO = [
  {
    id: "secret-shop",
    type: "app",
    name: "Speed-to-lead secret shopper",
    icon: "timer",
    tone: "blue",
    tagline: "Fills out a practice's web form as a new patient, then logs every call and text for five days and scores the response.",
    subtitle: "Times how fast practices call leads back",
    builtWith: ["ChatGPT Codex", "Claude Code"],
    stats: [
      { value: "13", label: "practices shopped" },
      { value: "5 days", label: "of call tracking" },
    ],
    why: "A slow call back can lose the patient. This shows a practice exactly how long theirs took.",
    points: [
      "Spins up a local tracking number and logs every call and text for five days",
      "Scores out of 100 (70 for speed, 30 for texting back), then writes a one-page report and PDF",
      "I built the production app with ChatGPT Codex (28 feature branches), then used Claude Code to make this public demo",
    ],
    tech: ["TypeScript", "Express", "Twilio", "Postgres", "PDFKit"],
    note: "The demo uses sample data.",
    links: [
      { label: "Open demo", url: "https://boost-secret-shop.vercel.app/", primary: true },
      { label: "Sample report", url: "https://boost-secret-shop.vercel.app/bramblewood-dental-r1002" },
    ],
    added: "2026-10",
  },
  {
    id: "boost-flow",
    type: "app",
    name: "Live call guide",
    icon: "phone",
    tone: "navy",
    tagline: "Turned 60+ call policies, each formatted differently, into one standard step-by-step guide for every call.",
    subtitle: "One standard format for every call policy",
    builtWith: ["Claude (vibe coded)"],
    stats: [
      { value: "60+", label: "call policies standardized" },
      { value: "6", label: "call stages, every practice" },
    ],
    why: "Our call policies lived in 60+ Google Docs, hundreds of pages, each formatted differently with different headings. Nobody could open a new one and know where to look.",
    points: [
      "A CMS backend behind Google sign-in, open only to Boost email addresses, with uploads limited to staff who had permission",
      "An AI skill reads any uploaded call policy and rewrites it into the BoostFlow format, so every practice's guide looks the same",
      "Concierges follow the same six stages on every call, from greeting to booking, with an emergency protocol built in",
    ],
    tech: ["CMS backend", "Google sign-in", "Role permissions", "AI import skill"],
    note: "The demo shows the concierge view. The CMS and import skill aren't in the demo.",
    links: [
      { label: "Open demo", url: "https://sensational-tarsier-0fed51.netlify.app/index.html?clinic=dell-laser-consultants", primary: true },
      { label: "Second practice", url: "https://sensational-tarsier-0fed51.netlify.app/index.html?clinic=still-waters" },
    ],
    added: "2026-10",
  },
  {
    id: "concierge-candidate-screening",
    type: "skill",
    name: "Candidate screener",
    icon: "users",
    tone: "deep",
    tagline: "Reads resumes, recruiter transcripts and interview videos, then writes a one-page review of each candidate.",
    subtitle: "Rates job applicants green, yellow or red",
    builtWith: ["Claude Skill", "Tested with evals"],
    stats: [
      { value: "18 / 18", label: "test checks passed" },
      { value: "39%", label: "same tests, no skill" },
    ],
    why: "We hire bilingual patient concierges through an outside recruiter. Every interview slot spent on a weak fit is wasted.",
    points: [
      "Scores 10 criteria. Every YELLOW comes with one specific question and what each answer means",
      "Checks the interview videos so nobody has to watch them: setup from frames, energy from pitch and volume",
      "Ignores age, sex, family status and appearance, even when a resume lists them",
    ],
    tech: ["Python", "ffmpeg", "python-docx", "skill-creator evals"],
    note: "Tested on 3 synthetic batches.",
    links: [
      { label: "View skill", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/concierge-candidate-screening/SKILL.md", primary: true },
      { label: "Sample summary", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/concierge-candidate-screening/samples/Sample_Executive_Summary.pdf" },
    ],
    added: "2026-10",
  },
  {
    id: "a-plus-call-check",
    type: "skill",
    name: "Client-ready call check",
    icon: "star",
    tone: "orange",
    tagline: "Scores a call someone flagged as great. If it's truly A+, Claude drafts the note to send the practice.",
    subtitle: "Checks a great call before the client hears it",
    builtWith: ["Claude Skill", "Tested with evals"],
    stats: [
      { value: "6", label: "scored sections" },
      { value: "2 / 2", label: "test verdicts correct" },
    ],
    why: "We sent standout calls to practices to build their confidence. That only works if every call we send is excellent.",
    points: [
      "Needs 90+ out of 100, no section under 80%, and none of 7 critical flags",
      "Rereads the call as the client would and blocks anything awkward, like a promise of results",
      "Writes a 3 to 5 sentence client note with no scores or QA language",
    ],
    tech: ["skill-creator evals"],
    note: "Tested on 2 synthetic calls.",
    links: [
      { label: "View skill", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/a-plus-call-check/SKILL.md", primary: true },
      { label: "Sample verdict", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/a-plus-call-check/samples/Sample_Verdict.md" },
    ],
    added: "2026-10",
  },
  {
    id: "aesthetics-consult-router",
    type: "skill",
    name: "Med spa consult router",
    icon: "split",
    tone: "blue",
    tagline: "An agent types what the caller wants, like \"Botox\" or \"my neck looks tired.\" Claude returns the consult and the fee.",
    subtitle: "Tells call agents which consult to book",
    builtWith: ["Claude Skill"],
    stats: [
      { value: "7", label: "consult types" },
      { value: "250+", label: "example lead phrasings" },
    ],
    why: "Agents on a live call aren't clinicians, and the lead is waiting. They need one answer without putting anyone on hold.",
    points: [
      "Maps brands, body areas and plain worries (\"my neck looks tired\") to one consult and its fee",
      "Safety first: a possible complication goes to clinical staff, stroke or vision symptoms get a 911 instruction",
      "Handles the edge cases agents get wrong, like a lip flip (neurotoxin, not filler)",
    ],
    tech: ["SKILL.md", "Reference catalog"],
    links: [
      { label: "View skill", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/aesthetics-consult-router/SKILL.md", primary: true },
      { label: "Service catalog", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/aesthetics-consult-router/references/catalog.md" },
    ],
    added: "2026-10",
  },
  {
    id: "jonah-voice",
    type: "skill",
    name: "My writing voice",
    icon: "pen",
    tone: "navy",
    tagline: "Rules and examples Claude follows when it drafts or edits anything I send or publish.",
    subtitle: "Makes Claude's drafts sound like me",
    builtWith: ["Claude Skill"],
    stats: [
      { value: "5", label: "hard rules" },
      { value: "7", label: "pre-handoff checks" },
    ],
    why: "Claude's default drafts don't sound like anyone in particular. Anything going out under my name should sound like me without a rewrite.",
    points: [
      "Hard rules on every draft: no em dashes, invent nothing, no inflation, keep my words when editing",
      "Separate guidance for emails, posts, reports, scripts and personal notes",
      "A checklist Claude runs before it hands over any draft",
    ],
    tech: ["SKILL.md"],
    links: [
      { label: "View skill", url: "https://github.com/jonahselner/jonah-selner-claude-portfolio/blob/main/skills/jonah-voice/SKILL.md", primary: true },
    ],
    added: "2026-10",
  },
];
