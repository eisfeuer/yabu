---
name: create-addpartmodel-function-call
description: Use when the user asks to create an addPartModel function call for a Transport Fever 3 model. Matches requests like "Please create a addPartModel function call for model xyz" or "Bitte erzeuge einen addPartModel Funktionsaufruf für model xyz".
---

# Create addPartModel function call

Builds the `Yabu.addPartModel(...)` call that registers a model in a `PartModelRepository`, using the model's bounding box. The call is only shown to the user; no file is edited unless the user asks for it.

## Instructions

1. Extract the model name `xyz` (with or without `.mdl`) and, if given, the repository variable name. The default variable name is `repo`.
2. Get the bounding box by following the `get-bounding-box-data` skill ("Please get bounding box info from model xyz"). If it reports an error (model not found, ambiguous, no bounding info), report it and stop. Do not guess values.
3. Pass the returned JSON to the bundled script:

   ```
   python .agents/skills/create-addpartmodel-function-call/scripts/create_addpartmodel_call.py "xyz" --repo repo --json '<bounding box JSON>'
   ```

   If quoting JSON in the shell is awkward, pipe it via stdin instead (omit `--json`).
4. Show the printed Lua call to the user in a `lua` code block. If the script fails, show the error and stop.

## Example

Input JSON:

```json
{ "bounding_box": { "min": { "x": 0, "y": -0.9, "z": -1.99883 }, "max": { "x": 13.5, "y": 0, "z": 1.01886 } } }
```

Output:

```lua
Yabu.addPartModel(
    repo,
    "xyz.mdl",
    { { 0, -0.9, -1.99883, }, { 13.5, 0, 1.01886, } }
)
```

The function signature is `yabu.addPartModel(repo, partModelId, bb, options)`, where `bb` is `{ { minX, minY, minZ, }, { maxX, maxY, maxZ, } }`.
