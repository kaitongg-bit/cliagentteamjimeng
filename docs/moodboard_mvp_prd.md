# Moodboard MVP PRD

## 1. Product Thesis

For aesthetic-heavy creative tasks, the agent team should not generate final-looking images too early.

The MVP exists to help the human build a prior expectation before AI generation. Agents should turn a fuzzy visual desire into searchable reference tasks, collect human taste signals, analyze reference images, and only then produce prompts or shot designs.

Core belief:

> AI should scaffold the user's imagination, not replace it with the first plausible image.

## 2. Current Problem

In the Dinggao look test, the agent team generated concept images before the human had a clear visual expectation.

This caused three issues:

- The AI image became a premature answer and pulled the human's taste toward it.
- Prompt writing compressed too many art-direction decisions into one long prompt.
- The output looked like "dirty cinematic realism" instead of "badly captured reality".

The workflow needs a stage before image generation:

- Agent proposes what references to look for.
- Human collects images and marks what is useful.
- Agent analyzes those references into shot rules.
- Only then does the prompt agent write generation prompts.

## 3. Users

Primary user:

- AI video creator / director who has taste but may not yet have precise film-language vocabulary.
- Wants to make shorts, series, ads, music videos, animation, or platform-native video.
- Needs help externalizing visual intuition before committing to AI generation.

Secondary users:

- Screenwriter using references to clarify tone.
- Director / cinematographer agent converting taste into camera rules.
- Prompt structurer agent converting visual rules into generation prompts.

## 4. MVP Goal

Create a lightweight local moodboard workspace where:

- Agents generate "reference search cards" for key shots.
- The human drops images into a local folder.
- The UI shows those images next to the cards.
- The human labels each image by what should be learned from it.
- Agents analyze selected images and produce reusable visual rules for storyboard and prompt generation.

## 5. Non-Goals

MVP should not:

- Become a full design tool like Figma.
- Require cloud upload or account systems.
- Auto-scrape copyrighted images.
- Generate final film stills before human taste calibration.
- Pretend reference images can be copied directly.

## 6. Success Criteria

The MVP is useful if:

- The human can add 10-30 reference images in under 5 minutes.
- Each image can be tagged as "use / avoid / only use X".
- Agents can summarize references into concrete shot rules.
- Later prompts become shorter, more controlled, and easier for the human to judge.
- The human can say why an AI output is wrong before seeing the next AI output.

## 7. Core Workflow

### Step 1: Agent Creates Reference Search Cards

For each key shot, the showrunner asks relevant agents to create a card.

Agents involved:

- Showrunner: chooses which shots need moodboard help.
- Director: defines dramatic purpose and viewer feeling.
- Cinematographer: defines camera position, shot size, lens feeling, light source.
- Visual concept designer: defines space, texture, color, references to search.
- Editor: defines where the image sits in rhythm.
- Prompt structurer: records what visual facts may later become prompts, but does not generate yet.

Card fields:

```yaml
card_id:
scene_id:
shot_name:
dramatic_function:
viewer_should_feel:
look_for:
  - character blocking
  - spatial relationship
  - shot size
  - camera position
  - light / color
  - texture / medium
avoid:
  - wrong genre
  - wrong era
  - wrong class signal
  - over-stylized risk
suggested_search_terms:
  zh:
  en:
reference_film_or_video_targets:
  - title:
    watch_for:
human_notes:
```

### Step 2: Human Collects References

The MVP creates a local folder:

```text
runs/<project_id>/05_moodboard/inbox/
```

The human can put screenshots, stills, web images, phone photos, or frame grabs into the folder.

Supported file types:

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

The UI watches or refreshes this folder and displays new images.

### Step 3: Human Tags Images

The human does not need to write formal critique. They label what the image is useful for.

Required tags:

- `靠近`
- `远离`
- `只要站位`
- `只要空间`
- `只要景别`
- `只要影调`
- `只要光线`
- `只要质感`
- `只要人物距离`
- `危险但有一点可学`

Optional free note:

```text
我只要它的门框站位，不要它的电影感。
```

### Step 4: Agent Analyzes References

For selected images, the image-analysis pass extracts:

```yaml
image_id:
linked_card_id:
human_tags:
scene_type:
shot_size:
camera_position:
camera_height:
subject_position:
foreground:
background:
space_pressure:
light_source:
color_temperature:
medium_texture:
what_to_learn:
what_to_avoid:
prompt_ready_rules:
```

The agent must separate:

- What the human wants to copy structurally.
- What should not be copied stylistically.
- What can be translated into storyboard.
- What can be translated into prompts.

### Step 5: Agent Produces Moodboard Synthesis

Output file:

```text
runs/<project_id>/05_moodboard/moodboard_synthesis.md
```

Synthesis sections:

- Human taste summary.
- Key accepted references.
- Key rejected references.
- Shot-by-shot camera / space / tone rules.
- Prompt rules.
- Negative prompt rules.
- Open questions for the human.

## 8. MVP UI

### Layout

Three-column working surface:

```text
Left: Reference Search Cards
Center: Image Grid
Right: Selected Image Inspector
```

### Left Column: Cards

Each card shows:

- Shot name.
- Dramatic function.
- What to look for.
- What to avoid.
- Search terms.
- Reference targets.

Actions:

- Select card.
- Mark card as resolved / unresolved.
- Add human note.

### Center Column: Moodboard Grid

Shows images from:

```text
runs/<project_id>/05_moodboard/inbox/
```

Each image tile shows:

- Thumbnail.
- Filename.
- Linked card.
- Human tags.
- Agent analysis status.

Actions:

- Link to selected card.
- Tag image.
- Mark as accepted / rejected.
- Open larger preview.

### Right Column: Inspector

Shows selected image plus:

- Human tags.
- Human note.
- Agent image analysis.
- "Use this for" checklist.
- "Avoid this" checklist.

## 9. Data Model

### File Structure

```text
runs/<project_id>/05_moodboard/
  reference_cards.yaml
  moodboard_items.json
  moodboard_synthesis.md
  inbox/
  accepted/
  rejected/
  exports/
```

### reference_cards.yaml

```yaml
cards:
  - card_id: MB_001
    scene_id: S01
    shot_name: Doorway view of Xu Lin at desk
    status: unresolved
    dramatic_function: First proof of life pressure, not villainy.
    viewer_should_feel: The room is stronger than the person.
    look_for:
      - doorway blocking
      - cramped room depth
      - back-turned figure at desk
      - screen as practical light
    avoid:
      - cyberpunk edit room
      - retro CRT computer
      - beautiful cinematic poverty
    suggested_search_terms:
      zh:
        - 出租屋 门口 电脑 背影
        - 旧小区出租屋 漏水 电脑桌
      en:
        - cramped apartment doorway computer back view
        - low income room computer screen light
```

### moodboard_items.json

```json
[
  {
    "image_id": "IMG_0001",
    "file_path": "inbox/example.png",
    "linked_card_id": "MB_001",
    "human_tags": ["只要站位", "远离"],
    "human_note": "站位接近，但太电影化。",
    "agent_analysis": {
      "shot_size": "wide shot",
      "camera_position": "doorway, looking inward",
      "subject_position": "right third, back turned",
      "what_to_learn": ["door frame as foreground pressure"],
      "what_to_avoid": ["polished lighting"]
    }
  }
]
```

## 10. Dinggao First MVP Cards

The first version should create cards for these shots:

1. Doorway view of Xu Lin at the editing desk.
2. Leaking room: basin, script, power strip, screen reflection.
3. Editing screen creates the first guilt narrative.
4. Delivery rider watching vertical-video judgment in rain.
5. Elevator corridor with apology pollution.
6. Xu Lin's father restaurant being hit by review pressure.
7. Public opinion montage on cheap screens.
8. Final empty room: person gone, system still syncing.

Each card should ask the human to find references for:

- Blocking / standing position.
- Space pressure.
- Shot size.
- Camera angle.
- Practical light.
- Texture / medium.
- What must be avoided.

## 11. Agent Team Responsibilities

### Showrunner

- Decides when moodboard is required.
- Selects the key shots.
- Prevents premature image generation.
- Records human decisions.

### Director

- Defines emotional function per shot.
- Rejects references that look good but harm the theme.

### Cinematographer

- Converts references into camera language.
- Tracks shot size, angle, light, movement, and frame logic.

### Visual Concept Designer

- Suggests reference domains.
- Translates human taste into space, props, texture, color, and material rules.

### Editor

- Judges whether a reference supports the film's rhythm.
- Flags images that are too iconic or too explanatory.

### Prompt Structurer

- Does not write final prompts until the moodboard synthesis exists.
- Converts accepted visual rules into concise prompt blocks.
- Preserves negative constraints from rejected references.

### Audience Panel

- Reviews whether the visual direction manipulates the audience in the intended way.
- Flags over-obvious or moralizing imagery.

### Human Creative Director

- Adds images.
- Tags what is useful.
- Gives final taste approval.

## 12. Implementation Plan

### Phase 1: Static Local MVP

Build a simple HTML/JS interface that:

- Reads a generated `moodboard_items.json`.
- Displays image thumbnails from the local project folder.
- Allows manual tagging and notes in the browser.
- Saves updated JSON through a small local server or export file.

### Phase 2: Folder-Linked MVP

Add a local watcher / refresh action:

- Scan `05_moodboard/inbox/`.
- Add new image files to `moodboard_items.json`.
- Display them automatically.

### Phase 3: Agent Analysis Pass

Add a command:

```text
analyze-moodboard
```

It should:

- Read `reference_cards.yaml`.
- Read `moodboard_items.json`.
- Analyze tagged images.
- Write `moodboard_synthesis.md`.

### Phase 4: Prompt Handoff

Prompt structurer reads:

- `moodboard_synthesis.md`
- accepted references
- rejected reference notes

Then writes:

- `team_jimeng_prompts.md`
- `prompt_ledger.md`
- `prompt_contradiction_check.md`

## 13. Open Product Questions

- Should image files be copied into `accepted/` and `rejected/`, or only tagged in JSON?
- Should the UI allow drag-and-drop upload, or is folder drop enough for MVP?
- Should image analysis happen automatically when a tag changes, or only on a button click?
- Should the human be able to compare AI-generated outputs against moodboard references side by side?
- How much reference-image metadata should be stored to avoid copyright and privacy risk?

## 14. MVP Acceptance Test

For Dinggao, MVP is accepted when:

- 8 reference cards are visible in the UI.
- The human can drop at least 5 images into `inbox/` and see them.
- The human can tag an image with "只要站位" and write a note.
- The agent can read those tags and produce a moodboard synthesis.
- The next generated prompt explicitly cites which moodboard rules it used and which rejected directions it avoided.
