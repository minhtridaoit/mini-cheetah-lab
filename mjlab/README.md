# Mini Cheetah Lab — MjLab runtime

This directory contains the vendored MjLab 1.6.0 runtime and this project's
Mini Cheetah model, velocity tasks, and PPO configuration. Use the
[project README](../README.md) for setup and training instructions.

Only Mini Cheetah is supported. The other upstream robot assets, task
configurations and associated demos are not included in this runtime.

Run these commands from this directory after installing dependencies with uv:

```sh
uv run python scripts/view_mini_cheetah.py
uv run train Mjlab-Velocity-Flat-MiniCheetah --env.scene.num-envs 256
uv run train Mjlab-Velocity-Rough-MiniCheetah --env.scene.num-envs 16
```

Configuration files:

- `src/mjlab/asset_zoo/robots/mini_cheetah/`: model, meshes and actuator settings.
- `src/mjlab/tasks/velocity/config/mini_cheetah/env_cfgs.py`: environment settings.
- `src/mjlab/tasks/velocity/config/mini_cheetah/rl_cfg.py`: PPO settings.

The Python package remains named `mjlab` to preserve its imports. This runtime
is part of Mini Cheetah Lab; its original source is
[mujocolab/mjlab](https://github.com/mujocolab/mjlab). The Apache-2.0 license
and original copyright notices are retained in [LICENSE](LICENSE).
Upstream documentation and citation metadata are preserved in
[docs/UPSTREAM_README.md](docs/UPSTREAM_README.md) and
[docs/UPSTREAM_CITATION.cff](docs/UPSTREAM_CITATION.cff).
