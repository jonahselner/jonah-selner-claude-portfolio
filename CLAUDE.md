# Jonah's AI Portfolio

One static page listing the apps, Claude skills and dashboards Jonah built. Hosted on Vercel.

- Live: https://jonah-ai-portfolio.vercel.app
- Vercel project: `jonah-ai-portfolio` (team `team_idk0RyREc1P6alnKmJypGzVa`)
- Source: `site/` (`index.html`, `projects.js`, `jonah.jpg`). No build step.

## "Add X to the portfolio"

1. Add one object to `window.PORTFOLIO` in `site/projects.js`. Client-facing work uses `type: "feature"` (a wide card above Apps, linking to its own case-study page in `site/`). Do not edit `index.html` for content. The field list and allowed values are in the comment at the top of `projects.js`.
   - Tiles are app-store style and must stay short: a ~15-word `tagline`, up to 2 `stats`, and the detail (`why`, up to 3 `points`, `tech`) folds under "How it works".
   - The page has two tiers. Entries with `featured` (1, 2, 3...) show as Audit → Optimize → Automate case studies: a big before → after, 2 to 4 words per step, a human-in-the-loop line and a proof line (see the field notes in `projects.js`). Everything else shows as a one-line row under "More builds". New items go in "More builds" unless Jonah says to feature them.
   - Every entry gets a `goal`: "money", "time" or "quality". Jonah maps every AI use case to one business outcome. Ask him if it isn't clear.
   - Pick an `icon` and `tone` that differ from the neighboring tiles.
   - Exactly one link is `primary: true` (the card's only button). Other links are kept in the data but not shown on the main page. For a skill, copy its files to `skills/<name>/` and link the SKILL.md on GitHub.
2. Get the facts from the thing itself (its repo, README, live URL), not from guesses. Ask Jonah for anything missing (links, numbers).
3. Voice: concrete, plain verbs, short sentences, sentence case, numbers with their source.
4. Check it renders (desktop + 390px mobile), then redeploy the `site/` files to the Vercel project with `target: "production"`, and commit to this repo.

## Design

Styled to match blankmetal.ai for the Blank Metal interview: dark ink `#231f20`, Anton uppercase headlines, DM Sans body, JetBrains Mono labels, coral→pink→purple gradient. Tokens are CSS variables at the top of `index.html`. Keep tile text to words and short phrases, not sentences.
