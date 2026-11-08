"""Regression checks for Mini Cheetah training configuration dependencies."""

import re

import mujoco
import pytest

from mjlab.asset_zoo.robots.mini_cheetah.mini_cheetah_constants import get_spec
from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.tasks.registry import load_env_cfg


@pytest.fixture(scope="module")
def robot_model() -> mujoco.MjModel:
  return get_spec().compile()


@pytest.fixture(params=("Flat", "Rough"))
def task_cfg(request) -> ManagerBasedRlEnvCfg:
  return load_env_cfg(f"Mjlab-Velocity-{request.param}-MiniCheetah")


def test_observation_sensors_exist(task_cfg, robot_model):
  """Every robot sensor requested by an observation must exist in the MJCF."""
  available = {robot_model.sensor(i).name for i in range(robot_model.nsensor)}
  for group in task_cfg.observations.values():
    for term in group.terms.values():
      sensor_name = term.params.get("sensor_name", "")
      if sensor_name.startswith("robot/"):
        assert sensor_name.removeprefix("robot/") in available


def test_posture_reward_covers_every_joint(task_cfg, robot_model):
  """Empty/partial tolerances cause reward tensor shape errors at runtime."""
  names = [
    robot_model.joint(i).name
    for i in range(robot_model.njnt)
    if robot_model.jnt_type[i] == mujoco.mjtJoint.mjJNT_HINGE
  ]
  assert len(names) == 12
  for regime in ("standing", "walking", "running"):
    tolerances = task_cfg.rewards["pose"].params[f"std_{regime}"]
    for name in names:
      matches = [v for p, v in tolerances.items() if re.fullmatch(p, name)]
      assert len(matches) == 1 and matches[0] > 0, (regime, name)


def test_training_model_uses_scene_terrain(robot_model):
  """An embedded plane bypasses scene terrain contact sensors on rough ground."""
  assert not any(t == mujoco.mjtGeom.mjGEOM_PLANE for t in robot_model.geom_type)


def test_friction_randomization_targets_feet(task_cfg):
  geoms = task_cfg.events["foot_friction"].params["asset_cfg"].geom_names
  assert set(geoms) == {f"{leg}_foot_collision" for leg in ("FR", "FL", "RR", "RL")}
