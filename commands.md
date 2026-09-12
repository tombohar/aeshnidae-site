# Aeshnidae commands

Everything the custom mods add. ACE's own commands are not listed — `/help` covers those.

Access level in brackets. Admin characters meet every level.

---

## Instanced dungeons — `/noinst` [Admin]

A dungeon that hands out private copies. The copy keeps the **source landblock id**, so
the client renders it from the dat it already has — nothing is shipped to anyone.

### Making a dungeon instanced

```
/noinst instance 008D personal        flag it: everyone entering gets their own copy
/noinst instance 008D fellowship      one copy per party, so groups stay together
/noinst instance 008D allegiance      one copy per allegiance, shared by all members
/noinst instance 008D                 unflag it
/noinst instance                      what is flagged, and how many copies are open
```

Once flagged, **every** route in works — a portal, a recall, an admin teleport, a login.
There is nothing to attach to the portal, and no new weenie: the hook is on entry.

### Looking and testing

```
/noinst                  where you are, every open copy, its players and object count
/noinst count drudge     how many of a thing the master and each copy really hold
/noinst enter 1          manually put yourself in copy 1 of the dungeon you are standing in
/noinst leave            back to the server's own version
/noinst close            drop every copy — anyone inside is recalled to their lifestone
```

`/noinst count` exists because "is that thing really in this copy, or is my client just
still showing it to me" is the question that comes up every time something looks wrong,
and object counts in the log are not an answer.

Rebuilding the mod reloads it, which drops every copy — but players are left standing
where they are and put back into a fresh copy on the next tick, rather than recalled.
Admins are left in the master on purpose, so authoring survives a rebuild.

`/noinst enter` is for testing. It does **not** flag the dungeon, so it will not survive a
relog — that is what `/noinst instance` is for.

### When something looks wrong

```
/noinst count drudge     what the master and each copy really hold, with physics cells
/noinst resync           clear a phantom player somebody can still see
/instance                which copy you are in [Player]
```

`/noinst count` reports, per object, which landblock's cells it is physically in against
which one lists it. Those are separate facts, and only the first decides what anyone can
see — a disagreement between them is invisible from every other angle.

The server also audits this itself every 15 seconds and repairs what it finds, logging
under `AUDIT`. Turn it off with `LogRouting` in Settings.json.

### Watching a player who is in their own copy

```
/noinst goto <player>    join whichever copy they are actually in
/teleto <player>         the same — patched to follow players into copies
/teletome <player>       bring them to you — patched to land them in your copy
```

Plain `/teleto` used to land you in a private copy of the same rooms, alone, because a
position cannot tell two copies apart. It now follows the player.

### Where am I? — `/instance` [Player]

```
/instance                which copy of a dungeon you are in, and who shares it
/noinst help             every command this mod adds, admin and player
```

`/instance` is player-level on purpose: "we can see each other" and "we can't see each
other" are both reported as bugs, and without this neither reporter can say which
landblock they are standing in.

### Authoring — the master copy

There is exactly **one** authored version of a dungeon: the world database rows for that
landblock id. Every copy spawns from those rows. That authored version is the *master*.

**Order matters.** `/createinst` spawns into whichever landblock you are standing in, so
go to the master *before* creating anything:

```
/noinst master                        FIRST — the only version that is authored
/createinst <wcid or classname>       place a permanent object at your feet (ACE, Developer)
/removeinst                           remove the last object you appraised
/noinst reload                        push the master into every open copy
```

Author inside a copy and the object is somewhere only that copy can see, until the copy
closes and it is gone. The routing log says which landblock a spawn actually landed in —
`LogRouting` in Settings.json, on by default.

`/noinst master` matters because an admin walking into an instanced dungeon is handed a
private copy like anyone else — edits made there would look right and reach nobody.

`/noinst reload` is the push, and it is needed after **removing** something as well as
after adding it. `/removeinst` deletes the authored row and the object in front of you;
copies that are already open keep the creatures they spawned with until they are reloaded
or they close. An extra monster in someone's copy after you deleted it is that, not a
duplication bug — `/noinst count <name>` will show you which copies still hold it.

ACE's own `/reload-landblock` only touches the single landblock you are standing in,
which for an instanced dungeon is one copy out of however many are open.

One authored version per landblock id — there is no way to keep the original and a
modified variant of the same dungeon live at the same time.

### Known gaps, in the order worth doing

- **Fellowship and allegiance scope are untested.** Every test so far has been
  `Personal`. Groups staying together is the point of the feature.
- **Capacity fallback.** At `MaxCopiesPerLandblock` a player is told the dungeon is full
  and left in the shared master. For a dungeon with no public version that is never the
  right answer — it should refuse entry.
- **No access control**, and no way to invite someone into your copy except by sharing a
  fellowship or allegiance.
- **Assignments live in memory only.** A restart or a mod reload loses which copy a group
  had. Low impact: copy *contents* never persist either, so a restored assignment would
  hand out a freshly spawned copy — the same thing a new one gives. The group key is
  computed live, so fellowship cohesion does not depend on this.
- **Rebuilding the mod reloads it**, which closes every copy and re-places the players
  inside — they get teleported. Expected during development, not during a play session.

---

## Skills — `/x`, `/raise`, `/check` [Player]

```
/x <skill>                      what the next +1, +5, +10 cost, and how many points you can afford
/cost <skill>                   the same
/raise <skill> [n]              buy n mastery points
/mastery                        every skill you hold mastery in
/check <skill>                  what a skill actually works out to, and where each part comes from
```

Skill names with spaces work as-is: `/x melee defense`. (`/c` and `/m` are chat channels in the client, so it never sends them to the server.)

`/check` shows attributes, retail ranks, mastery, augmentations, buffs, and then the
combat layer — weapon, burden, stance, armour imbues — with the effective figure taken
from ACE's own calculation rather than recomputed.

Mastery is paid for in **Radiance** from the account bank, priced along the retail
skill curve continued: the first mastery point costs what rank 209 would have, and each
point after is 1.0787x the one before (the retail table's own tail multiplier). One
mastery rank is one skill point. Roughly: +30 in a skill totals ~34B Radiance, +50 ~168B
(about one whole climb to level 275), so the curve is its own ceiling.

Mastery survives enlightenment. Retail ranks do not.

---

## Experience — retired

`/xp` and `/xpsend` are gone. Experience is not a currency on Aeshnidae and cannot be
sent between characters; `Aeshnidae.XpCurrency` was disabled on 2026-09-12. The
currencies are Radiance and Resonance - see Banking.

---

## Fellowships — `/fellow` [Player]

```
/fellow                         the share curve, with your fellowship's row marked
/fellow reload                  re-read settings without a restart [Admin]
```

---

## Banking — `/bank`, `/b`, `/earned` [Player]

```
/b                              balances - Radiance, Resonance, pyreals, luminance, keys
/b d                            deposit EVERYTHING: all pyreals, luminance and keys
/b d <item> [n]                 deposit one thing; no amount means all of it
/b w <item> [n]                 withdraw; no amount means all of it
/b pay <player> <cur> <n>       send Radiance or Resonance to another account (2% fee, 100,000 min)
/bank autolum on|off            earned luminance goes straight to the bank, past your cap
/earned                         Radiance, Resonance and luminance over 5/10/30/60 min, session, per hour
/earned reset                   start the session clock over
/bank help                      full syntax
/bankreload                     re-read settings [Admin]
```

Shared by every character on the account. Every verb has a long form too (`/bank
deposit`, `withdraw`, `pay`) - the short ones are just the ones worth remembering.

Radiance is experience's mirror: one Radiance per point of experience received, from
kills, quests and fellowship shares, and it keeps accruing at the level cap. It is what
skill mastery costs. Resonance is 10 per quest completion. Both are earned straight into
the balance and never carried; they cannot be deposited or withdrawn, only spent and sent.

---

## Developer content — `/wexport` [Developer]

For developers with no way onto the server. Renders a weenie to SQL exactly as
`/export-sql` does and posts it to the `#content` Discord channel as a file.

```
/wexport 22642                          by wcid
/wexport ace22642-brighteyesthetailor   by class name
```

The first export after a start is slower - ACE's writer loads every weenie and spell
name to annotate the output. There is deliberately no `/wimport`: changes go back
through the ledger in `Content\sql\changes\` so every edit is recorded, snapshotted
and reversible. See the README there.

```
/contenttools                   status, webhook shown masked [Admin]
/contenttools-reload            re-read settings [Admin]
```

---

## Staff — `/grant` [Admin]

```
/grant radiance 5000000 Dargoth Hera    add Radiance to that character's account
/grant resonance 100                    yourself, in game
/grant radiance -5m Dargoth Hera        take it away; refuses to go below zero
```

For testing. Writes the account balance directly - no earning buffer, no `/earned`
history, no fee. Works from the console (`ace-cmd.sh 'grant radiance 1 Dargoth Hera'`)
with a player named. Character names can be two words; the name is everything after the
amount.

---

## Staff — `/adminaudit`, `/fairplay`, `/discordrelay` [Admin]

```
/adminaudit                     audit trail status; one line per Discord webhook
/adminaudit hooks               which cross-mod hooks are bound
/adminaudit tail [n]            last n entries
/adminaudit find <text> [n]     search
/adminaudit rebind              re-attach the cross-mod hooks
/fairplay                       fair-play status
/fairplay shared                addresses used by several accounts
/fairplay linked                household clusters
/fairplay account <name>        one account's history
/fairplay ip <address>          one address's history
/discordrelay                   chat relay status
/discordrelay-test <channel>    post a test line, e.g. /discordrelay-test Trade
```

Each has a `-reload` that re-reads its `Settings.json` without a restart.

---

## Movement validation — `/moveguard` [Admin]

Rejects client positions that outrun the player's real speed, and reports positions
the physics engine could not reach. Closes the gap Blink-style plugins use: stock ACE
only speed-checks moves that cross more than a whole landblock, and forces a
requested position even when its own collision check stopped short of it.

```
/moveguard                      status, thresholds, counters
/moveguard mode log             measure and report, reject nothing  (default)
/moveguard mode enforce         reject and snap the client back
/moveguard mode off
/moveguard check <name>         one player's computed top speed, strikes, latest violation
/moveguard me                   the same for yourself
/moveguard top                  everyone online with a strike, worst first
/moveguard reload               re-read Settings.json
```

Start in `log` and read the audit channel for a few days before `enforce`. Geometry
violations stay log-only even in `enforce` until `EnforceGeometry` is set in
Settings.json - see the mod's Readme for why, and for the rollout order.

---

## The rest

```
/maxlevel [level]               the level cap and what levels cost [Player]
/qb                             your quest bonus [Player]
/qbreload                       re-read quest bonus settings [Admin]
/datbackup                      snapshot the server's dats [Admin]
/datbackup-reload               re-read settings [Admin]
```

---

## Settings

Not a game command — run it from `C:\ACEPublic\Mods`:

```bash
python settings.py                    every setting, from all four places they live
python settings.py xp                 only lines matching "xp"
python settings.py --set Aeshnidae.InstancesNoDat EmptyGraceSeconds 900
python settings.py --set-db xp_modifier 0.75
```

Mod settings need a restart (or that mod's reload command). Shard database properties go
live within five minutes on their own.

---

## Not loaded

`Aeshnidae.Instances` (the dat-patching version) and `Aeshnidae.AllowNewerDats` live in
`Mods\_disabled\` and cannot load. `Aeshnidae.Instances` provided `/instance`; do not
confuse it with `/noinst instance`, which belongs to the current mod.

There is also a `Aeshnidae.DiscordRelay` in `Mods\src\` that is not deployed.
