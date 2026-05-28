# Prompt Ledger

This file is the required public record for every image/video generation pass in the Dinggao agent-team experiment.

Each generation round must expose:

- Source agents and their responsibilities.
- Exact prompt text used by the CLI.
- Negative constraints or safety/style exclusions.
- Model and generation parameters.
- Submit IDs and local output files.
- Showrunner quality read.
- Human feedback.
- Next prompt revision plan.

## Round 12 Human Feedback

Human feedback: the first concept set feels "真不真假不假".

Showrunner interpretation:

- The current images are too close to composed film stills and concept art.
- The direction should move from "dirty cinematic realism" toward "badly captured reality".
- Next revision should reduce intentional composition, reduce polished lighting, avoid perfect widescreen beauty, and add cheap-device defects: bad autofocus, low dynamic range, lens smears, exposure pumping, rolling shutter, phone HDR artifacts, video compression, screen moire, accidental cropping, and ordinary ugly practical locations.

Next prompt revision principle:

- Keep the story world realistic.
- Make the camera less talented.
- Make the image feel collected from life, not staged for a moodboard.

## Prompt Structurer Self-Audit On DG_CONCEPT_001

Human critique: the prompt is too long, lacks structure, and the result feels neither truly real nor fully artificial.

Prompt agent judgment:

- The original direction was valid: it tried to lock the main rental-room location as damp, cheap, screen-lit, and unglamorous.
- The core elements were useful: leaking aluminum window, plastic basin, old monitor, unpaid bill, faded work badge, cold food, tired freelance editor.
- The failure was execution: the prompt became a prop list and visual-bible compression instead of a controlled image-generation instruction.
- "Low quality real" was named but not technically specified. The prompt should have described device failure: bad autofocus, dirty lens, greenish auto white balance, crushed dark areas, overexposed screen, JPEG compression, accidental crop, and screen moire.
- Too many details competed for attention, making the image feel staged and composed.
- The protagonist description was too portrait-like; future prompts should make the room believable first and let the person appear as a caught presence.

Revised structure for future image prompts:

```yaml
intent: one visual question this image is testing
camera_source: device, defects, compression, focus, exposure
scene: place, time, weather, space
composition: where the camera is and why the frame feels accidental
light: practical sources and exposure mistakes
visible_details: 4-6 mandatory objects only
human_presence: posture and silhouette, not star portrait
screen_rule: unreadable UI or composited text plan
style: exact medium feel
negative: strongest failure modes to prevent
```

DG_CONCEPT_001 revised prompt:

```text
A bad cheap-phone photo from the doorway of a tiny old Chinese rental room at rainy night. Handheld, slightly tilted, soft focus, dirty lens, greenish auto white balance, crushed dark areas, overexposed computer screen, visible JPEG compression noise. The room is cramped and damp: peeling gray-white wall, taped leaking aluminum window, plastic basin on the floor catching water, cheap desk with one old monitor, unpaid bill partly under a takeout soup lid, power strip lifted on swollen books. A tired man sits at the desk with his back half turned, only a dull silhouette in cold screen glow. The editing software on the monitor is unreadable, just gray blocks and timeline-like light. Ordinary, humid, ugly, unglamorous, documentary accident, like a real still found in a phone gallery.
```

Negative constraints:

```text
cinematic lighting, beautiful composition, movie poster, cyberpunk, neon, sci-fi, hacker room, luxury apartment, clean design interior, staged poverty, dramatic horror, electric sparks, glossy photography, anime, illustration, CGI, game render, readable long text, real brand logo, real platform logo, real celebrity face
```
