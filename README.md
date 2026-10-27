# I've seen it all — 20 free video effects for Claude

Drop your clip into Claude, say the effect and the seconds. That's the whole edit. Works on Mac and Windows.

By **Raed Ouerfelli**.

> Want Claude to do the whole edit from your raw video? **[Join the Creator Studio waitlist](https://learn.ouerfelli-raed.com/en/waitlist/ai-video-editing?src=github)**

## The 20 effects
<table>
<tr><td align="center" width="25%"><img src="gallery/free/glass-widgets.gif" width="180" alt="glass-widgets"><br><code>glass-widgets</code><br><sub>frosted glass widgets around your head</sub></td><td align="center" width="25%"><img src="gallery/free/orbit.gif" width="180" alt="orbit"><br><code>orbit</code><br><sub>your reels circle your head</sub></td><td align="center" width="25%"><img src="gallery/free/spotlight.gif" width="180" alt="spotlight"><br><code>spotlight</code><br><sub>lights drop, glowing word behind you</sub></td><td align="center" width="25%"><img src="gallery/free/glitter-spotlight.gif" width="180" alt="glitter-spotlight"><br><code>glitter-spotlight</code><br><sub>spotlight look: gold rays, gold word, sparkles</sub></td></tr>
<tr><td align="center" width="25%"><img src="gallery/free/checklist.gif" width="180" alt="checklist"><br><code>checklist</code><br><sub>Claude task list ticks green</sub></td><td align="center" width="25%"><img src="gallery/free/liquid-glass-graph.gif" width="180" alt="liquid-glass-graph"><br><code>liquid-glass-graph</code><br><sub>glass card, graph climbs</sub></td><td align="center" width="25%"><img src="gallery/free/liquid-glass-graph-bento.gif" width="180" alt="liquid-glass-graph-bento"><br><code>liquid-glass-graph (bento)</code><br><sub>liquid-glass-graph, bento look</sub></td><td align="center" width="25%"><img src="gallery/free/apple-toggles.gif" width="180" alt="apple-toggles"><br><code>apple-toggles</code><br><sub>iPhone switches flip on</sub></td></tr>
<tr><td align="center" width="25%"><img src="gallery/free/messages.gif" width="180" alt="messages"><br><code>messages</code><br><sub>iMessage notifications stack up</sub></td><td align="center" width="25%"><img src="gallery/free/led-sign.gif" width="180" alt="led-sign"><br><code>led-sign</code><br><sub>LED sign types itself behind you</sub></td><td align="center" width="25%"><img src="gallery/free/red-collage.gif" width="180" alt="red-collage"><br><code>red-collage</code><br><sub>B&W you, giant red word</sub></td><td align="center" width="25%"><img src="gallery/free/cover-star.gif" width="180" alt="cover-star"><br><code>cover-star</code><br><sub>you on a magazine cover</sub></td></tr>
<tr><td align="center" width="25%"><img src="gallery/free/cover-star-ed.gif" width="180" alt="cover-star-ed"><br><code>cover-star (editorial)</code><br><sub>cover-star, editorial look</sub></td><td align="center" width="25%"><img src="gallery/free/split-headline.gif" width="180" alt="split-headline"><br><code>split-headline</code><br><sub>headline card pushes you down</sub></td><td align="center" width="25%"><img src="gallery/free/backdrop-word.gif" width="180" alt="backdrop-word"><br><code>backdrop-word</code><br><sub>giant word behind you</sub></td><td align="center" width="25%"><img src="gallery/free/headline-wall.gif" width="180" alt="headline-wall"><br><code>headline-wall</code><br><sub>headlines pile up behind you</sub></td></tr>
<tr><td align="center" width="25%"><img src="gallery/free/match-cut.gif" width="180" alt="match-cut"><br><code>match-cut</code><br><sub>news pages cut on one word</sub></td><td align="center" width="25%"><img src="gallery/free/place-in-grid.gif" width="180" alt="place-in-grid"><br><code>place-in-grid</code><br><sub>you in your 3x3 profile grid</sub></td><td align="center" width="25%"><img src="gallery/free/paper-cut.gif" width="180" alt="paper-cut"><br><code>paper-cut</code><br><sub>torn-paper cut-out scrapbook</sub></td><td align="center" width="25%"><img src="gallery/free/palm-tags.gif" width="180" alt="palm-tags"><br><code>palm-tags</code><br><sub>labels ride on your hands</sub></td></tr>
<tr><td align="center" width="25%"><img src="gallery/free/wall-of-words.gif" width="180" alt="wall-of-words"><br><code>wall-of-words</code><br><sub>giant sliding words replace the room</sub></td><td align="center" width="25%"><img src="gallery/free/green-screen.gif" width="180" alt="green-screen"><br><code>green-screen</code><br><sub>an app replaces your room</sub></td><td align="center" width="25%"><img src="gallery/free/phone-mockup.gif" width="180" alt="phone-mockup"><br><code>phone-mockup</code><br><sub>iPhone beside you, a tap approves</sub></td></tr>
</table>

## Install
Paste this in a terminal (or ask Claude Code to do it for you):

```bash
git clone https://github.com/ouerf-man/Ive-seen-it-all ~/.claude/skills/studio-effects
```

On Windows (PowerShell) use `$HOME\.claude\skills\studio-effects` as the folder. Then restart Claude.

## Use it
Open Claude Code (the app or the terminal), drag your video in, then say **the effect name + the seconds**. Any of these work:

```
/studio-effects orbit from 3 to 6
add glass-widgets from 0 to 3
paper-cut from 8 to 11, with the letters "WOW"
orbit 3-6 and then spotlight 10-13 with the word CLAUDE
```

The effect names are the ones under each GIF above. Not sure which? Ask *"show me the effects"* and Claude opens the gallery.

The first time, Claude sets itself up (a few minutes: ffmpeg, Node, Python). Then it checks a few frames and renders `yourclip_effects.mp4` next to your clip, with your sound.

## Want the full editing studio?
This free pack adds one effect where you say. **Creator Studio** does the whole edit: **drop your raw video and Claude takes care of everything.**

- Enhances your voice, cuts the pauses and retakes
- Picks the moments from what you say and plans the edit
- Adds effects, captions (even in Tunisian derja) and sound effects
- You review, Claude refines, then renders the final video

It also unlocks these 9 effects and the "one clip → 7 edits" reel builder:

<table>
<tr><td align="center" width="33%"><img src="gallery/studio/documentary.gif" width="180" alt="documentary"><br><code>🔒 documentary</code><br><sub>archive film, B&W, red signal</sub></td><td align="center" width="33%"><img src="gallery/studio/render-studio.gif" width="180" alt="render-studio"><br><code>🔒 render-studio</code><br><sub>"Claude renders it" editing suite</sub></td><td align="center" width="33%"><img src="gallery/studio/shatter-on-clap.gif" width="180" alt="shatter-on-clap"><br><code>🔒 shatter-on-clap</code><br><sub>the frame shatters into glass</sub></td></tr>
<tr><td align="center" width="33%"><img src="gallery/studio/glass-type.gif" width="180" alt="glass-type"><br><code>🔒 glass-type</code><br><sub>3D glass letters behind you</sub></td><td align="center" width="33%"><img src="gallery/studio/frame-break.gif" width="180" alt="frame-break"><br><code>🔒 frame-break</code><br><sub>you burst out of a photo</sub></td><td align="center" width="33%"><img src="gallery/studio/vertigo.gif" width="180" alt="vertigo"><br><code>🔒 vertigo</code><br><sub>dolly zoom, the room rushes in</sub></td></tr>
<tr><td align="center" width="33%"><img src="gallery/studio/echo-hands.gif" width="180" alt="echo-hands"><br><code>🔒 echo-hands</code><br><sub>strobe trails behind your hands</sub></td><td align="center" width="33%"><img src="gallery/studio/ui-world.gif" width="180" alt="ui-world"><br><code>🔒 ui-world</code><br><sub>Claude UI on top, your clips fly in</sub></td><td align="center" width="33%"><img src="gallery/studio/zoom-through-cut.gif" width="180" alt="zoom-through-cut"><br><code>🔒 zoom-through-cut</code><br><sub>rush through into the next shot</sub></td></tr>
</table>

**The AI video editing program** teaches you how it's done, step by step, and how to customize the studio to your needs and your brand: colors, fonts, style, your own effects.

### 👉 [Join the waitlist](https://learn.ouerfelli-raed.com/en/waitlist/ai-video-editing?src=github)
Pick the studio, the program or both. Waitlist only: -40% at launch, no payment today.

## Honest notes
- Starter versions. It drafts, you approve: watch before you post.
- This free pack adds the effect where you say. It doesn't choose moments, write captions or add sound.

## Credits
Our studio effects: MIT (`LICENSE`). The 16 classic effects are by [@vibha.in.progress](https://github.com/Vibha-Ramprakash/claude-video-effects), also MIT. Details in `THIRD_PARTY.md`.
