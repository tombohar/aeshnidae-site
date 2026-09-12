# Aeshnidae — the website

The player-facing site for Aeshnidae, a private Asheron's Call server. Static pages,
served by GitHub Pages from this repo's `main` branch. Edit, commit, push — live within
a minute.

| | |
| --- | --- |
| `index.html` | The front page: how to join, what's different (one card per always-on feature), house rules, help. |
| `changes.html` | **Changes to Dereth** — every world change, newest first, dated, with the reason. Grows with each change. |
| `site.css` | The one stylesheet both pages share. |

## Adding a change

Every world-database change gets an entry in `changes.html`, added at the **top** of
`<div class="rules changes">`, the same day it goes live:

```html
<div class="rule">
  <p class="eyebrow">11 September 2026</p>
  <h3>What changed, as a headline</h3>
  <p>What it means for a player, and why. Name the NPCs and items. Say what was
     deliberately left alone if a player might wonder.</p>
</div>
```

Player-facing wording lives beside the change in the main repo as a `.patchnote.md`
(`Mods\Content\sql\changes\`) — reuse it, shortened. The Discord post, the patch note file
and this page should agree.

## Adding a feature

A new always-on feature (a mod that players interact with) gets a card in the
`<div class="features">` grid on `index.html` — heading, one paragraph, and its commands
in a `.cmds` block. The grid is three across; a lone last card stretches to fill its row.
