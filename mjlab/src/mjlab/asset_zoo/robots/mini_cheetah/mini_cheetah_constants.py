"""Mini Cheetah constants."""

from pathlib import Path

import mujoco

from mjlab import MJLAB_SRC_PATH
from mjlab.actuator import BuiltinPositionActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.actuator import ElectricActuator, reflected_inertia
from mjlab.utils.spec_config import CollisionCfg

##
# MJCF and assets.
##

MINI_CHEETAH_XML: Path = (
  MJLAB_SRC_PATH / "asset_zoo" / "robots" / "mini_cheetah" / "xmls" / "mini_cheetah.xml"
)
assert MINI_CHEETAH_XML.exists()


def get_spec() -> mujoco.MjSpec:
  return mujoco.MjSpec.from_file(str(MINI_CHEETAH_XML))


##
# Actuator config (MIT Mini Cheetah specs).
##

ROTOR_INERTIA = 0.000033  # 33e-6 kg m^2
GEAR_RATIO = 6

ACTUATOR = ElectricActuator(
  reflected_inertia=reflected_inertia(ROTOR_INERTIA, GEAR_RATIO),
  velocity_limit=30.0,
  effort_limit=17.0,
)

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS = 30.0
DAMPING = 0.8

MINI_CHEETAH_ACTUATOR_CFG = BuiltinPositionActuatorCfg(
  target_names_expr=(".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"),
  stiffness=STIFFNESS,
  damping=DAMPING,
  effort_limit=ACTUATOR.effort_limit,
  armature=ACTUATOR.reflected_inertia,
)

##
# Initial Pose Keyframe.
##

INIT_STATE = EntityCfg.InitialStateCfg(
  pos=(0.0, 0.0, 0.31),
  joint_pos={
    ".*_hip_joint": 0.0,
    # With parallel +Y joint axes, a negative calf angle needs positive thigh
    # flexion to place the feet beneath the body.
    ".*_thigh_joint": 0.8,
    ".*_calf_joint": -1.6,
  },
  joint_vel={".*": 0.0},
)

##
# Collision config.
##

_foot_regex = "^[FR][LR]_foot_collision$"

FEET_ONLY_COLLISION = CollisionCfg(
  geom_names_expr=(_foot_regex,),
  contype=0,
  conaffinity=1,
  condim=3,
  priority=1,
  friction=(0.8,),
  solimp=(0.9, 0.95, 0.023),
)

_collision_regex = r".*_collision"

FULL_COLLISION = CollisionCfg(
  geom_names_expr=(_collision_regex,),
  contype=1,
  conaffinity=1,
  solref=(0.01, 1),
  condim={_foot_regex: 6, _collision_regex: 1},
  priority={_foot_regex: 1, ".*": 0},
  friction={_foot_regex: (1.0, 5e-3, 5e-4)},
)

##
# Final config.
##

MINI_CHEETAH_ARTICULATION = EntityArticulationInfoCfg(
  actuators=(MINI_CHEETAH_ACTUATOR_CFG,),
  soft_joint_pos_limit_factor=0.9,
)


def get_mini_cheetah_robot_cfg() -> EntityCfg:
  """Get a fresh Mini Cheetah robot configuration instance."""
  return EntityCfg(
    init_state=INIT_STATE,
    collisions=(FULL_COLLISION,),
    spec_fn=get_spec,
    articulation=MINI_CHEETAH_ARTICULATION,
  )


MINI_CHEETAH_ACTION_SCALE: dict[str, float] = {}
for a in MINI_CHEETAH_ARTICULATION.actuators:
  assert isinstance(a, BuiltinPositionActuatorCfg)
  e = a.effort_limit
  s = a.stiffness
  names = a.target_names_expr
  assert e is not None
  for n in names:
    MINI_CHEETAH_ACTION_SCALE[n] = 0.25 * e / s
