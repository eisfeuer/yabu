---
name: setup-yabu-project
description: Use when the user asks to set up a Yabu project for a Transport Fever 3 bridge or tunnel mod. Matches requests like "please setup yabu project" or "bitte setze das yabu projekt auf".
---

# Setup Yabu project

Turns the template in `game_data` into a bridge or tunnel mod. Run this only once on a fresh template (it expects the `new_bridge` placeholders to still exist).

## Steps

1. Ask the user (ask_user, one form with all fields) for:
   - **Mod id** (lowercase letters, digits, underscores; e.g. `yourname_my_bridge`)
   - **File name** of the bridge/tunnel without extension (e.g. `my_bridge`)
   - **Display name** (e.g. `My Bridge`)
   - **Type**: bridge or tunnel
2. Run from the repository root:

   ```
   python .agents/skills/setup-yabu-project/setup_yabu_project.py --mod-id <mod_id> --file-name <file_name> --display-name "<display name>" --type <bridge|tunnel>
   ```

3. Report the result and grep to verify no `new_bridge` / `NEW_BRIDGE` / `New Bridge` placeholders remain (the `.tga` icon referenced in the config still has to be created by the user).

## What the script does

- Replaces `yourname_new_bridge` with the mod id in all text files in `game_data`.
- In `.bridge.lua` and `strings.json`: `NEW_BRIDGE_NAME` → `<FILE_NAME_UPPERCASE>_NAME`.
- In `.bridge.lua`: `new_bridge` → file name (updateFn `fileName`, `.tga` icon, model path); renames `new_bridge.bridge.lua` and `new_bridge.script.lua`.
- In `strings.json` and `modinfo.json`: `New Bridge` → display name (JSON-escaped).
- If type is **tunnel**: renames `*.bridge.lua` → `*.tunnel.lua`, folder `infrastructure/bridge` → `infrastructure/tunnel`, and `/infrastructure/bridge` → `/infrastructure/tunnel` in all text files. For bridges these steps are skipped.
