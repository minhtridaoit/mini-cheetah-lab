"""Inspect the Mini Cheetah model using the environment's initial pose."""

import argparse
import re
import time

import mujoco
import mujoco.viewer

from mjlab.asset_zoo.robots.mini_cheetah.mini_cheetah_constants import (
  INIT_STATE,
  get_spec,
)


def load_robot() -> tuple[mujoco.MjModel, mujoco.MjData]:
  model = get_spec().compile()
  data = mujoco.MjData(model)
  data.qpos[:3] = INIT_STATE.pos
  data.qpos[3:7] = INIT_STATE.rot
  for joint_id in range(model.njnt):
    joint = model.joint(joint_id)
    for pattern, angle in (INIT_STATE.joint_pos or {}).items():
      if re.fullmatch(pattern, joint.name):
        data.qpos[joint.qposadr[0]] = angle
  mujoco.mj_forward(model, data)
  return model, data


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--check", action="store_true", help="Load without a GUI")
  args = parser.parse_args()
  model, data = load_robot()

  if args.check:
    print(f"Model loaded: {model.nq} position DOFs, {model.nv} velocity DOFs")
    for leg in ("FR", "FL", "RR", "RL"):
      print(f"{leg} foot position: {data.site(leg).xpos.round(4)}")
    return

  with mujoco.viewer.launch_passive(model, data) as viewer:
    with viewer.lock():
      viewer.cam.lookat[:] = (0.0, 0.0, 0.22)
      viewer.cam.distance = 1.15
      viewer.cam.azimuth = 125
      viewer.cam.elevation = -18
      viewer.opt.geomgroup[3] = 0
    print("Mini Cheetah Lab — standing pose preview; physics and policy stopped.")
    while viewer.is_running():
      viewer.sync()
      time.sleep(1.0 / 60.0)


if __name__ == "__main__":
  main()
