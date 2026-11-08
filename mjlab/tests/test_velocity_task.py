"""Integrity checks for the two supported Mini Cheetah velocity tasks."""

import pytest

from mjlab.asset_zoo.robots import MINI_CHEETAH_ACTION_SCALE
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.tasks.registry import list_tasks, load_env_cfg
from mjlab.tasks.velocity.mdp import UniformVelocityCommandCfg

TASK_IDS = (
  "Mjlab-Velocity-Flat-MiniCheetah",
  "Mjlab-Velocity-Rough-MiniCheetah",
)


def test_only_mini_cheetah_tasks_are_registered() -> None:
  assert set(list_tasks()) == set(TASK_IDS)


@pytest.mark.parametrize("task_id", TASK_IDS)
def test_velocity_command_and_actions(task_id: str) -> None:
  cfg = load_env_cfg(task_id)
  assert isinstance(cfg.commands["twist"], UniformVelocityCommandCfg)
  action = cfg.actions["joint_pos"]
  assert isinstance(action, JointPositionActionCfg)
  assert action.scale == MINI_CHEETAH_ACTION_SCALE


@pytest.mark.parametrize("task_id", TASK_IDS)
def test_terrain_and_contact_sensors(task_id: str) -> None:
  cfg = load_env_cfg(task_id)
  assert cfg.scene.terrain is not None
  names = {sensor.name for sensor in cfg.scene.sensors or ()}
  assert {"feet_ground_contact", "foot_height_scan"} <= names
  if "Flat" in task_id:
    assert cfg.scene.terrain.terrain_type == "plane"
    assert cfg.scene.terrain.terrain_generator is None
    assert "terrain_scan" not in names
  else:
    assert cfg.scene.terrain.terrain_type == "generator"
    assert cfg.scene.terrain.terrain_generator is not None
    assert {"terrain_scan", "self_collision", "thigh_ground_touch"} <= names
