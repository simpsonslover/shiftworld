# shiftworld
## Shiftworld data pack (Minecraft 1.21.11)

Moves the Overworld floor from y=-64 to y=0 (build limit stays at y=320, bedrock at y=0–4).

**Install:** zip `pack.mcmeta` + `data/` (or drop this folder) into `<world>/datapacks/` **before** the world is first created — dimension height can't change safely in an existing world.

Files:
- `data/minecraft/dimension_type/overworld.json` — `min_y: 0`, `height: 320`
- `data/minecraft/worldgen/noise_settings/overworld.json` — noise range 0–320, bottom slide moved to y=0–24, ore veins start at y=0
