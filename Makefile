.PHONY: help view check test-config train-flat train-rough

NUM_ENVS ?= 256

help:
	@echo "make view         Open the Mini Cheetah 3D pose viewer"
	@echo "make check        Format, lint, and type-check MjLab"
	@echo "make test-config  Check registered task configurations"
	@echo "make train-flat   Train on flat terrain (NUM_ENVS=256)"
	@echo "make train-rough  Train on rough terrain (NUM_ENVS=256)"

view:
	cd mjlab && uv run python scripts/view_mini_cheetah.py

check:
	$(MAKE) -C mjlab check

test-config:
	cd mjlab && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run pytest tests/test_task_configs.py tests/test_mini_cheetah_training.py tests/test_velocity_task.py tests/test_asset_zoo.py -q

train-flat:
	cd mjlab && uv run train Mjlab-Velocity-Flat-MiniCheetah --env.scene.num-envs $(NUM_ENVS)

train-rough:
	cd mjlab && uv run train Mjlab-Velocity-Rough-MiniCheetah --env.scene.num-envs $(NUM_ENVS)
