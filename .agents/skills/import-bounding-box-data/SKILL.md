---
name: import-bounding-box-data
description: Use when the user asks to add, import, or update bounding info or bounding-box data from a Transport Fever 3 model in a bridge or tunnel config. This includes the exact request “Please add bounding info from model xyz”.
---

# Import bounding box data

When the user asks to add bounding info from a model (including the exact request “Please add bounding info from model xyz”), carry out the requested file edit; do not just explain the procedure. Here, `xyz` represents the model name supplied by the user. Apply this skill to equivalent English or German requests and to requests for one or more models.

This skill does not read bounding boxes or build the call itself. It uses the `create-addpartmodel-function-call` skill (which in turn uses `get-bounding-box-data`) and writes the resulting call into the config.

## Instructions

1. Identify the target config (`.tunnel.lua` or `.bridge.lua`) and all requested model names. If the user does not name a config, use the uniquely identifiable target config in the project. Ask for clarification only if no target can be identified or multiple targets are plausible. Support multiple names in a request, including comma-separated names and names joined by “and” or “und”. Use each name as the model filename stem and append `.mdl` unless the extension is already present.
2. In the target config, find the repository variable used by `Yabu.initializeModelPartRepository()` (usually `repo`). Use its actual name in the next step.
3. For each requested model, follow the `create-addpartmodel-function-call` skill ("Please create a addPartModel function call for model xyz"), passing the repository variable name. Use the returned `Yabu.addPartModel(...)` call exactly as produced. If that skill reports an error (model not found, ambiguous model, missing bounding info), do not guess or invent values: leave that model unchanged and report what could not be resolved. If multiple model files are plausible, ask the user which one is meant.
4. Write each call into the target config:
   - If a `Yabu.addPartModel` call for the same model filename (e.g. `"xyz.mdl"`) already exists for that repository, replace the entire existing call with the new one. If it is already identical, leave it unchanged.
   - Otherwise add the call in the `--Part Models` section. If that section is absent, place it immediately after the `Yabu.initializeModelPartRepository()` call.
   - Adapt indentation to the file's existing formatting.
5. Preserve all unrelated config content and never add a duplicate registration.
