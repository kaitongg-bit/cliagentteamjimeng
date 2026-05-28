# Showrunner Dynamic Orchestration

## Why This Exists

Agent team workflows cannot be a fixed conveyor belt. The role library can be stable, but the order of agents must change with the project type and the current highest-risk unresolved decision.

In the `定稿` run, the user interrupted after screenplay and rough storyboard to ask what the film should feel like: animation, silent film, low-quality documentary, live action, GTA-like game, retro sci-fi, AIGC art style, etc. That intervention exposed a missing orchestration rule: before fine storyboard and prompt generation, the team must lock the image medium and direct viewing experience.

## Core Rule

The Showrunner must decide the next agent step by asking:

1. What is the biggest unresolved decision right now?
2. If this decision is wrong or late, will it force major downstream rewrite?
3. Which agents are qualified to decide it, and which agents should only execute after it is locked?

If the unresolved decision can cause major rewrite, stop the default workflow and convene the relevant agents.

## Medium And Look Lock

Before fine storyboard, shot prompts, or large-scale generation, the Showrunner must check whether the project has a locked medium promise.

Medium promise means the viewer's first-body impression of what they are watching:

- hyperreal live-action film
- low-quality consumer documentary or leaked footage
- phone-shot vertical video
- screenlife film
- stop-motion or handmade animation
- polished 3D animation
- GTA-like game cinematic
- dieselpunk or retro sci-fi
- AIGC collage / experimental synthetic image
- mixed-media hybrid

This is not the same as props, sets, color palette, or costume. It controls camera movement, performance scale, grain, compression, UI visibility, prompt language, asset generation, and editing rhythm.

## Trigger Conditions

Trigger a Medium And Look Lock when:

- the user asks what the piece should feel like visually
- the visual bible describes locations and props but not image species
- storyboard would become inconsistent without a medium decision
- the project type changes, such as film festival short, short-video platform drama, animation, ad, MV, or game cinematic
- prompt structuring is about to begin and style terms are still generic

## Recommended Agent Participants

- Showrunner: frames the decision and records the lock
- Visual Concept Designer: proposes style routes and visual worlds
- Director: judges camera, performance, pacing, and directorial feasibility
- Cinematographer: judges lens, light, movement, grain, exposure
- Prompt Structurer: judges whether the style can be translated into controllable generation prompts
- Audience Panel: judges what the viewer will think they are watching
- Human Creative Director: final taste and product decision

## Example: `定稿`

The current best route is not animation, GTA, cyberpunk, or retro sci-fi.

Recommended route:

`hyperreal live-action docu-fiction + degraded consumer-camera realism + screen compression pollution`

Meaning:

- The main room should feel like real live action.
- The image should not be glossy commercial cinema.
- Some layers should feel like cheap phone video, screen recording, reposted short-video compression, hallway audio leakage, and accidental surveillance.
- The film should remain highly realistic, cold, humid, and physically grounded.

## Project-Type Examples

### Film Festival Short

Prioritize theme, structure, medium promise, directorial language, and ambiguity control.

Likely order:

Showrunner -> Screenwriter/Opposition/Audience -> Screenwriter -> Director/Visual Concept -> Reviewer -> Rough Storyboard -> Medium And Look Lock -> Fine Storyboard -> Prompt Structurer.

### Short-Video Platform Drama

Prioritize hook, persona, rhythm, episode-end retention, platform-native editing, and audience desire.

Likely order:

Showrunner -> Platform/Audience/Growth Agent -> Screenwriter -> Hook/Suspense Reviewer -> Episode Structure -> Director/Editor -> Prompt Structurer.

### Animation

Prioritize world, character silhouettes, animation style, asset reuse, and motion language.

Likely order:

Showrunner -> Visual Concept/Character Design -> Screenwriter -> Director -> Storyboard -> Asset/Prompt Pipeline.

### Brand Film Or Ad

Prioritize brand promise, target audience, product rules, compliance, and memorability.

Likely order:

Brand Strategy -> Creative Concept -> Director/Visual Concept -> Copy -> Storyboard -> Compliance -> Prompt Structurer.

### Music Video Or Mood Film

Prioritize rhythm, image motifs, musical structure, color, movement, and repeatable visual grammar.

Likely order:

Director/Editor/Visual Concept -> Lightweight Writer -> Storyboard -> Prompt Structurer.

## Decision Log Template

```md
# Orchestration Decision

## Current Default Next Step

## Why The Default Step Is Unsafe Or Safe

## Biggest Unresolved Decision

## Agents Convened

## Options Considered

## Human Taste Notes

## Locked Decision

## Downstream Impact

## Files To Update
```

## Anti-Pattern

Do not continue to fine storyboard merely because rough storyboard exists.

Do not continue to prompt generation merely because a visual bible exists.

If the project has not decided what kind of image it is, the next output will look precise but point in different directions.
