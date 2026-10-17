---
name: get-bounding-box-data
description: Use when the user asks to get, show, or read bounding box info of a Transport Fever 3 model. Matches requests like "Please get bounding box info from model xyz", "Please get bounding box info from model xyz.mdl", "Bitte gebe Bounding Box info vom Model xyz" or "... xyz.mdl".
---

# Get bounding box data

Reads the bounding box of a Transport Fever 3 model (`.mdl`) from the currently opened project and returns it as JSON. Only files inside the project are searched. Nothing is changed in the project.

## Instructions

1. Extract the model name `xyz` from the request (with or without `.mdl`).
2. Run the bundled script from the project root (the workspace folder):

   ```
   python .agents/skills/get-bounding-box-data/scripts/get_bounding_box_data.py "xyz"
   ```

   Optionally pass `--root <project dir>`; the default is the current directory.
3. On success, show the JSON printed by the script to the user unchanged:

   ```json
   {
       "bounding_box": {
           "min": { "x": 0, "y": 0, "z": -1.99883 },
           "max": { "x": 13.5, "y": 5, "z": 0 }
       }
   }
   ```

4. If the script exits with an error (file not found in the project, multiple files with that name, or no bounding info), tell the user the message and stop. Do not guess, search outside the project, or invent values. For multiple matches, ask the user which file is meant.

## Source format

The script uses regular expressions (no Lua parsing) on this section of the `.mdl` file:

```lua
boundingInfo = {
    bbMax = { bbMaxX, bbMaxY, bbMaxZ, },
    bbMin = { bbMinX, bbMinY, bbMinZ, },
},
```
