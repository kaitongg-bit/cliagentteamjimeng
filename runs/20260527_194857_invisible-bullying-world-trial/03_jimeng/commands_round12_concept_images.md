# Round 12 Dreamina CLI Commands: Low-Quality Real Concept Images

## Status

CLI found:

```bash
/Users/bytedance/.local/bin/dreamina
```

Current blocker inside Codex:

```text
authsdk: store unavailable: save: store: backend unavailable: exit status 161
```

This means the Dreamina CLI can be found, but OAuth credential storage is unavailable inside the current Codex sandbox. Run login/generation in a normal macOS Terminal if this persists.

## Login

```bash
/Users/bytedance/.local/bin/dreamina login
```

If using headless flow:

```bash
/Users/bytedance/.local/bin/dreamina login --headless
/Users/bytedance/.local/bin/dreamina login checklogin --device_code=<device_code> --poll=30
```

## Output Directory

```bash
mkdir -p runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/jimeng_outputs/round12_low_quality_real_concepts
```

## Commands

> Note: Dreamina CLI submits async tasks. Capture each `submit_id`, then query with `dreamina query_result --submit_id=<id>`.

### DG_CONCEPT_001

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_001/{flag=1; next} /## DG_CONCEPT_002/{flag=0} flag')"
```

### DG_CONCEPT_002

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_002/{flag=1; next} /## DG_CONCEPT_003/{flag=0} flag')"
```

### DG_CONCEPT_003

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_003/{flag=1; next} /## DG_CONCEPT_004/{flag=0} flag')"
```

### DG_CONCEPT_004

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_004/{flag=1; next} /## DG_CONCEPT_005/{flag=0} flag')"
```

### DG_CONCEPT_005

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_005/{flag=1; next} /## DG_CONCEPT_006/{flag=0} flag')"
```

### DG_CONCEPT_006

```bash
/Users/bytedance/.local/bin/dreamina text2image \
  --model_version=5.0 \
  --resolution_type=2k \
  --ratio=16:9 \
  --poll=120 \
  --prompt="$(cat runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md | awk '/## DG_CONCEPT_006/{flag=1; next} flag')"
```

## Recommended Manual Alternative

If shell substitution is fragile, copy each prompt from:

```text
runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/prompts/round12_low_quality_real_concept_images.md
```

and run:

```bash
/Users/bytedance/.local/bin/dreamina text2image --model_version=5.0 --resolution_type=2k --ratio=16:9 --poll=120 --prompt="PASTE_PROMPT_HERE"
```
