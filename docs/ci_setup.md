# CI Setup - open_mmwave Rev G

The CI workflow is defined in `.github/workflows/hardware_ci.yml`.

## Steps
- Runs `tools/ci_pipeline.py` to generate `data/ci_baseline.json`.
- Extend with validation tools as needed.
