# Jonah's AI Portfolio

One static page listing the apps, Claude skills and dashboards Jonah built. Hosted on Vercel.

- Live: https://jonah-ai-portfolio.vercel.app
- Vercel project: `jonah-ai-portfolio` (team `team_idk0RyREc1P6alnKmJypGzVa`)
- Source: `site/` (`index.html`, `projects.js`, `jonah.jpg`). No build step.

## "Add X to the portfolio"

1. Add one object to `window.PORTFOLIO` in `site/projects.js`. Do not edit `index.html` for content.
   - `type`: `"app"`, `"skill"` or `"dashboard"` (the page groups and counts by type automatically)
   - `id`, `name`, `tagline`, `problem`, 3–5 `highlights`, `stack`, up to 3 `stats`, `links`, `added: "YYYY-MM"`
   - Mark the main link(s) `primary: true`. For a skill with no live demo, link the SKILL.md on GitHub.
2. Get the facts from the thing itself (its repo, README, live URL), not from guesses. Ask Jonah for anything missing (links, numbers).
3. Voice follows the Boost Patients design system: concrete, plain verbs, short sentences, sentence case, numbers with their source.
4. Check it renders (desktop + 390px mobile), then redeploy the `site/` files to the Vercel project with `target: "production"`, and commit to this repo.

## Design

Boost Patients design system (Barlow; brand blue `#2a5caa`; ink `#17223b`; navy `#0b1633` for the stats panel and closing band). Tokens live as CSS variables at the top of `index.html`.
