# Jonah's AI Portfolio

One static page listing the apps, Claude skills and dashboards Jonah built. Hosted on Vercel.

- Live: https://jonah-ai-portfolio.vercel.app
- Vercel project: `jonah-ai-portfolio` (team `team_idk0RyREc1P6alnKmJypGzVa`)
- Source: `site/` (`index.html`, `projects.js`, `jonah.jpg`). No build step.

## "Add X to the portfolio"

1. Add one object to `window.PORTFOLIO` in `site/projects.js`. Do not edit `index.html` for content. The field list and allowed values are in the comment at the top of `projects.js`.
   - Tiles are app-store style and must stay short: a ~15-word `tagline`, up to 2 `stats`, and the detail (`why`, up to 3 `points`, `tech`) folds under "How it works".
   - Pick an `icon` and `tone` that differ from the neighboring tiles.
   - Exactly one link is `primary: true` (the tile's button). Other links show under "How it works". For a skill, copy its files to `skills/<name>/` and link the SKILL.md on GitHub.
2. Get the facts from the thing itself (its repo, README, live URL), not from guesses. Ask Jonah for anything missing (links, numbers).
3. Voice follows the Boost Patients design system: concrete, plain verbs, short sentences, sentence case, numbers with their source.
4. Check it renders (desktop + 390px mobile), then redeploy the `site/` files to the Vercel project with `target: "production"`, and commit to this repo.

## Design

Boost Patients design system (Barlow; brand blue `#2a5caa`; ink `#17223b`; navy `#0b1633` for the stats panel and closing band). Tokens live as CSS variables at the top of `index.html`.
