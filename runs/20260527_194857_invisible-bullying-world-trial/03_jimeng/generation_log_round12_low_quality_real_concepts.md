# Round 12 Low Quality Real Concept Images

Purpose: validate the visual direction for Dinggao as hyperreal live-action docu-fiction with degraded consumer-camera realism, rain, cramped rental-room texture, screen compression, and ordinary public spaces polluted by online judgment.

Agent collaboration used:

- Visual concept agent selected the six test subjects from the visual bible: rental room, leaking script, editing screen, delivery-rider public viewing, elevator apology wall, and empty synced room.
- Prompt structurer agent converted each subject into concise Dreamina-safe text-to-image prompts, removing real celebrity / real brand references and keeping the visual instructions non-contradictory.
- Showrunner chose Dreamina CLI model `4.6`, `2k`, `16:9`, then rejected the first overlong prompt style after one failed run and switched to shorter production prompts.

Disclosure rule added after Human feedback:

- Every future image/video pass must expose the exact prompts, negative constraints, parameters, submit IDs, local files, quality read, Human feedback, and next prompt revision plan in `prompt_ledger.md`.
- Human feedback on this set: "真不真假不假".
- Showrunner interpretation: these images are useful as a direction board, but they are still too composed and film-still-like. The next look-test should push harder toward badly captured reality: cheap phone defects, bad autofocus, accidental framing, compression noise, screen moire, low dynamic range, practical ugly light, and less beautiful widescreen composition.

CLI setup:

- Tool: `/Users/bytedance/.local/bin/dreamina`
- Model: `4.6`
- Resolution: `2k`
- Ratio: `16:9`
- Local output directory: `runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/jimeng_outputs/round12_low_quality_real_concepts/`

Generation notes:

- One long-form prompt attempt failed before the final production pass.
- All six final concept images generated successfully.
- The CLI returns image URLs under `result_json.images[0].image_url`.

## Outputs

| ID | Subject | Submit ID | Local File |
| --- | --- | --- | --- |
| DG_CONCEPT_001 | Damp rental room, screen glow, editor as protagonist | `d30bbaa3-22f8-4732-b936-5bc590943e89` | `DG_CONCEPT_001_damp_rental_room_screen_glow.png` |
| DG_CONCEPT_002 | Wet script as gutter, basin reflecting editing timeline | `3543fb7b-7aac-4496-9fa5-b2f4c55a07c2` | `DG_CONCEPT_002_basin_script_reflection.png` |
| DG_CONCEPT_003 | Editing screen manufactures guilt over a fictional male guest | `ecf8a994-2828-4e22-a41b-ec5ff9e6cd54` | `DG_CONCEPT_003_editing_screen_title_face.png` |
| DG_CONCEPT_004 | Delivery rider watching vertical-video judgment in rain | `a2d9a79e-2a36-4a1f-ae23-c80b9591346e` | `DG_CONCEPT_004_delivery_rider_vertical_video_rain.png` |
| DG_CONCEPT_005 | Elevator corridor, apology graffiti, polished ad image | `9e07a4f9-b50e-430c-a985-1e54c3226054` | `DG_CONCEPT_005_elevator_apology_ad_corridor.png` |
| DG_CONCEPT_006 | Empty room at morning, system keeps syncing | `3b3912c7-25b0-40ba-9b53-1e579a67ce6f` | `DG_CONCEPT_006_empty_room_sync_morning.png` |

## Showrunner Read

Useful direction:

- The rental-room and basin images are closest to the film's emotional temperature: damp, poor, practical, and quietly humiliating.
- The delivery-rider and elevator images make the social-system layer visible without leaving the realistic mode.
- The empty-room image is a strong final-image candidate because it makes the machine feel more alive than the absent editor.

Risks to fix in later image/video prompts:

- Some images still look cleaner and more composed than true low-end phone footage. Later prompts should add bad autofocus, lens smears, exposure pumping, and surveillance / cheap-phone framing.
- On-screen Chinese text is unreliable in AI generation. For production, reserve important text for post overlays or UI compositing instead of asking the image model to draw exact characters.
- The protagonist room should not drift into stylized misery. Keep details functional: rent, work badge, old equipment, takeout, water damage, not decorative poverty.
