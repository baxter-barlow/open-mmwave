# Gerber Validation - open_mmwave Rev G

Sources: `data/gerber_analysis.json`, Gerber files from the fabrication package.

## Layer Completeness
- Ensure all required layers are present: GTL/GBL/GTS/GBS/GTO/GBO/GTP/GBP and GM1 outline.

## Board Outline
- Outline bounding box extracted from GM1 layer (raw coordinate units).
- Convert to mm/inches using Gerber format settings if needed.

## Feature Statistics
- Draw/flash counts and aperture counts are in `data/gerber_analysis.json`.
