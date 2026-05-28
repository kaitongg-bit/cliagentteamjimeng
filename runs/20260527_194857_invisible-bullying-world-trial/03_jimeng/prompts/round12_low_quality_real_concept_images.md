# Round 12: Low-Quality Real Concept Image Prompt Pack

## Agent Roles Used

- **Showrunner**: chose the current goal: generate a small look-test set before fine storyboard.
- **Visual Concept / Medium Agent**: selected the 6 image subjects that best test the image species.
- **Prompt Structurer Agent**: translated the look into Dreamina `text2image` prompts and negative constraints.
- **CLI Runner**: intended execution path is Dreamina/Jimeng CLI (`dreamina`).

## Medium Lock

`hyperreal live-action docu-fiction + degraded consumer-camera realism + screen compression pollution`

Not animation, not GTA/game cinematic, not cyberpunk, not retro sci-fi, not glossy commercial cinema.

## Suggested Dreamina Parameters

```yaml
task: text2image
ratio: 16:9
resolution_type: 2k
model_version: 5.0
poll: 120
session: 0
```

For `DG_CONCEPT_005` elevator ad, `3:4` can be tested later, but first round stays `16:9` for consistent short-film framing.

## Unified Negative Prompt

```text
animation, anime, illustration, concept art, game render, CGI, 3D render, cyberpunk, retro sci-fi, futuristic city, hologram, neon data stream, hacker room, luxury apartment, glamorous movie poster, beautiful cinematic poster lighting, fashion editorial, glossy commercial photography, heroic composition, horror movie lighting, jump scare, electric sparks, dramatic thriller lighting, clean designer interior, spotless desk, exaggerated poverty, staged mess, readable long text, walls of text, real brand logo, real platform logo, real celebrity face, famous actor likeness, watermark, subtitles, big red arrows, meme graphics, comic book style
```

## DG_CONCEPT_001 / damp_rental_room_screen_glow

Purpose: Validate the main rental room: cheap, humid, physically real, screen-lit.

```text
Hyperreal live-action docu-fiction still, degraded consumer camera realism, shot on a cheap phone or low-end mirrorless camera with compression artifacts and slight screen-video pollution. A cramped 15 square meter old Chinese rental room at rainy night, damp gray-white walls, peeling paint, taped aluminum window seam leaking water, a plastic basin catching drops on the floor. One old computer monitor is the only strong light source, cold blue-gray glow revealing an unpaid bill, a faded work badge, cold steamed bun, takeout soup container, cheap tissues, coins, old access card, and a messy editing desk. A tired 32-year-old Chinese freelance video editor in a worn dark hoodie sits half in shadow, not theatrical, not handsome, just exhausted and focused. Realistic ugly fluorescent spill from the corridor under the door, humid air, dirty tile seams, practical location, restrained, cold, unglamorous, ordinary urban China.
```

## DG_CONCEPT_002 / wet_script_water_basin_reflection

Purpose: Validate the water/script/screen reflection/power-strip danger motif.

```text
Hyperreal live-action docu-fiction close-medium still, degraded low-end camera realism, visible compression noise, imperfect autofocus, dim apartment interior. A softened wet old variety show script is folded like a practical gutter under a leaking window, guiding rainwater into a pale plastic basin. The cover is water-stained and warped, with only a few small Chinese prop characters barely visible, not a readable page. The basin water reflects a dark gray editing timeline from a computer screen, the reflection trembling; small flakes of peeled wall paint float at the bottom. Beside it, a cheap power strip sits on two swollen old books, too close to a spreading water stain but no sparks. Cold monitor light, damp wall texture, oil-stained takeout lid reflection, shallow focus, restrained realistic anxiety, no melodrama.
```

## DG_CONCEPT_003 / editing_screen_title_over_face

Purpose: Validate title-over-face and editing manipulation without turning the screen into a readable info board.

```text
Hyperreal live-action docu-fiction still from inside a cheap apartment editing room, degraded consumer camera image, compressed screen recording pollution. Over-the-shoulder view of a tired Chinese video editor at a single monitor, his face lit by cold screen light and reflected in the dark window glass. On the monitor, a generic dark gray editing software interface with dense timeline, waveforms, thumbnails, and a blurred entertainment-show frame; a short bold title bar covers the face of a fictional male TV guest, but the text is not readable except as graphic blocks. Rain trails on the window, taped window seam, coffee stain on mouse pad, cold bun near his hand, muted dirty blue-gray palette. The image should feel like a real low-budget behind-the-scenes documentary capture, not a designed film still.
```

## DG_CONCEPT_004 / rainy_awning_delivery_phone

Purpose: Validate the first expansion from room to public space through delivery-rider phone playback.

```text
Hyperreal live-action docu-fiction street still, degraded cheap phone camera realism, rainy night in an ordinary Chinese residential compound gate. Under a translucent greenish plastic awning, a delivery rider in a generic rain poncho with no real brand logo waits on an electric scooter. A smartphone mounted on the handlebar plays a vertical video; the screen is bright but mostly unreadable, with blurred comment blocks covering the face of a fictional entertainment figure. Red traffic light reflected on wet asphalt, rainwater dripping from the awning edge, wet gloves, battery pack cable, cheap food bags, harsh practical streetlight, compressed highlights, unglamorous documentary realism, cold and humid atmosphere.
```

## DG_CONCEPT_005 / elevator_ad_apology_smudge

Purpose: Validate the public-space pollution image: online judgment written onto a cheap elevator ad.

```text
Hyperreal live-action docu-fiction still, old Chinese apartment elevator lobby, degraded low-end mirrorless camera look with slight blur and compression. A scratched metal elevator door and a cheap lifestyle delivery advertisement on the wall: a polished fictional actress face smiles too cleanly in the ad, no real celebrity likeness, no real brand. Next to the poster, fresh black marker handwriting says only "道歉", slightly smudged by a wet sleeve. Peeling wall, adhesive residue, small illegal sticker marks, yellowed wall base, wet footprints, flickering cold fluorescent light reflected in the elevator metal. A tired Chinese man stands near the doorway in the background, still and half cut off, not posing. Ordinary public surface polluted by online judgment, restrained, cold, realistic.
```

## DG_CONCEPT_006 / empty_room_sync_morning

Purpose: Validate the ending feeling: person gone, system still running.

```text
Hyperreal live-action docu-fiction final-room still, degraded consumer camera realism, early gray morning after rain. An empty damp old Chinese rental room, no person present. The computer is still on, casting weak cold light over the messy editing desk; the screen shows a generic sync notification and a dark editing timeline as blurred UI shapes, not readable text. Plastic basin on the floor, one water drop ripple, damp wall, taped leaking window, tied takeout trash bag near the door, swollen old books, power strip moved farther away from the water. Pale daylight leaks through cheap curtains, the room feels abandoned but the system keeps running. Realistic, quiet, cold, unromantic, low-budget short film texture, compressed digital noise, no moralizing.
```
