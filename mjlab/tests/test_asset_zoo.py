"""Check that the supported Mini Cheetah asset compiles."""

import mujoco

from mjlab.asset_zoo.robots import get_mini_cheetah_robot_cfg
from mjlab.entity import Entity


def test_mini_cheetah_compiles() -> None:
  model = Entity(get_mini_cheetah_robot_cfg()).compile()
  assert isinstance(model, mujoco.MjModel)
  assert model.nu == 12
