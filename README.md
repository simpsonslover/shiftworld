# shiftworld
## Shiftworld data pack (Minecraft 1.21.11)

Shifts the whole Overworld up 64 blocks: bedrock at y=0, sea level at y=127, build limit y=384. Terrain, caves, ores, biomes (incl. deep dark), ancient cities and trial chambers keep the same shape relative to each other, just 64 blocks higher.

**Install:** put `shiftworld.zip` in `<world>/datapacks/` **before** the world is first created.

How it works: vanilla worldgen files are copied with every absolute Y value moved by +64 (dimension height, noise range, `y_clamped_gradient`s, 3D noises re-offset via `shifted_noise`, surface rules, ore/feature height ranges, carvers, ancient city / trial chamber start heights). Nether/End content is left untouched. Regenerate with `shift.py` against misode/mcmeta `1.21.11-data`.

Known limits (hardcoded in the game, can't be fixed by a data pack):
- Deep lava lakes/aquifers (vanilla lava below y=-54) become water.
- Ocean monuments still spawn at the hardcoded y=39, so they end up buried under the raised ocean floor.
- Some fine terrain/cave noise isn't Y-shiftable, so the world is equivalent but not block-for-block identical to a vanilla seed.
